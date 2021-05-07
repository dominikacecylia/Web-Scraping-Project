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
        img_url = self.driver.find_element_by_xpath('//img').get_attribute('src')
        price = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/div[1]/div/span').text
        origin = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/ng-container/div/div[2]/div[2]/div/p').text
        # weight = self.driver.find_element_by_xpath('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/product-form/product-form-selectors/div[2]/ng-container/ul/li[1]/div').text
        # grounds = self.driver.find_elements_by_xpath('//*[@id="productFormSelectors"]/div[1]/ng-container/div/ul/li')
        weight = self._get_details_with_possible_null('/html/body/main/div/div[2]/product-page-above-fold/div/div[2]/product-form/product-form-selectors/div[2]/ng-container/ul/li[1]/div')

        # ground_types = []
        # for ground in grounds:
        #     ground_type = ground.find_element_by_xpath('//*[@id="productFormSelectors"]/div[1]/ng-container/div/ul/li[1]/div').text
        #     ground_types.append(ground_type)

        # add weight and roast and any other such info
        # print(img_url)
        # print(price)
        # print()
        return img_url, price, origin, weight

    def scrape(self):
        self.search()
        coffees = self.driver.find_elements_by_xpath('/html/body/main/collection/div/div/div[2]/products/ul/li')

        links = []
        for coffee in coffees:
            link = coffee.find_element_by_tag_name('a').get_attribute('href')
            links.append(link)

        coffees = []
        for idx, link in enumerate(links):

            self.driver.get(link)

            img_url, price, origin, weight = self._get_coffee_details()

            # if '.png' in img_url:
            #     ext = 'png'
            # else:
            #     ext = 'jpg'
            # self.download_file(img_url, f'data/pictures/c1/coffee_{idx}.{ext}')

            coffee = {
                'img_url' : img_url,
                'price' : price,
                'origin' : origin,
                'weight' : weight
            }
            coffees.append(coffee)

        with open('data/test_brew.json', 'w') as f:
            json.dump(coffees, f, indent=4)


    def scroll(self, x=0, y=10000):
        self.driver.execute_script(f'window.scrollBy({x}, {y})')

    def download_file(self, src_url, local_destination):
        response = requests.get(src_url)
        with open(local_destination, 'wb+') as f:
            f.write(response.content)

    def _get_details_with_possible_null(self, xpath):
        try:
            text = self.driver.find_element_by_xpath(xpath).text
            return text
        except Exception:
            return None



scraper = CoffeeScraper()
scraper.scrape()
