# MicroServo 99 (SG99)

import RPi.GPIO as GPIO
import time

MIN_DUTY = 2
MAX_DUTY = 13
CENTRE = MIN_DUTY + (MAX_DUTY - MIN_DUTY) / 2

servo_pin = 5
duty_cycle = CENTRE

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm_servo = GPIO.PWM(servo_pin, 50)
pwm_servo.start(duty_cycle)

def change_min():
    print("MIN")
    pwm_servo.ChangeDutyCycle(MIN_DUTY)

def change_max():
    print("MAX")
    pwm_servo.ChangeDutyCycle(MAX_DUTY)

def change_center():
    print("CEN")
    pwm_servo.ChangeDutyCycle(CENTRE)
        
def close():
    pwm_servo.ChangeDutyCycle(CENTRE)
    GPIO.cleanup()

#change_center()
#time.sleep(2)
#close()