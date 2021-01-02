import lcddriver
import time

class Lcd:
    display = lcddriver.lcd()
    
    def lcd_password(self,psw):
        self.display.lcd_display_string("Password:", 1)
        self.display.lcd_display_string(psw, 2) 
    
    def lcd_password_result(self,msg):
        self.long_string(msg, 1)
        time.sleep(3)
        
    def clean_lcd(self):
        self.display.lcd_clear()                               

    def long_string(self, text = '', num_line = 1, num_cols = 16):
        if(len(text) > num_cols):
            self.display.lcd_display_string(text[:num_cols],num_line)
            time.sleep(1)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i+num_cols]
                self.display.lcd_display_string(text_to_print,num_line)
                time.sleep(0.2)
            time.sleep(1)
        else:
            self.display.lcd_display_string(text,num_line)

    # 0 Normal Display
    # 1 Scrolling Display
    # 2 Black Light Display
    def my_display(self, msg1, msg2, flag=0):
        while True:
            try:
                #print("Writing to display")
                if flag == 0:
                    self.display.lcd_display_string(msg1, 1) 
                    self.display.lcd_display_string(msg2, 2)
                    #time.sleep(2)                                     
                    #self.display.lcd_clear()                               
                    #time.sleep(2)
                elif flag == 1:
                    self.long_string(msg1 + " " + msg2, 1)
                    time.sleep(2)
                    self.display.lcd_clear()                               
                    self.long_string(msg1 + " " + msg2, 2)
                    time.sleep(2)
                    self.display.lcd_clear() 
                elif flag == 2:
                    self.display.lcd_backlight(1)                         
                    time.sleep(0.5)                                   
                    self.display.lcd_backlight(0)                          
                    time.sleep(0.5)                                   
                    self.display.lcd_backlight(1)                          
                    time.sleep(1)                                     
                    self.display.lcd_display_string(msg1, 1)   
                    self.display.lcd_display_string(msg2, 2)   
                    time.sleep(2)                                     
                    self.display.lcd_backlight(0)                          
                    time.sleep(0.5)                                   
                    self.display.lcd_backlight(1)                          
                    time.sleep(0.5)                                   
                    self.display.lcd_backlight(0)                          
                    time.sleep(0.5)                                   
                    self.display.lcd_backlight(1)                          
                    time.sleep(2)                                     
                    self.display.lcd_clear()                               
                    time.sleep(1)                                     
                    self.display.lcd_backlight(0)                          
                    time.sleep(1.5)
            except KeyboardInterrupt:
                print("Cleaning up!")
                self.display.lcd_clear()
                self.display.lcd_backlight(1)
                break
