from distutils.util import strtobool
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
import yaml  
from backend.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, OrderItem, \
    Contact, ConfirmEmailToken
from backend.serializers import UserSerializer, CategorySerializer, ShopSerializer, ProductInfoSerializer, \
    OrderItemSerializer, OrderSerializer, ContactSerializer, PartnerOrderSerializer
from backend.signals import new_user_registered, new_order
from backend.permissions import ByerPermission, ShopPermission
from rest_framework.viewsets import ModelViewSet

class RegisterAccount(APIView):
    """
    Для регистрации покупателей/магазина
    """
     
    def post(self, request, *args, **kwargs):

        """
        Регистрация методом POST
        {   "username" : "username",
            "first_name": "Иван",
            "last_name":"Иванович",
            "company":"Рога и Копыта",
            "position":"менеджер",
            "email": "email@yandex.ru",
            "password": "пароль"
        для магащина добавляем:
            "type": "shop"}   
        получили на почту токен 
        """

        if {'first_name', 'last_name', 'email', 'password', 'company', 'position'}.issubset(request.data):      # проверяем обязательные аргументы
            errors = {}            
            try:                                                # проверяем пароль на сложность
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []                
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:                   
                request.data.update({})     # проверяем данные для уникальности имени пользователя
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():                    
                    user = user_serializer.save()       # сохраняем пользователя
                    user.set_password(request.data['password'])
                    user.save()
                    new_user_registered.send(sender=self.__class__, user_id=user.id)
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class LoginAccount(APIView):
    """
    Класс для авторизации пользователей
    """
    
    def post(self, request, *args, **kwargs):

        """           
        Авторизация 
        {"email" : "test@yandex.ru",
            "password": "пароль"}

        Для сброса пароля
        http://127.0.0.1:8000/api/v1/user/password_reset
        {    "email": "test@yandex.ru"}
        Новый пароль
        http://127.0.0.1:8000/api/v1/user/password_reset/confirm
        {
        "password": "новый пароль",
        "token": "токен из письма для сброса"

        """

        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Token': token.key})
            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccount(APIView):
    """
    Класс для подтверждения почтового адреса
    """
    
    def post(self, request, *args, **kwargs):

        """    
        Подтверждение почтового ящика
        {"email" : "test@yandex.ru",
        "token": "токен из письма при регистрации"}
        """

        # проверяем обязательные аргументы
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                    key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

class AccountDetails(APIView):
    """
    Класс для работы данными пользователя
    """
    permission_classes = [ByerPermission]

    # получить данные
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    # Редактирование методом POST
    def post(self, request, *args, **kwargs):     
       
        if 'password' in request.data:     # проверяем обязательные аргументы
            errors = {}            
            try:                                                # проверяем пароль на сложность
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []               
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])       
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)   # проверяем остальные данные
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})

class ContactView(APIView):
    """
    Класс для работы с контактами покупателей
    """
    permission_classes = [ByerPermission]

    # получить мои контакты
    def get(self, request, *args, **kwargs):
        
        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    # добавить новый контакт
    def post(self, request, *args, **kwargs):

        """        
        {
        "city": "Москва",
        "street": "Новокосинская",
        "house": "5",
        "structure": "2",
        "building": "3",
        "apartment": "5",
        "phone": "+7(926)555-53-64-75"
        }
            """
        
        if {'city', 'street', 'phone'}.issubset(request.data):            
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить контакт
    def delete(self, request, *args, **kwargs):

        """
          {"items":  "5"}
        """
        
        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            query = Q()
            objects_deleted = False
            for contact_id in items_list:
                if contact_id.isdigit():
                    query = query | Q(user_id=request.user.id, id=contact_id)
                    objects_deleted = True
            if objects_deleted:
                deleted_count = Contact.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # редактировать контакт
    def put(self, request, *args, **kwargs):

        """
        {
        "id": 1,
        "city": "Москва",
        "street": "Победы",
        "house": "5",
        "structure": "2",
        "building": "3",
        "apartment": "5",
        "phone": "+7(926)555-55-55"
        }
        """
        if 'id' in request.data:
            if request.data['id'].isdigit():
                contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
                print(contact)
                if contact:
                    serializer = ContactSerializer(contact, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'Status': True})
                    else:
                        JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

