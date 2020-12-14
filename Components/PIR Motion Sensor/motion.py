from gpiozero import MotionSensor, LED
import RPi.GPIO as GPIO
import time

pir = MotionSensor(4)
led = LED(17)
led.off()

try:
	while True:
		if pir.motion_detected:
			led.on()
			print("Motion Detected")
			time.sleep(5)
		else:
			led.off()
except KeyboardInterrupt:
    print("\nApplication stopped!")
