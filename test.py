from selenium import webdriver
from pprint import pprint
import json
import requests


driver = webdriver.Chrome()
driver.get('https://brewed.online/products/blanca-rosa')

ground_button = driver.find_element_by_xpath('//*[@id="productFormSelectors"]/div[1]/ng-container/ul/li[2]/div')
driver.execute_script("arguments[0].click();", ground_button)

grind_types = []
grinds = driver.find_elements_by_xpath('//ul[@class="flex row-wrap align-center justify-left cell-l--s cell-r--s"]//li')      
for grind in grinds:
    grind_types.append(grind.text)
    # print(grind.text)        
print(grind_types)

process = driver.find_element_by_xpath('/html/body/main/div/product-details/ng-container/div/ul/li[2]/div/div[2]/p').text
print(process)