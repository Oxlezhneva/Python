import time
import requests
import json
import conf
from tqdm import tqdm
import VK

class YaUploader(): 

    def autorization_disk(self):
        a = input(f'Введите токен для Яндекс.Диска(Выход - "q"): ')
        if a != 'q':            
            url ='https://cloud-api.yandex.net/v1/disk/'
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'OAuth {a}'
            }
            try:
                response = requests.get(url,headers=headers)
                response.raise_for_status()
                if response.status_code== 200:
                    global token1
                    token1 = a
                    global test  
                    test = 2                                    
            except:
                print(f"Ошибка ввода токена для Яндекс.Диска")
                self.autorization_disk()
        else:
            print("Выход из программы")                     
            return   
        
    def create_folder(self):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token1}'
        }
        params_create = {'path': conf.foldername}
        folder_name =  params_create["path"]
        try:          
            res = requests.put(url, headers=headers, params = params_create)
            res.raise_for_status()
            if res.status_code == 201:            
                print(f'На Яндекс.Диске создана новая папка {params_create["path"]}')
        except requests.exceptions.HTTPError:
                print(f'Фотографии будут загружены в папку {params_create["path"]} на Яндекс.Диске')        
        global folder
        folder = folder_name
        return       
       
    def upload_disc_api(self):       
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {token1}'
        } 
        name_folder = folder
        try:
            print(f'По умолчанию на Яндекс.Диск можно загрузить только {conf.filedisk} фото')
            list_json = []
            count = 0                              
            for item in tqdm(VK.listik, ncols = 50, total = conf.filedisk):               
                file_name_disk =(item['file_name'])
                url_photo = (item["url"])
                param = {"path": f'{name_folder}/{file_name_disk}', "url": url_photo, "overwrite": "true" }
                response = requests.post(url, headers=headers, params=param)
                time.sleep(1)
                response.raise_for_status()               
                if response.status_code == 202:
                    count += 1                          
                    dict_json = {'file_name':file_name_disk, 'size' : (item[file_name_disk]) }
                    list_json.append(dict_json)
                    if count > conf.filedisk:
                        break        
                else:
                    print(f'Ошибка при загрузке {count} файлов. Код {response.status_code}')             
        except:                
            print(f'Выход из программы')   
            return 
        print(f'Фотографии успешно загружены на Яндекс.Диск')
        with open('data.json', 'w') as fp:     
            data = json.dump(list_json, fp)
        return data