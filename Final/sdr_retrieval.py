
from selenium import webdriver
import time

url = 'http://192.168.4.1:8081/compass.html'
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(30)
time.sleep(9)
degree = browser.find_element_by_id('doa').text
print(degree)
browser.quit()