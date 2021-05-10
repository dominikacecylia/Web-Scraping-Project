from selenium import webdriver
from pprint import pprint
import json
import requests
import time

"""Try:
    - storing data in csv
    - try and catch for exception of lacking details on particular products
    - 
"""

class CoffeeScraper2:
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def search(self, url):
        self.driver.get(url)
        
    
    def _get_coffee_details(self):
        img_url = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]//img').get_attribute('src')
        price = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/span[3]').text
        description = self._get_details_in_table('//*[@id="description"]/span/div[1]')

        self._click_on_button('//*[@id="tabs"]/ul/li[2]/a/span')
        
        coffee_details = self._get_details_in_table('//*[@id="attributes"]/table')
        return img_url, price, description, coffee_details

    def scrape(self):
        urls = ('https://www.coffeedesk.pl/kawa/filters/on-page/120/0/','https://www.coffeedesk.pl/kawa/filters/on-page/120/1/') 
        #'https://www.coffeedesk.pl/kawa/filters/on-page/120/2/') #,'https://www.coffeedesk.pl/kawa/filters/on-page/120/3/'
        # 'https://www.coffeedesk.pl/kawa/filters/on-page/120/4/','https://www.coffeedesk.pl/kawa/filters/on-page/120/5/'#
        # 'https://www.coffeedesk.pl/kawa/filters/on-page/120/6/','https://www.coffeedesk.pl/kawa/filters/on-page/120/7/')
        for url in urls:
            self.search(url)

            coffees = self.driver.find_elements_by_xpath('//div[@class="products-list"]//a')
            print(len(coffees))

            links = [coffee.get_attribute('href') for coffee in coffees]
            # for coffee in coffees:
            #     link = coffee.get_attribute('href')
            #     links.append(link)
                

            details = []
            for idx, link in enumerate(links):

                self.driver.get(link)
                img_url, price, description, coffee_details = self._get_coffee_details()

                if '.png' in img_url:
                    ext = 'png'
                else:
                    ext = 'jpg'
                self._download_file(img_url, f'data/pictures/c2/kawa_{idx}.{ext}')

                detail = {
                    'img_url' : img_url,
                    'price' : price,
                    'coffee_details' : coffee_details,
                    'description' : description
                }
                details.append(detail)

            with open('data/data_pl_coffee_part1.json', 'w') as f:
                json.dump(details, f, indent=4)


    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')

    def _download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)

    def _click_on_button(self, xpath):
        button = self.driver.find_element_by_xpath(xpath)
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(1)
    
    def _get_details_in_table(self, xpath):
        details = self.driver.find_elements_by_xpath(xpath)
        all_details = [detail.text for detail in details]
        return all_details






scraper2 = CoffeeScraper2()
scraper2.scrape()
