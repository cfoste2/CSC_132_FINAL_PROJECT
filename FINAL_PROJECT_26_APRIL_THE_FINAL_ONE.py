#############################################################################################################################################
# Names: Clark Foster, Jacob Anthon, Juwan Joseph
# Date: 26 April 2019
# Description: Proximity Alarm System
#############################################################################################################################################

#import out Tk interface and fonts
from Tkinter import *
import tkFont

#import other necessary libraries
import RPi.GPIO as GPIO
import time
import datetime
import picamera
import pygame

#initialize pygame library
pygame.init()

#setup our siren sound using pygame mixer
siren = pygame.mixer.Sound("siren.wav")

#setup the class for our Promiximity Alarm
class ProxAlarm(Frame):
    #our constructor
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master

    #method to setup our GUI
    def setupGUI(self):

        #setup a variable for our font for ease of use
        helv36 = tkFont.Font(family='Helvetica', size=9, weight=tkFont.BOLD)

        #button for number 1
        b1 = Button(self.master, text = "1", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("1"))
        b1.grid(row=0, column = 0)

        #button for number 2
        b2 = Button(self.master, text= "2", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("2"))
        b2.grid(row=0, column = 1)

        #button for number 3
        b3 = Button(self.master, text= "3", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("3"))
        b3.grid(row=0, column = 2)

        #button for number 4
        b4 = Button(self.master, text= "4", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("4"))
        b4.grid(row=1, column = 0)

        #button for number 5
        b5 = Button(self.master, text= "5", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("5"))
        b5.grid(row=1, column = 1)

        #button for number 6
        b6 = Button(self.master, text= "6", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("6"))
        b6.grid(row=1, column = 2)

        #button for number 7
        b7 = Button(self.master, text= "7", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("7"))
        b7.grid(row=2, column = 0)

        #button for number 8
        b8 = Button(self.master, text= "8", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("8"))
        b8.grid(row=2, column = 1)

        #button for number 9
        b9 = Button(self.master, text= "9", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("9"))
        b9.grid(row=2, column = 2)

        #button for number 0
        b0 = Button(self.master, text= "0", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("0"))
        b0.grid(row=3, column = 1)

        #button for backspace
        backspace = Button(self.master, text="<-", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("back"))
        backspace.grid(row=3, column=0)

        #button for AC
        all_clear = Button(self.master, text="AC", fg="green", bg="black", font=helv36, height = 5, width = 10, command=lambda: self.process("AC"))
        all_clear.grid(row=3, column =2)

        #this sets up the window that supplies messages to user
        self.text_messages = Label(self.master, bg="white", font=helv36, borderwidth=2, relief="groove", height = 5, width = 10)
        self.text_messages.grid(row=0, column=3, rowspan=3, columnspan=2, sticky=W+E+N+S,)

        #this is the label for user input
        input_label = Label(self.master, text="User Input", font=helv36, height = 5, width = 10, anchor=E)
        input_label.grid(row=3, column=3)

        #user input is displayed through this
        self.user_input = Label(self.master, bg="white", borderwidth=2, relief="groove", width=10, text = "", anchor=E)
        self.user_input.grid(row=3, column=4)

        #this button arms the prox alarm
        arm_button = Button(self.master, text= "ARM/DISARM", height = 1, width = 11, command=lambda: self.process("arm"))
        arm_button.grid(row=3, column=4, sticky=S)

        #this button sets the code
        code_set = Button(self.master, text= "CODE SET", height = 1, width = 11, command=lambda: self.process("set"))
        code_set.grid(row=3, column=4, sticky=N)

        #Boolean values
        self.shouldClear = False
        self.codeSetMode = False
        self.armed = False
        self.alarmGoingOff = False

        #Intro screen
        self.text_messages["text"] = "Enter 6-digit code \nand press CODE SET button\n to set code"

        # grn_LED is illuminated when not armed
        GPIO.output(grn_LED, True)

            
    # processes button presses
    def process(self, button):
        
        #shouldClear = True clears the display when button pressed, see below
        if self.shouldClear == True:
            self.user_input["text"] = ""
            self.shouldClear = False
        # AC clears the display
        
        elif (button == "AC"):
            # clear the display
            self.user_input["text"] = ""
            
        #prevents user from entering for than 7 characters 
        elif (len(self.user_input["text"]) > 6) and (button != "set") and (button != "arm"):
            button = ""

       # back clears the last element in the display
        elif (button == "back"):
            self.user_input["text"] = self.user_input["text"][:-1]
            
        #set button
        elif (button == "set"):
            self.codeSetMode = True
            # take us to the program method after pressing code set button
            self.program()

        #arm button
        elif (button == "arm"):
            if (self.alarmGoingOff == True) and (self.user_input["text"] == code1):
                # if our alarm is going off and we have entered
                # the appropriate code, then red light, siren sound,
                # and camera will shut off
                GPIO.output(red_LED, False)
                camera.stop_preview()
                camera.stop_recording()
                pygame.mixer.pause()
                #clean up our GPIO
                GPIO.cleanup()
                #go to next function and alter our text message to user
                self.text_messages.after(1, self.pir6)
            else:
                # if alarm is not going off then we are trying to arm it
                # when we press the arm/disarm button 
                self.arm()
                
        else:
            # adds button characters to the display
            self.user_input["text"] += button


    # this method ensures that input is 6 digits and gives error message if it does
    def program(self):
        # range check 6-digits entered
        if (len(self.user_input["text"]) != 6):
            # display error message if more or less than 6 digits entered
            self.text_messages["text"] = "Error: Enter 6 digits\n and try again"
            self.shouldClear = True
        else:
            # if correct number of digits (6) were enterd, procede with
            # program sequence
            self.program2()

    # this method is ran if the user entered 6 digits
    def program2(self):
        # global variable code 1 will be used to store our user's code
        global code1
        code1= self.user_input["text"]
        #display to user when code is stored:
        self.text_messages["text"] = "Code stored. Enter\n code again and\n press ARM button to\n arm Proximity Alarm"
        # when code is stored, we clear the display:
        self.user_input["text"] = ""
        self.shouldClear = True

    # this method confirms that the user entered the correct code to arm the alarm and then activates the sequence to arm the alarm
    def arm(self):
        # check to see if user entry matches pre-stored code
        if (self.user_input["text"] == code1):
            # let user know that arming sequence has begun
            self.text_messages["text"] = "Arming Sequence\n Initiating..."
            # pause and then go to next part of arming sequence
            self.text_messages.after(2000, self.pir)
        else:
            # if user entered incorrect code, then give them an error message
            self.text_messages["text"] = "Invalid Entry.\n Try again." 

    def pir(self):
        #let the passive infrared sensor settle
        self.text_messages["text"] = "Initializing PIR..."
        # go to next step in arming sequence
        self.text_messages.after(2000, self.pir2)

    def pir2(self):
        # arming sequence is complete, we let the user know and
        # LED switches from green to yellow
        self.text_messages["text"] = "System Armed"
        GPIO.output(grn_LED, False)
        GPIO.output(ylw_LED, True)
        self.user_input.after(1, self.pir3)
        self.text_messages.after(1, self.pir3)

    def pir3(self):
        # clear user input label
        self.user_input["text"] = " "
        # go to armed mode
        self.text_messages.after(1, self.pir4)

    def pir4(self):
        self.armed = True
        # if the system is armed, then the following will occur:
        while ((True) and self.armed == True) :
            #if pir pin goes HIGH, this means that motion is detected
            if (GPIO.input(PIR) == True):
                # yellow LED goes out and red comes on
                GPIO.output(ylw_LED, False)
                GPIO.output(red_LED, True)
                # break the loop
                self.armed = False
                # turn on the alarm going off boolean
                self.alarmGoingOff = True
                # identify the file name for our video
                filename = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
                # show user what is being filmed
                camera.start_preview(alpha=200)
                # start filming
                camera.start_recording(filename)
                # go to next method in intruder sequence
                self.text_messages.after(1, self.pir5)
                
