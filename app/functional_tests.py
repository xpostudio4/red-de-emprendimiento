"""This file contains all the text related to how
the website should work."""
from selenium import webdriver


browser = webdriver.Firefox()
browser.get('http://localhost:8001')

assert 'Red Nacional de Emprendimiento' in browser.title

browser.quit()
