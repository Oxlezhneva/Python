from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import m3u8
import requests
import time
import json
import os 

my_list = ['https://']  
 
def link_browser_name(url):   

    list_link = []
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)

    email_input =  driver.find_element(By.XPATH, "//input[@class='form-control form-field-email']")
    email_input.clear()
    email_input.click()
    email_input.send_keys("test@mail.ru")

    password_input =  driver.find_element(By.XPATH, "//input[@class='form-control form-field-password']")
    password_input.clear()
    password_input.click()
    password_input.send_keys("password")

    driver.find_element(By.XPATH, "//button[@id='xdget431829_1_1_1_1_1_1_1_1_1_1_1_1_1_1_1_1_1']").click()
    time.sleep(10)

    title_name1 =  driver.find_element(By.XPATH, "//h1[text()]")
    time.sleep(10)
    ru_text = title_name1.text.replace('.', '')      
    name_parts1 = ru_text.split(" ")

    title_name2 =  driver.find_element(By.XPATH, "//h2[text()]")
    ru_text = title_name2.text.replace('.', '')      
    name_parts = ru_text.split(" ")     
    name_video = f'М{name_parts1[-1]}_У{"_".join(name_parts[1:4])}'    
    # {name_parts1[0]}_
    # name_video = 'name_1'  
    # print(name_video)
    video_link =  driver.find_elements(By.XPATH, "//iframe[@class='vhi-iframe js--vhi-iframe']")
    time.sleep(40)
    for item in video_link:
        url2 = item.get_attribute("src")
        list_link.append(url2)            
    return name_video, list_link

def link_console(url2):

    browser_console = DesiredCapabilities.CHROME
    browser_console['goog:loggingPrefs'] = { 'performance':'ALL' }
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), desired_capabilities=browser_console)
    driver.get(url2)    
    console_data = driver.get_log('performance')
    logs_json = []
    for item in  console_data:
        a = item["message"]
        item = logs_json.append((json.loads(a)))   
    for item in logs_json:                
        if 'response' in item['message']['params']:
            z = item['message']['params']['response']["url"]                           
            if "master.m3u8"  in z:
                url3 = (z.split('?'))[0]                
                return  url3
                

def link_m3u8_480(name_video, url3):
   
    sess = requests.Session()
    res  = sess.get(url3)
    m3u8_master = m3u8.loads(res.text)    
    for playlist in m3u8_master.data['playlists']:        
        if "480.m3u8" in playlist['uri']:
            playlist_uri = playlist['uri']
            final_url = (playlist_uri.split('?'))[0] 
            command = str(f"ffmpeg -i {final_url} -c copy -bsf:a aac_adtstoasc {name_video}.mp4") 
            os.system(command)            
            
 
def main():
    count = 0    
    for item in my_list:
        count2 = 0
        count += 1
        name_video, list_link = link_browser_name(item)
        for item in list_link:          
            count2+=1
            url3 = link_console(item)
            name_video1 = f'{name_video}_{count2}'
            link_m3u8_480(name_video1, url3)
            time.sleep(10)
            print(count)


main()
