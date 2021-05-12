from selenium import webdriver
from pprint import pprint
import json
import requests
import time

"""Try:
    - try and catch for exception of lacking details on particular products 
"""

class CoffeeScraper2:
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.already_visited_links = [] 
        
        with open('data/data_pl_test.json', 'r', encoding='utf-8') as json_file:
            data_dicts = json.load(json_file)
        self.already_visited_links = [dd['unique_id'] for dd in data_dicts] 
        
       # TODO: try catch for empty file

    def search(self, url):
        self.driver.get(url)
        
    
    def _get_coffee_details(self):
        img_url = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]//img').get_attribute('src')
        price = self.driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[1]/span[3]').text
        description = [desc.text for desc in self.driver.find_elements_by_xpath('//*[@id="description"]/span/div[1]')]

        self._click_on_button('//*[@id="tabs"]/ul/li[2]/a/span')
        
        coffee_details = self._get_details_in_table('//*[@id="attributes"]/table/tbody')
        return img_url, price, description, coffee_details

    def scrape(self):
        # urls = ('https://www.coffeedesk.pl/kawa/filters/on-page/120/0/','https://www.coffeedesk.pl/kawa/filters/on-page/120/1/')
        urls = ('https://www.coffeedesk.pl/kawa/filters/on-page/120/2/','https://www.coffeedesk.pl/kawa/filters/on-page/120/3/',
        'https://www.coffeedesk.pl/kawa/filters/on-page/120/4/','https://www.coffeedesk.pl/kawa/filters/on-page/120/5/',
        'https://www.coffeedesk.pl/kawa/filters/on-page/120/6/','https://www.coffeedesk.pl/kawa/filters/on-page/120/7/')

        for url in urls: #TODO: redo the links and urls as this is the duplicate source
            
            if url != 'https://www.coffeedesk.pl/product/17414/Audun-Coffee-Drip-No-1-%3E75Procent-Rwanda-Kopakama-1Kg': # TODO: remove this link from urls
                self.search(url)

            coffees = self.driver.find_elements_by_xpath('//div[@class="products-list"]//a')
            print(len(coffees))

            links = [coffee.get_attribute('href') for coffee in coffees]                 

            details = []
            for idx, link in enumerate(links):
                if link in self.already_visited_links:
                    print("Already visited this link")
                    continue
                else:
                    self.already_visited_links.append(link)
                
                if link != 'https://www.coffeedesk.pl/product/17414/Audun-Coffee-Drip-No-1-%3E75Procent-Rwanda-Kopakama-1Kg':
                    self.driver.get(link)
                img_url, price, description, coffee_details = self._get_coffee_details()

                if '.png' in img_url:
                    ext = 'png'
                else:
                    ext = 'jpg'
                idx = idx+240
                self._download_file(img_url, f'data/pictures/c2/kawa_{idx}.{ext}')

                detail = {
                    'unique_id' : link,
                    'img_url' : img_url,
                    'price' : price,
                    'description' : description,
                    **coffee_details
                }

                details.append(detail)

            with open('data/data_pl_test.json', 'w') as f:
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
        try:
            details = self.driver.find_element_by_xpath(xpath)
            rows = details.find_elements_by_tag_name('tr')
            all_details = {}
            for row in rows:
                key, value = [e.text for e in row.find_elements_by_tag_name('td')] # TODO: try prints, try doule nesting maybe
                all_details[key] = value
            return all_details
        except Exception:
            return {'Empty' : None}






scraper2 = CoffeeScraper2()
scraper2.scrape()
