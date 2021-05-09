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

    def search(self):
        self.driver.get('https://www.coffeedesk.pl/kawa/')
        
    
    def _get_coffee_details(self):
        img_url = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]//img').get_attribute('src')
        price = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/span[3]').text

        description_elements = self.driver.find_elements_by_xpath('//*[@id="description"]/span/div[1]')
        description = []
        for element in description_elements:
            description.append(element.text)

        details_button = self.driver.find_element_by_xpath('//*[@id="tabs"]/ul/li[2]/a/span')
        self.driver.execute_script("arguments[0].click();", details_button)
        time.sleep(1)
        
        details = self.driver.find_elements_by_xpath('//*[@id="attributes"]/table')

        coffee_details = []
        for detail in details:
            coffee_details.append(detail.text)
        # process = self.driver.find_element_by_xpath('//*[@id="attributes"]/table/tbody/tr[6]/td[2]').text
        # grind_types = self.driver.find_element_by_xpath('//*[@id="attributes"]/table/tbody/tr[8]/td[2]').text
        # roast = self.driver.find_element_by_xpath('//*[@id="attributes"]/table/tbody/tr[7]/td[2]').text
        # //*[@id="attributes"]/table/tbody/tr[7]/td[2]
        # blend = self.driver.find_element_by_xpath('//*[@id="attributes"]/table/tbody/tr[5]/td[2]').text

        return img_url, price, description, coffee_details

    def scrape(self):
        self.search()
        coffees = self.driver.find_elements_by_xpath('//div[@class="products-list"]//a')
        print(len(coffees))

        links = []
        for coffee in coffees:
            link = coffee.get_attribute('href')
            links.append(link)
            

        details = []
        for idx, link in enumerate(links):

            self.driver.get(link)
            

            img_url, price, description, coffee_details = self._get_coffee_details()

            if '.png' in img_url:
                ext = 'png'
            else:
                ext = 'jpg'
            self.download_file(img_url, f'data/pictures/c2/kawa_{idx}.{ext}')

            detail = {
                'img_url' : img_url,
                'price' : price,
                'coffee_details' : coffee_details,
                # 'process' : process,
                # 'grind_types' : grind_types,
                # 'flavor' : flavor,
                # 'roast' : roast,
                'description' : description
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


scraper2 = CoffeeScraper2()
scraper2.scrape()
