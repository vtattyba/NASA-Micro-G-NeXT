import pyautogui as mouse
import webbrowser
from selenium import webdriver
import time
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

url = 'http://192.168.4.1:8081/compass.html'
browser = webdriver.Chrome()
browser.get(url)
browser.implicitly_wait(30)
time.sleep(9)
# need to collect at least 10 degrees and confirm the avg
degree = browser.find_element_by_id('doa').text


print(degree)
browser.quit()


if degree > 180:
	os.system("python3 servo_left.py")
	
else:
	os.system("python3 servo_right.py")

time.sleep(1)
os.system("pigs s 4 1300")
time.sleep(7)
os.system("python3 servo_straight.py")

