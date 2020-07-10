import time
import board
import digitalio
import busio
import math 
import adafruit_lis3dh
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6) 
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

while True:
    
    x, y, z = lis3dh.acceleration
    one = math.pow(x,2)
    two = math.pow(y,2)
    three = math.pow(z,2)
    summ = one + two + three
    sq = math.sqrt(summ)

    norm = (sq/9.81)

    print(str(norm) + "g")

    if norm >= 3:
        #time.sleep(1)
        print("MOTOR Trig")
        break

"""
lis3dh.set_tap(2, 60)
while True:
    if lis3dh.tapped:
        print("Tapped!")
        time.sleep(0.01)
        """