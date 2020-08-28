import pyautogui as mouse
import webbrowser
from selenium import webdriver
import time

class SDR: 
	def __init__(self):
		print('initializing SDR...')
		'''
		webbrowser.open('http://192.168.4.1:8080/init', new=2)
		time.sleep(1)
		mouse.click(920,117)
		time.sleep(2)
		mouse.click(360,198)
		time.sleep(2)
		mouse.click(406,215)
		time.sleep(2)
		mouse.click(470,445)
		time.sleep(30)
		'''
		print('DONE')

	def check_SDR(self):
		url = 'http://192.168.4.1:8081/compass.html'
		browser = webdriver.Chrome()
		browser.get(url)
		browser.implicitly_wait(30)
		time.sleep(9)
		# need to collect at least 10 degrees and confirm the avg
		degree = browser.find_element_by_id('doa').text
		browser.quit()
		degree = int(degree.split()[2])
		# potentially change the degree threshold 
		if degree > 180:
			return -1
		else:
			return 1
			

