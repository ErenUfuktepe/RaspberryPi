import RPi.GPIO as GPIO
import threading
import time

class Keypad:
    
    L1 = 21
    L2 = 20
    L3 = 16
    L4 = 12

    C1 = 25
    C2 = 24
    C3 = 23
    C4 = 18

    R1 = ["1","2","3","A"]
    R2 = ["4","5","6","B"]
    R3 = ["7","8","9","C"]
    R4 = ["*","0","#","D"]

    keypadPressed = -1

    secretCode = "1234"
    input = ""
    
    result = 0
    
    def __init__(self):
        self.L1 = 21
        self.L2 = 20
        self.L3 = 16
        self.L4 = 12

    def is_correct(self):
        return self.result

    def keypadCallback(self, channel):
        if self.keypadPressed == -1:
            self.keypadPressed = channel

    def setAllLines(self, state):
        GPIO.output(self.L1, state)
        GPIO.output(self.L2, state)
        GPIO.output(self.L3, state)
        GPIO.output(self.L4, state)

    def checkSpecialKeys(self):
        pressed = False

        GPIO.output(self.L3, GPIO.HIGH)

        if (GPIO.input(self.C4) == 1):
            self.result = -1
            print("Input reset!");
            pressed = True

        GPIO.output(self.L3, GPIO.LOW)
        GPIO.output(self.L1, GPIO.HIGH)

        if (not pressed and GPIO.input(self.C4) == 1):
            if self.input == self.secretCode:
                self.result = 1
                print("Code correct!")
                # TODO: Unlock a door, turn a light on, etc.
            else:
                self.result = 0
                print("Incorrect code!")
                # TODO: Sound an alarm, send an email, etc.
            pressed = True

        GPIO.output(self.L3, GPIO.LOW)

        if pressed:
            self.input = ""

        return pressed

    def getInput(self):
        return self.input

    def readLine(self, line, characters):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            self.input = self.input + characters[0]
            self.end = characters[0]
        if(GPIO.input(self.C2) == 1):
            self.input = self.input + characters[1]
            self.end = characters[1]
        if(GPIO.input(self.C3) == 1):
            self.input = self.input + characters[2]
            self.end = characters[2]
        if(GPIO.input(self.C4) == 1):
            self.input = self.input + characters[3]
            self.end = characters[3]
        GPIO.output(line, GPIO.LOW)

    def start(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        
        GPIO.setup(self.L1, GPIO.OUT)
        GPIO.setup(self.L2, GPIO.OUT)
        GPIO.setup(self.L3, GPIO.OUT)
        GPIO.setup(self.L4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.C1, GPIO.RISING, callback=self.keypadCallback)
        GPIO.add_event_detect(self.C2, GPIO.RISING, callback=self.keypadCallback)
        GPIO.add_event_detect(self.C3, GPIO.RISING, callback=self.keypadCallback)
        GPIO.add_event_detect(self.C4, GPIO.RISING, callback=self.keypadCallback)

        try:
            while True:
                if self.keypadPressed != -1:
                    self.setAllLines(GPIO.HIGH)
                    if GPIO.input(self.keypadPressed) == 0:
                        self.keypadPressed = -1
                    else:
                        time.sleep(0.1)
                else:
                    if not self.checkSpecialKeys():
                        self.readLine(self.L1, self.R1)
                        self.readLine(self.L2, self.R2)
                        self.readLine(self.L3, self.R3)
                        self.readLine(self.L4, self.R4)
                        time.sleep(0.1)
                    else:
                        time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nApplication stopped!")
            
#kp=Keypad()
#thread = threading.Thread(target=kp.start, args=())
#thread.start()
#while True:
#    print(kp.getInput())