
from pprint import pprint

def dict_cook_book():
    cook_book = {} 
    with open("recipes.txt", encoding='utf-8') as file:           
        for i in file:
            dish = i.strip()
            count = int(file.readline().strip())                   
            listing = []
            for k in range(count):
                ingredient = (file.readline().strip().split('|'))
                other = {'ingredient_name':ingredient[0], 'quantity':ingredient[1], 'measure':ingredient[2]}
                listing.append(other)
            cook_book[dish] = listing
            file.readline().strip()    
    return cook_book   

def get_shop_list_by_dishes(dishes, person_count):
    dict_by_dishes = {}    
    for i in dishes:
        if i in dict_cook_book():
            dishes_count = dict_cook_book()[i]            
            for k in dishes_count:
                list_dishes_count = list(k.values())
                list_keys = list(k.keys())
                if list_dishes_count[0] in dict_by_dishes:
                    dict_other = dict_by_dishes[list_dishes_count[0]]
                    count_dishes = dict_other['quantity']
                    dict_by_dishes[list_dishes_count[0]] = {list_keys[2]:list_dishes_count[2], list_keys[1]:int(list_dishes_count[1])*person_count+count_dishes}       
                else:
                    dict_by_dishes[list_dishes_count[0]] = {list_keys[2]:list_dishes_count[2], list_keys[1]:int(list_dishes_count[1])*person_count}
    pprint(dict_by_dishes)            
    
print(dict_cook_book())
print()
get_shop_list_by_dishes(['Омлет', 'Омлет'], 2)





   

    

            
            

           
        
            


          


            
    

    

        


        