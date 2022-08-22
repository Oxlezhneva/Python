import pandas as pd
import re
import csv

my_list = []

with open("phonebook_raw.csv", encoding = "UTF-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)    

for item in contacts_list:
    name_1 = (item[0].split())
    name_2 = (item[1].split())           
    if len(name_1) == 3:          
        item[0] = name_1[0]
        item[1] = name_1[1]
        item[2] = name_1[2]
    elif len(name_1) == 2:
        item[0] = name_1[0]
        item[1] = name_1[1]
    elif len(name_2) == 2:
        item[1] = name_2[0]
        item[2] = name_2[1]        
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})\-*(\d{2})\-*(\d+)(\s*)\(*([а-яА-я]+\.)*\s*(\d+)*\)*(\.)*"
    repl = r"+7(\2)\3-\4-\5\6\7\8\9"
    item[5] = re.sub(pattern, repl, item[5])
    if (len(item)) == 8 and item[7] == '':
        item.pop(7)
    my_list.append(item)
 
    

for item in range(1,len(my_list)):    
    for element in range(2,len(my_list)):        
        if my_list[item][0] == my_list[element][0] and my_list[item][1] == my_list[element][1] and item != element:                     
            for component in range(2,7):
                if my_list[item][component] != my_list[element][component]:                   
                    if my_list[item][component] == "":
                        my_list[item][component] = my_list[element][component]                                                  
                    elif my_list[element][component] == "":
                        my_list[element][component] = my_list[item][component]
                    elif my_list[item][component] != "" and my_list[element][component]!= "":
                        combining = f'{my_list[item][component]} / {my_list[element][component]}'
                        my_list[element][component] = combining
                        my_list[item][component] = combining
        

list_drop_duplicates = pd.Series(my_list).drop_duplicates().tolist() 

with open("phonebook.csv", "w", encoding = "UTF-8", newline='') as f:
  datawriter = csv.writer(f, delimiter=',')  
  datawriter.writerows(list_drop_duplicates)