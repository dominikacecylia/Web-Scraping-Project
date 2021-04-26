""" In the web browser use CTRL SHIFT C to open the inspect mode which allows you to inspect elements
by placing cursos over them directly"""

#%%
from selenium import webdriver #Allows you to launch/initialise a browser.
from pprint import pprint

driver = webdriver.Chrome()
url = 'https://brewed.online/collections/all?sort-by=manual'
driver.get(url)

#%%
products = driver.find_elements_by_xpath('/html/body/main/collection/div/div/div[2]/products/ul/li') #gets all products info

for prod in products:
    print(prod.text)





# %%
driver.quit()