class PartnerUpdate(APIView):
    """
    Класс для обновления прайса от поставщика(магазина)
    """
    permission_classes = [ShopPermission]

    #Добавляем/обновляем прайс из файла
    def post(self, request, *args, **kwargs):  
        
        """
        {"file": "data/shop1.yaml"}
        """  
        try:
            user_id = request.user.id
            filename = request.data.get('file')                                 
            if filename:  # извлечение информации из файла
                with open(filename, 'r', encoding='utf-8') as stream:
                    data = yaml.safe_load(stream)
                    print(data)
            else:
                JsonResponse({'Status': False, 'Error': 'The source of information is incorrectly specified'})
            try:  # загрузка информации в базу данных
                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=user_id)
            except IntegrityError as error:
                return JsonResponse({'Status': False, 'Error': f'{error}'})
            Shop.objects.filter(user_id=user_id).update(filename=filename)
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()
            ProductInfo.objects.filter(shop_id=shop.id).delete()
            for item in data['goods']:
                product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'],
                                                           id=item['id'])
                product_info = ProductInfo.objects.create(product_id=product.id,
                                                          model=item['model'],
                                                          price=item['price'],
                                                          price_rrc=item['price_rrc'],
                                                          quantity=item['quantity'],
                                                          shop_id=shop.id)
                for name, value in item['parameters'].items():
                    parameter_object, _ = Parameter.objects.get_or_create(name=name)
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter_object.id,
                                                    value=value)
            return JsonResponse({'Status': True})
        except BaseException as error:
            return JsonResponse({"Status": "False", "Error": f"{error.__str__()}"})



class CategoryView(ListAPIView):
    """
    Класс для просмотра категорий
    """
    permission_classes = [ByerPermission]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ShopView(ListAPIView):
    """
    Класс для просмотра списка магазинов
    """
    permission_classes = [ByerPermission]
    queryset = Shop.objects.filter(state=True)
    serializer_class = ShopSerializer


class ProductInfoView(APIView):
    """
    Класс для поиска товаров по магазину, категории, карточка товара
    """
    permission_classes = [ByerPermission]

    def get(self, request, *args, **kwargs):

        """
        http://127.0.0.1:8000/api/v1/products/?category_id=221 поиск по id категории 
        http://127.0.0.1:8000/api/v1/products/?shop_id=8       поиск по id магазину
        http://127.0.0.1:8000/api/v1/products/?product_id=24   карточка товара по его id 
        """

        query = Q(shop__state=True)
        shop_id = request.query_params.get('shop_id')
        category_id = request.query_params.get('category_id')
        product_id = request.query_params.get('product_id')
        if shop_id:
            query = query & Q(shop_id=shop_id)
        if category_id:
            query = query & Q(product__category_id=category_id)          
        if product_id:
            query = query & Q(id=product_id)
        # фильтруем и отбрасываем дуликаты
        queryset = ProductInfo.objects.filter(
            query).select_related(
            'shop', 'product__category').prefetch_related(
            'product_parameters__parameter').distinct()
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class BasketView(APIView):
    """
    Класс для работы с корзиной пользователя
    """
    permission_classes = [ByerPermission]

    # посмотреть корзину
    def get(self, request, *args, **kwargs):

        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    # создать корзину / добавить товары
    def post(self, request, *args, **kwargs):
        """
        {
        "items": [
            {"quantity":"4","product_info" : "24"},
            {"quantity":"5", "product_info" : "8"}
                 ]
        }
        """        
        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = items_sting
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': basket.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return JsonResponse({'Status': False, 'Errors': str(error)})
                        else:
                            objects_created += 1
                    else:

                        JsonResponse({'Status': False, 'Errors': serializer.errors})
                return JsonResponse({'Status': True, 'Создано объектов': objects_created})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # удалить товары из корзины
    def delete(self, request, *args, **kwargs):

        """
        {"items": "38,39,40"} , где числа, это id товара в корзине
        """       
        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            query = Q()
            objects_deleted = False
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    query = query | Q(order_id=basket.id, id=order_item_id)
                    objects_deleted = True
            if objects_deleted:
                deleted_count = OrderItem.objects.filter(query).delete()[0]
                return JsonResponse({'Status': True, 'Удалено объектов': deleted_count})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    # изменить количество товара в корзине
    def put(self, request, *args, **kwargs):

        """
        {
        "items": [{"quantity":  10, "id" : 65}]    
        }
        """        
        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = items_sting
            except ValueError:
                JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
                objects_updated = 0
                for order_item in items_dict:
                    if type(order_item['id']) == int and type(order_item['quantity']) == int:
                        objects_updated += OrderItem.objects.filter(order_id=basket.id, id=order_item['id']).update(
                            quantity=order_item['quantity'])
                return JsonResponse({'Status': True, 'Обновлено объектов': objects_updated})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

