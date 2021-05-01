from selenium import webdriver
from pprint import pprint
import json
import requests
# check out the one below for going down the page
# from selenium.webdriver import common.actions.ActionChains

class CoffeeScraper:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def search(self):
        self.driver.get('https://brewed.online/collections/all?sort-by=manual')
    
    def _get_coffee_details(self):
        # details = self.driver.find_elements_by_xpath('/html/body/main/collection/div/div/div[2]/products/ul/li')
        img_url = self.driver.find_element_by_xpath('//img').get_attribute('src')
        price = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/div[1]/div/span').text
        origin = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/ng-container/div/div[2]/div[2]/div/p').text
        print(img_url)
        print(price)
        print()
        return img_url, price, origin

    def scrape(self):
        self.search()
        products = self.driver.find_elements_by_xpath('/html/body/main/collection/div/div/div[2]/products/ul/li')

        links = []
        for product in products:
            link = product.find_element_by_tag_name('a').get_attribute('href')
            links.append(link)

        examples = []
        for idx, link in enumerate(links):

            self.driver.get(link)

            img_url, price, origin = self._get_coffee_details()

            if '.png' in img_url:
                ext = 'png'
            else:
                ext = 'jpg'
            self.download_file(img_url, f'data/product_{idx}.{ext}')

            example = {
                'img_url' : img_url,
                'price' : price,
                'origin' : origin
            }
            examples.append(example)

        with open('data/data.json', 'w') as f:
            json.dump(examples, f, indent=4)


    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')

    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)


scraper = CoffeeScraper()
scraper.scrape()
