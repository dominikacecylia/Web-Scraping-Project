""" In the web browser use CTRL SHIFT C to open the inspect mode which allows you to inspect elements
by placing cursos over them directly"""
#%%
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://brewed.online/collections/all?sort-by=manual')

#%%
