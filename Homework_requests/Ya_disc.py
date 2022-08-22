import os
import requests

class YaUploader:
    def __init__(self, token: str):
        self.token = token        

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, files_path:str):
            upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
            headers = self._get_headers()
            params = {"path": f'test/{os.path.basename(files_path)}', "overwrite": "true"}
            response = requests.get(upload_url, headers=headers, params=params)
            return response.json()

    def upload(self, files_path:str):
        href = self._get_upload_link(files_path).get("href", "")
        with open(files_path, 'rb') as f:            
            response = requests.put(href, data=f)
            response.raise_for_status()
            if response.status_code == 201:
                print("Success")

    
if __name__ == '__main__':
    token = input('Введите OAuth-токен: ')  
    path_to_file = input('Введите путь к файлу на компьютере: ')  
    uploader = YaUploader(token)  
    result = uploader.upload(path_to_file)




