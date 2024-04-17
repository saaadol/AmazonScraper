from amazoncaptcha import AmazonCaptcha
from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tkinter import messagebox
from datetime import datetime

my_path = os.getcwd()
keyword = input("Type a keyword to scrape: ")
class Amazon:
    def __init__(self) -> None:
        self.name = []
        self.whole_price = []
        self.fract_price = []
        self.number_of_reviews = []
        self.reviews_rating = []
        self.category = []
        self.link = []
        self.keyword = None
    def get_data(self):
        driver = webdriver.Chrome()  
        driver.get('https://www.amazon.com/')

        captcha = AmazonCaptcha.fromdriver(driver)
        solution = captcha.solve()
        try:
            t =  driver.find_element(By.XPATH, '//*[@id="captchacharacters"]')
            t.send_keys(solution)
            time.sleep(3)
            t.send_keys(Keys.ENTER)
            x = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')
            time.sleep(3)
            self.keyword = keyword
            x.send_keys(self.keyword)
            time.sleep(1)
            x.send_keys(Keys.ENTER)
            time.sleep(2)
        except:
            pass
        i = 0
        while(True):
            
            time.sleep(3)
            items = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
            for item in items:
                try:
                    name = item.find_elements(By.XPATH, './/span[@class="a-size-base-plus a-color-base a-text-normal"]')
                    for n in name:
                        self.name.append(n.text)
                    self.current_time = datetime.now()  
                except:
                   self.name.append("None") 
                try:
                    category = item.find_elements(By.XPATH, './/span[@class="a-size-base a-color-base s-background-color-platinum a-padding-mini aok-nowrap aok-align-top aok-inline-block a-spacing-top-micro puis-medium-weight-text"]')
                    for t in category:
                        if (t.text == None or t.text == ""):
                            self.category.append("None")
                        else:
                            self.category.append(t.text)
                except:
                    self.category.append("None")
                try:
                    reviews = item.find_elements(By.XPATH, ".//span[contains(@aria-label, 'stars')]")
                    for number_of_reviews in reviews:
                        sibling_element = number_of_reviews.find_element(By.XPATH, "./following-sibling::span")
                        self.reviews_rating.append(number_of_reviews.get_attribute('aria-label'))
                        self.number_of_reviews.append(sibling_element.get_attribute('aria-label'))
                except:
                    self.reviews_rating.append("None")
                    self.number_of_reviews.append("None")
                try:
                    link = item.find_elements(By.XPATH, './/a[@class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
                    for specific_link in link:
                        self.link.append(specific_link.get_attribute('href'))
                except:
                    self.link.append("None")
                
                try:
                    fract_price  = item.find_elements(By.XPATH, './/span[@class="a-price-fraction"]')
                    for price in fract_price:
                        self.fract_price.append(price.text)
                except:
                    self.fract_price.append("")
                try:
                    whole_price = item.find_elements(By.XPATH, './/span[@class="a-price-whole"]')
                    for price in whole_price:
                        self.whole_price.append(price.text)
                except:
                    self.whole_price.append("")
            time.sleep(5)
            button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//a[contains(@aria-label, 'Go to next page')]")))
            button.click()
            i = i + 1
            if (i == 2):
                break

        for i in range(0, len(self.whole_price)):    
            if (self.fract_price[i] != ""):
                self.whole_price[i] = self.whole_price[i] + "," + self.fract_price[i] + "$"
        min_length = min(len(self.name), len(self.whole_price), len(self.number_of_reviews), len(self.reviews_rating), len(self.category), len(self.link))
        print("this is min_length ", min_length)
        if len(self.name) > min_length:
            self.name = self.name[:-(len(self.name) - min_length)]

        if len(self.whole_price) > min_length:
            self.whole_price = self.whole_price[:-(len(self.whole_price) - min_length)]

        if len(self.number_of_reviews) > min_length:
            self.number_of_reviews = self.number_of_reviews[:-(len(self.number_of_reviews) - min_length)]

        if len(self.reviews_rating) > min_length:
            self.reviews_rating = self.reviews_rating[:-(len(self.reviews_rating) - min_length)]

        if len(self.category) > min_length:
            self.category = self.category[:-(len(self.category) - min_length)]

        if len(self.link) > min_length:
            self.link = self.link[:-(len(self.link) - min_length)]
        if len(self.current_time) > min_length:
            self.current_time = self.current_time[:-(len(self.current_time) - min_length)]

    def saving_data(self):
        data = {
            'name' : self.name,
            'price':self.whole_price,
            'number of reviews': self.number_of_reviews,
            'reviews rating': self.reviews_rating,
            'category': self.category,
            'link': self.link,
            'Date_of_Scrape': self.current_time
        }
        self.df = pd.DataFrame(data)
        # self.df['Date_of_Scrape'] = pd.to_datetime(self.df['Date_of_Scrape'])
        # self.df['Date_of_Scrape'] = self.df['Date_of_Scrape'].dt.strftime('%Y-%m-%d')
        # try:
            
        #     existing_df = pd.read_excel(f'{my_path}/amazon_{self.keyword}.xlsx')
        #     existing_df = pd.concat([existing_df, self.df])
        #     existing_df = existing_df.drop_duplicates(subset=['Job_title', 'Job_provider'])
        #     existing_df = existing_df.reset_index(drop=True)
        #     existing_df.to_excel(f'{my_path}/new_output_linkedin_{self.keyword}_{self.location}.xlsx', index=False)
        # except:
        self.df.to_excel(f'amazon_{self.keyword}.xlsx', index= False)
            
        messagebox.showinfo('Done', 'File has been created successfully') 

obj = Amazon()
driver = obj.get_data()
obj.saving_data()

driver.quit()
