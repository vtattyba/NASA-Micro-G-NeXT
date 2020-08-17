import RPi.GPIO as GPIO
import time
import pygame
import os

#os.system("sudo pigpiod")

GPIO.setwarnings(False)
servoPIN = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)
p.start(0)

pygame.init()

def servo (sleep, cycle):
    p.ChangeDutyCycle(cycle)
    time.sleep(sleep)
    return

def main():
    speed = 900
    angle = 6
    servo(.05, angle)
    pygame.display.set_mode((50,50))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if angle == 7.5 or angle == 6:
                        angle -= 1.5
                        print("LEFT")
                        servo(.05, angle)
                if event.key == pygame.K_RIGHT:
                     if angle == 4.5 or angle == 6:
                        angle += 1.5
                        print("RIGHT")
                        servo(.05, angle)
                if event.key == pygame.K_UP:
                    speed += 50
                    os.system("pigs s 4 {}".format(speed))
                    print("Current RPM {}".format(speed))
                if event.key == pygame.K_DOWN:
                    speed -= 50
                    os.system("pigs s 4 {}".format(speed))
                    print("Current RPM {}".format(speed))
                if event.key == pygame.K_i:
                    os.system("pigs s 4 1000")
                if event.key == pygame.K_q:
                    os.system("pigs s 4 1000")
                    os.system("pigs s 4 0")
                    p.stop()
                    GPIO.cleanup()
                    print("Shutting Down")
                    return
main()
