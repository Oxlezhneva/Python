import requests
import time
import requests
import conf
from tqdm import tqdm
from pprint import pprint
import time

class VkUser: 
    with open('token.txt', 'r') as file_object:
        token = file_object.read().strip()                    
       
    def __init__(self):        
        self.params = {
            'access_token': self.token,
            'v': '5.131'                       
        }  

    def autorization_VK(self):
        try:
            a = input(f'Введите id Вконтатке (Выход - "q"): ')
            if a != 'q' and a!= '':           
                url = 'https://api.vk.com/method/users.get'
                params = {
                        'user_id': a,
                        'name_case' : 'gen' 
                }                
                response = requests.get(url, params={**self.params, **params})
                response.raise_for_status()        
                if len(response.json()['response']) !=0:                   
                    for i in response.json()['response']: 
                        if i['is_closed'] == False:              
                            tell = input(f'Если Вы хотите скачать фото со страницы {i["first_name"]} {i["last_name"]}, введите "y". Для повторного ввода нажмите "n", для выхода любую клавишу : ')
                            if tell == "y":
                                global id
                                id = i['id']
                                return id               
                            else:
                                if tell == "n":
                                    self.autorization_VK()
                                else:                                         
                                    return 
                        else:
                            print(f'С данной страницы невозможно скачать данные')
                            self.autorization_VK()                              
                else:
                    print(f'С данной страницы невозможно скачать данные')
                    self.autorization_VK()
            else:                     
                return
        except:
            print(f'Ошибка вода токена от Вконтакте в файле token.txt')
            return

  
    def upload_vk_api(self):
                        
        url = 'https://api.vk.com/method/photos.get'
        param_photo = {             
            'album_id' : 'profile', 
            'extended' : 'likes',
            'count': conf.filevk,
            'photo_sizes' : '1',
            'user_id' : id               
        }
        count=0
        list_all_data = []
        listnames = []
        dict_all_data = {}
        try:            
            res = requests.get(url, params={**self.params, **param_photo})
            res.raise_for_status()                                  
            data = res.json()['response']['items']                                 
            if res.status_code == 200:
                for q in data:                    
                    if  q['owner_id'] == param_photo['user_id']:                                                                         
                        continue                                           
                    else:                        
                        return
                for item in tqdm(data, ncols = 50):                                          
                    count += 1
                    time.sleep(0.1)  
                    url_foto = item['sizes'][-1]['url']
                    size = item['sizes'][-1]['type']
                    date_public = item['date']
                    count_likes = item['likes']['count']
                    file_name_like = f'{count_likes}.jpg'
                    file_name_date = f'{count_likes}_{date_public}.jpg'
                    if  file_name_like not in  listnames:
                        dict_all_data = {'file_name':file_name_like, "size": size, "url": url_foto, file_name_like: size}                    
                    else:
                        dict_all_data = {'file_name':file_name_date, "size": size, "url": url_foto, file_name_date: size}      
                    list_all_data.append(dict_all_data)
                    listnames.append(dict_all_data['file_name'])                    
                print(f' Из "Вконтакте" было выгружено {count} фото.')
                global listik
                listik = list_all_data
                global test
                test = 1                 
        except:
            print(f'Выход из программы')
            return            
        return                              
     
