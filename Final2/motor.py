import os
import time

# 0 = stop
# 1000 = rest
# 1250 = move

class Motor:
	def __init__(self):
		#os.system('sudo killall pigpiod')
		os.system("sudo pigpiod")
		os.system('pigs s 4 1000')
		time.sleep(2)
		
	def rpm(self, r):
		os.system('pigs s 4 ' + str(r))
		return
	def halt(self):
		os.system('pigs s 4 1000')
		return
	def quit(self):
		os.system('pigs s 4 1000')
		os.system('pigs s 4 0')
		os.system('sudo killall pigpiod')
		return
		
		
