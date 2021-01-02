from Components.MicroServo import micro_servo as ms
from Components.PIR_MotionSensor import motion as m
from Components.Keypad import keypad
import lcd
import time
import threading

lcd = lcd.Lcd()
kp= keypad.Keypad()

thread = threading.Thread(target=kp.start, args=())
thread.start()

start = False
lcd_flag = False
empty = True

ms.change_center()

while True:
    try:
        if m.start():
            for sec in range(50): # Wait 20 secondes
                if not kp.getInput() == "":
                    start = True
                if start:
                    lcd_flag = True
                    
                lcd.lcd_password(kp.getInput())
                
                if not kp.getInput() and lcd_flag:
                    start = False
                    lcd_flag = False
                    lcd.clean_lcd()
                    if kp.is_correct() == 1:
                        lcd.lcd_password_result("Correct Password")
                        ms.change_min()
                        time.sleep(5)
                        ms.change_center()
                        lcd.clean_lcd()
                        break
                    if kp.is_correct() == 0:
                        lcd.lcd_password_result("Incorrect Password")
                    lcd.clean_lcd()
                time.sleep(0.4)
            lcd.clean_lcd()
    except KeyboardInterrupt:
        lcd.clean_lcd()
        thread.join()
        break
