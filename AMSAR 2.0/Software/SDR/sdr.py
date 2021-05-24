import pyautogui as mouse
import webbrowser
from selenium import webdriver
import time

# this class is used to define the SDR module for retrieving the sensor readings. 
# it's to be used on the main pi. 
class SDR():
    def __init__(self, temp=True, min_confidence=30):
        self.temp = temp
        self.min_confidence = min_confidence
        
        print('initializing sdr..')
        url = 'http://192.168.4.1:8081/compass.html'
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.browser.implicitly_wait(30)
        time.sleep(10)
        return
    
    # function that gets data from the SDR and returns a direction 
    # inputs - None
    # outputs - direction suggested by sensor
    def get(self):
        if self.temp:
            return 'straight'
        
        direction = 0
        for i in range(20):
            degree = int(self.browser.find_element_by_id('doa').text.split()[2])        
            confidence = int(self.browser.find_element_by_id('conf').text.split()[2])
            print(degree, confidence)
            if confidence < self.min_confidence:
                continue
            direction = direction - 1 if degree < 0 else direction + 1
            #direction = direction - 1 if degree < 180 else direction + 1
            time.sleep(0.1)
        if direction < 0:
            return 'left'
        elif direction > 0:
            return 'right'
        else:
            return 'straight'
            
    # function that quits the SDR session    
    def quit(self):
        return self.browser.quit()
