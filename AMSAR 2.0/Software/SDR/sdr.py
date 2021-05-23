import pyautogui as mouse
import webbrowser
from selenium import webdriver
import time

class SDR():
    def __init__(self):
        print('initializing sdr..')
        self.browser = webdriver.Chrome()
        self.browser.get('http://192.168.4.1:8081/compass.html')
        self.browser.implicity_wait(30)
        return
    
    def get(self, temp=True):
        if not temp:
            left, right = 0, 0
            for i in range(20):
                degree = int((browser.find_by_element_id('doa').text).split()[2])
                time.sleep(0.1)
                if degree > 180:
                    left += 1
                else:
                    right += 1
                time.sleep(0.01)
            return 'left' if left > right else 'right'
        else:
            return np.random.choice(['left', 'right'])
