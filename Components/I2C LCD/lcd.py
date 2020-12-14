import lcddriver
import time

display = lcddriver.lcd()


def long_string(display, text = '', num_line = 1, num_cols = 16):
    if(len(text) > num_cols):
        display.lcd_display_string(text[:num_cols],num_line)
        time.sleep(1)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print,num_line)
            time.sleep(0.2)
        time.sleep(1)
    else:
        display.lcd_display_string(text,num_line)

# 0 Normal Display
# 1 Scrolling Display
# 2 Black Light Display
def my_display(msg1, msg2, flag=0):
    print("Writing to display")
    if flag == 0:
        display.lcd_display_string(msg1, 1) 
        display.lcd_display_string(msg2, 2)
        time.sleep(2)                                     
        display.lcd_clear()                               
        time.sleep(2)
    elif flag == 1:
        long_string(display, msg1 + " " + msg2, 1)
        time.sleep(2)
        display.lcd_clear()                               
        long_string(display, msg1 + " " + msg2, 2)
        time.sleep(2)
        display.lcd_clear() 
    elif flag == 2:
        display.lcd_backlight(1)                         
        time.sleep(0.5)                                   
        display.lcd_backlight(0)                          
        time.sleep(0.5)                                   
        display.lcd_backlight(1)                          
        time.sleep(1)                                     
        display.lcd_display_string(msg1, 1)   
        display.lcd_display_string(msg2, 2)   
        time.sleep(2)                                     
        display.lcd_backlight(0)                          
        time.sleep(0.5)                                   
        display.lcd_backlight(1)                          
        time.sleep(0.5)                                   
        display.lcd_backlight(0)                          
        time.sleep(0.5)                                   
        display.lcd_backlight(1)                          
        time.sleep(2)                                     
        display.lcd_clear()                               
        time.sleep(1)                                     
        display.lcd_backlight(0)                          
        time.sleep(1.5)

while True:
    try:
        my_display("Wait for it!","LEGENDARY!",0)
    except KeyboardInterrupt:
        print("Cleaning up!")
        display.lcd_clear()
        display.lcd_backlight(1)
        break
