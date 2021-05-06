from selenium import webdriver
from pprint import pprint
import json
import requests
import time

class CoffeeScraper:
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def search(self):
        self.driver.get('https://www.coffeedesk.pl/kawa/')
        time.sleep(5)
    
    def _get_coffee_details(self):
        img_url = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]/div[2]/div/div[1]/div[2]/img').get_attribute('src')
        # price = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/div[1]/div/span').text
        # origin = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/ng-container/div/div[2]/div[2]/div/p').text
        print(img_url)
        # print(price)
        # print()
        return img_url

    def scrape(self):
        self.search()
        # coffees = self.driver.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div[4]') #issue as not a list
        coffees = self.driver.find_elements_by_class_name('products-list')

        links = []
        for coffee in coffees:
            link = coffee.find_element_by_tag_name('a').get_attribute('href')
            links.append(link)
            time.sleep(5)

        details = []
        for idx, link in enumerate(links):

            self.driver.get(link)
            time.sleep(5)

            img_url = self._get_coffee_details()

            if '.png' in img_url:
                ext = 'png'
            else:
                ext = 'jpg'
            self.download_file(img_url, f'data/pictures/c2/kawa_{idx}.{ext}')

            detail = {
                'img_url' : img_url#,
                # 'price' : price,
                # 'origin' : origin
            }
            details.append(detail)

        with open('data/data_pl_coffee.json', 'w') as f:
            json.dump(details, f, indent=4)


    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')

    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)


scraper = CoffeeScraper()
scraper.scrape()