class OrderView(APIView):
    """
    Класс для получения и размешения заказов пользователями
    """
    permission_classes = [ByerPermission]

    # получить заказ пользователя
    def get(self, request, *args, **kwargs):
        
        order = Order.objects.filter(user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category','ordered_items__product_info__product_parameters__parameter').select_related(
            'contact').annotate(total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    # разместить заказ из корзины
    def post(self, request, *args, **kwargs):

        """
        {"id" : "19", "contact" : "7"}
        """        
        if {'id', 'contact'}.issubset(request.data):
            if request.data['id'].isdigit():
                try:
                    is_updated = Order.objects.filter(
                        user_id=request.user.id, id=request.data['id']).update(
                        contact_id=request.data['contact'],
                        state='new')
                except IntegrityError as error:
                    print(error)
                    return JsonResponse({'Status': False, 'Errors': 'Неправильно указаны аргументы'})
                else:
                    if is_updated:
                        new_order.send(sender=self.__class__, user_id=request.user.id)
                        return JsonResponse({'Status': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class PartnerState(APIView):
    """
    Класс для работы со статусом поставщика
    """
    permission_classes = [ShopPermission]

    # получить текущий статус
    def get(self, request, *args, **kwargs):
      
        shop = request.user.shop
        serializer = ShopSerializer(shop)
        return Response(serializer.data)

    # изменить текущий статус
    def post(self, request, *args, **kwargs):
        """
        {"state" : "on"}
        {"state" : "off"}
        """        
        state = request.data.get('state')
        if state:
            try:
                Shop.objects.filter(user_id=request.user.id).update(state=strtobool(state))
                return JsonResponse({'Status': True})
            except ValueError as error:
                return JsonResponse({'Status': False, 'Errors': str(error)})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


# class PartnerOrders(APIView):
#     """
#     Класс для получения заказов поставщиками
#     """
#     permission_classes = [ShopPermission]

#     #получить заказы от пользователей
#     def get(self, request, *args, **kwargs):
        
#         order = Order.objects.filter(
#             ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
#             'ordered_items__product_info__product__category',
#             'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
#             total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
#         serializer = OrderSerializer(order, many=True)
#         return Response(serializer.data)


class PartnerOrdersViewSet(ModelViewSet):
    """
    Класс для получения заказов поставщиками
    """
    queryset = Order.objects.all()    
    permission_classes = [ShopPermission]

    # получить заказы от пользователей
    def list(self, request, *args, **kwargs):
        
        order = Order.objects.filter(
            ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').select_related('contact').annotate(
            total_sum=Sum(F('ordered_items__quantity') * F('ordered_items__product_info__price'))).distinct()
        serializer = PartnerOrderSerializer(order, many=True)
        return Response(serializer.data)