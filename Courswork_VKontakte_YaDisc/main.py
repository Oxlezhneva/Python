from Disk import YaUploader
from VK import VkUser
import VK
import Disk

def start_program(): 
    try:
        uploader = VkUser()
        uploader.autorization_VK()
        uploader.upload_vk_api()
        if VK.test == 1:            
            loader = YaUploader()
            loader.autorization_disk()            
            if Disk.test == 2:
                loader.create_folder()    
                loader.upload_disc_api()                
            else:                
                return    
    except:
        return 

       
   
start_program()


# 552934290 (тестовый id)


