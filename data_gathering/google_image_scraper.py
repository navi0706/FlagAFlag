from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import time
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from data_gathering.settings import Config

from settings import Config

#load csv containing list of countries
table = pd.read_csv("list_of_countries.csv")
convert_to_list = table["Država"].tolist()

# Init env variables
env_config = Config()
chromedriver = env_config.CHROMEDRIVER_PATH
data_gathering_path = env_config.DATA_GATHERING_PATH

max_counter = 20


def scrape_data(list_of_countries):
    # Scrape images for each country in the list
    for country in list_of_countries:
        try:
            os.mkdir(country)
        except Exception as e:
            #TODO implementing logging, better handling
            print("Issue when creating directory")
        
        # Get data from webpage
        driver = webdriver.Chrome(executable_path=chromedriver)
        driver.get("https://www.google.com/imghp?hl=en")

        try:       
            element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#sbtc > div > div.a4bIc > input"))
                    )
            element.send_keys(f"{country} flag")
            element.send_keys(Keys.RETURN)

            scroll_counter = 0

            while scroll_counter< max_counter:  
            #Scrolling down to the end of the 
                driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
                time.sleep(3)
                scroll_counter+=1
                try:
                    driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
                except Exception as e:
                    pass

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.close()

        except Exception as e:
            driver.quit()


        #find img in the url
        downloaded_images = soup.find_all("img", class_="rg_i")

        image_counter = 1
        for image in downloaded_images:
            urllib.request.urlretrieve(image["src"],f"{data_gathering_path}/{country}/{image_counter}.jpg")
            image_counter+=1
            print(f"For country - {country}: Downloaded {image_counter}")
        