# /home/pi/Desktop/FINAL_PROJECT_ALARM/NEW_PROJECT/hello.h264

    def pir5(self):
        # let user know that intruder has been detected
        self.text_messages["text"] = "INTRUDER DETECTED!"
        # play siren sound until disarmed
        siren.play(-1)

    def pir6(self):
        # let user know that system has been disarmed and clear user input display
        self.text_messages["text"] = "System Disarmed.\nEnter 6-Digit\ncode to arm."
        self.alarmGoingOff = False
        self.user_input["text"] = ""

##################################################################################
##################################################################################
## MAIN PROGRAM ##################################################################
##################################################################################
        

#set GPIO to pin numbering
GPIO.setmode(GPIO.BCM)

# set camera variable to our picamera
camera = picamera.PiCamera()

#associate our motion sensor (PIR) and our LEDs with their respective GP pins
PIR = 4
red_LED = 5
grn_LED = 24
ylw_LED = 23

#setup Motion sensor as input
GPIO.setup(PIR, GPIO.IN)

#setup LEDs as output
GPIO.setup(red_LED, GPIO.OUT)
GPIO.setup(grn_LED, GPIO.OUT)
GPIO.setup(ylw_LED, GPIO.OUT)

#RUN THE GUI
window = Tk()
window.title("Proximity Alarm")
t = ProxAlarm(window)
t.setupGUI()
window.mainloop()

