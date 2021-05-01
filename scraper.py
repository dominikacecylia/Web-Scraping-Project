""" In the web browser use CTRL SHIFT C to open the inspect mode which allows you to inspect elements
by placing cursos over them directly"""

#%%
from selenium import webdriver #Allows you to launch/initialise a browser.
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get('https://www.coffeedesk.pl/kawa/#close')
actions = ActionChains(driver)
# sth to accept cookies test it 
driver.find_element_by_xpath('//button[contains(@id, "onetrust-accept-btn-handler")]').click()
actions.send_keys(Keys.PAGE_DOWN).perform()
actions.send_keys(Keys.PAGE_DOWN).perform()
time.sleep(15)
next_button = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[6]/div/div/ul/li[7]/a').click()

# url = 'https://brewed.online/collections/all?sort-by=manual'
# driver.get(url)

#%%
def scroll(x=0, y=10000):
    driver.execute_script(f'window.scrollBy({x}, {y})')

#%%
# products = driver.find_elements_by_xpath('/html/body/main/collection/div/div/div[2]/products/ul/li') #gets all products info

# for prod in products:
#     img = prod.find_element_by_xpath('product-thumbnail/div/a/div[1]/div/img').get_attribute('src')
#     price = prod.find_element_by_xpath('product-thumbnail/div/a/div[2]/div/div[1]/div/div[1]/div')
#     print(img)
#     print()
#     print(price.text)







