from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_experimental_option("detach", True)

def link_browser_name():   
    chr_options = Options()
    chr_options.add_experimental_option("detach", True)
    
    with open("Algorithms_and_Data_Structures.txt", 'a', encoding='utf-8') as f:

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chr_options)
        url = f'http://aliev.me/runestone/Introduction/Objectives.html'
        driver.get(url)
        
        for i in range(1, 164): 
            email_input =  driver.find_element(By.XPATH, "//div[@class='section']")
            print(email_input.text)
            time.sleep(10)
            f.write(str(email_input.text))
            time.sleep(10)
            email_input =  driver.find_element(By.XPATH, "//*[@id='relations-next']/a")       
            email_input.click()    
            time.sleep(5)
        
        



link_browser_name()