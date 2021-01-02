from gpiozero import MotionSensor, LED
import RPi.GPIO as GPIO
import time

pir = MotionSensor(4)
led = LED(17)
led.off()

def start():
    try:
        if pir.motion_detected:
            led.on()
            print("Motion Detected")
            time.sleep(1)
            return True
        else:
            led.off()
            return False
    except KeyboardInterrupt:
        led.off()
        print("\nApplication stopped!")
        return False
    
#while True:
#    if start():
#        print("Motion Detected")
#    else:
#        print("Motion Not Detected")
