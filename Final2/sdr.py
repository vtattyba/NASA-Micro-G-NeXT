import pyautogui as mouse
import webbrowser
from selenium import webdriver
import time

class SDR: 
	def __init__(self):
		print('Initializing SDR...')
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
		
		print('SDR Calibrated!')

	def check_SDR(self):
		url = 'http://192.168.4.1:8081/compass.html'
		browser = webdriver.Chrome()
		browser.get(url)
		browser.implicitly_wait(30)
		# need to collect at least 10 degrees and confirm the avg
		score_L = 0
		score_R = 0
		for i in range(20):
			degree = int((browser.find_element_by_id('doa').text).split()[2])
			if degree > 180:
				score_L += 1
			else: 
				score_R += 1
			time.sleep(0.01)
		browser.quit()
		# potentially change the degree threshold 
		if score_L > score_R:
			return 'L'
		else:
			return 'R'


