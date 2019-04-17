#################################################################
# Name: Clark Foster, Jacob Anthon, Juwan Joseph
# Date: 16 May 2019
# Description: Proximity Alarm
#################################################################
from Tkinter import *
import RPi.GPIO as GPIO
from time import sleep, time


#constants are always in all caps:
DEBUG = False      #debug mode?
SETTLE_TIME = 2      # seconds to let the sensor settle
CALIBRATIONS = 5      #number of calibration measures to take
CALIBRATION_DELAY = 1   #seconds to delay in between calibration measurements
TRIGGER_TIME = 0.00001   #seconds needed to trigger sensor (to get measurement)
SPEED_OF_SOUND = 343      #speed of sound in m/s

#set the RPi to the Broadcom pin layout
GPIO.setmode(GPIO.BCM)

#GPIO pins
TRIG = 18            #sensor's TRIG pin
ECHO = 27           # sensor's ECHO pin

GPIO.setup(TRIG, GPIO.OUT) #TRIG is an output
GPIO.setup(ECHO, GPIO.IN)   #ECHO is an input



# the main GUI
class MainGUI(Frame):
    # the constructor
    def __init__(self, parent):
            Frame.__init__(self, parent, bg="white")
            parent.geometry("400x200+50+50")
#           parent.attributes("-fullscreen", True)
            self.setupGUI()

    
        # sets up the GUI
    def setupGUI(self):
            self.display = Label(self, text="", anchor=E, bg="white", height=1, font=("TexGyreAdventor", 35))
            # put it in the top row, spanning across all four
            # columns; and expand it on all four sides
            self.display.grid(row=0, column=0, columnspan=4,sticky=E+W+N+S)
            # the button layout
            # 1 2 3
            # 4 5 6
            # 7 8 9
            # < 0 E
            # configure the rows and columns of the Frame to adjust
            # to the window
            # there are 5 rows (0 through 4)
            for row in range(5):
                Grid.rowconfigure(self, row, weight=1)
            # there are 3 columns (0 through 2)
            for col in range(3):
                Grid.columnconfigure(self, col, weight=1)
            # the first row
            # 1
            # first, fetch and store the image
            # to work best on the RPi, images should be 115x115
            # pixels
            # otherwise, may need to add .subsample(n)


            img = PhotoImage(file="images/1.gif")
            # next, create the button (white background, no border,
            # no highlighting, no color when clicked)
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("1"))
             # set the button's image
            button.image = img
             # put the button in its proper row and column
            button.grid(row=1, column=0, sticky=N+S+E+W)
             
             # the same is done for the rest of the buttons
             # 2
            img = PhotoImage(file="images/2.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("2"))
            button.image = img
            button.grid(row=1, column=1, sticky=N+S+E+W)

             # 3
            img = PhotoImage(file="images/3.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("3"))
            button.image = img
            button.grid(row=1, column=2, sticky=N+S+E+W)
             
             # the second row
             # 4
            img = PhotoImage(file="images/4.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("4"))
            button.image = img
            button.grid(row=2, column=0, sticky=N+S+E+W)

             
             # 5
            img = PhotoImage(file="images/5.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("5"))
            button.image = img
            button.grid(row=2, column=1, sticky=N+S+E+W)

             # 6
            img = PhotoImage(file="images/6.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("6"))
            button.image = img
            button.grid(row=2, column=2, sticky=N+S+E+W)

             # the third row
             # 7
            img = PhotoImage(file="images/7.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("7"))
            button.image = img
            button.grid(row=3, column=0, sticky=N+S+E+W)

             # 8
            img = PhotoImage(file="images/8.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("8"))
            button.image = img
            button.grid(row=3, column=1, sticky=N+S+E+W)

            # 9
            img = PhotoImage(file="images/9.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("9"))
            button.image = img
            button.grid(row=3, column=2, sticky=N+S+E+W)

            # the fourth row
            # backspace
            img = PhotoImage(file="images/bak.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("back"))
            button.image = img
            button.grid(row=4, column=0, sticky=N+S+E+W)

             # 0
            img = PhotoImage(file="images/0.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("0"))
            button.image = img
            button.grid(row=4, column=1, sticky=N+S+E+W)

             # =
            img = PhotoImage(file="images/eql.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("="))
            button.image = img
            button.grid(row=4, column=2, sticky=N+S+E+W)

            #5th row
             # AC
            img = PhotoImage(file="images/clr.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("AC"))
            button.image = img
            button.grid(row=5, column=0, sticky=N+S+E+W)

            # *
            img = PhotoImage(file="images/mul.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("*"))
            button.image = img
            button.grid(row=5, column=1, sticky=N+S+E+W)

            # **
            img = PhotoImage(file="images/pow.gif")
            button = Button(self, bg="white", image=img, borderwidth=0, highlightthickness=0, activebackground="white", command=lambda: self.process("**"))
            button.image = img
            button.grid(row=5, column=2, sticky=N+S+E+W)

            self.shouldClear = False
            self.codeSetMode = False
            # pack the GUI
            self.pack(fill=BOTH, expand=1)


    #code set system:
    def program(self):
        self.display["text"] = "Enter 6-digits, Press ="
        self.shouldClear = True

    def run(self):
        if (len(self.display["text"]) != 6):
            self.display["text"] = "Error: Enter 6 dgts"
            self.shouldClear = True
        else:
            self.run2() 
            
    def run2(self):
        global code1
        code1= self.display["text"]
        self.display["text"] = "Re-Enter, Press **"
        self.shouldClear = True
        
    def run3(self):
        self.codeSetMode = False
        if (self.display["text"] == code1):
            self.display["text"] = "Code Stored"
            self.shouldClear = True
        else:
            self.display["text"] = "Error: Enter Code"
            self.shouldClear = True

    #arming system        
    def arm(self):
        if (self.display["text"] == code1):
            self.display["text"] = "System Armed"

    #alert intruder
    def alert(self):
        self.display["text"] = "ALERT! INTRUDER"
    
    # processes button presses
    def process(self, button):
        #shouldClear = True clears the display when button pressed, see below
        if self.shouldClear == True:
            self.display["text"] = ""
            self.shouldClear = False
        # AC clears the display
        if (button == "AC"):
            # clear the display
            self.display["text"] = ""
        # Program desired 6-digit code
        elif (button == "*"):
            self.codeSetMode = True
            self.program()
        elif (button == "="):
            if (self.codeSetMode == True):
                self.run()
                self.codeSetMode = False
            else:
                self.arm()
        elif (button == "**"):
            self.run3()
            
        
    
            # = starts an evaluation of whatever is on the display
       # back clears the last element in the display
        elif (button == "back"):
            self.display["text"] = self.display["text"][:-1]
        
                
            
            #clear the error or old solution when type new button
            self.shouldClear = True
        #limit display to 14 characters by making button = "" which is null
        elif (len(self.display["text"]) > 13):
              button = ""
        else:
            self.display["text"] += button




# MAKE THIS PRINT AND INTERACT WITH GUI

#Calibrates the sensor
#technically, it returns a correction factor to use in our calculations
def calibrate():
    print "Calibrating..."
    #prompt the user for an object'sknown distance
    print "-Place the sensor a measured distance away from an object."
    known_distance = input("What is the measured distance (cm)?")
    #measure the distance to the object with the sensor
    #do this several times and get an average
    print "-Getting calibration measurements..."
    distance_avg = 0
    for i in range(CALIBRATIONS):
        distance = getDistance()
        if (DEBUG):
            print "---Got {}cm".format(distance)
        #keep a running sum
        distance_avg += distance
        #delay a short time before using the sensor again.
        sleep(CALIBRATION_DELAY)
    #calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print "--Average is {} cm".format(distance_avg)
    #calculate the correction factor
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print "--Correction factor is {}".format(correction_factor)
    print "Done."
    print #puts a blank line afterwards

    return correction_factor




#uses the senstor to claculate the distacne to an object
def getDistance():
    #trigger the sensor by setting it high for a short time and then lsetting it to low
    GPIO.output(TRIG, GPIO.HIGH)
    sleep(TRIGGER_TIME)
    GPIO.output(TRIG, GPIO.LOW)

    #wait for the ECHO pin to read high
    # once th ECHO pin is high, the start time is set
    #once the ECHO pin is low again, the end time is set
    while (GPIO.input(ECHO) == GPIO.LOW):
        start = time()
    while (GPIO.input(ECHO) == GPIO.HIGH):
         end = time()
    #calculate the duration that the ECHO pin was high
    # this is how long the pulse took to get form the sensor to the object and back again
    duration = end - start
    #calculate the total distance that pulse traveled by
    # factoring in the speed of sound(m/s)
    distance = duration * SPEED_OF_SOUND
    #the distance form the sensor to the object is half of the total distance traveled
    distance /= 2
    #convert from meters to centimeres
    distance *= 100
    return distance

        
        
##############################
# the main part of the program
##############################
# create the window
window = Tk()
# set the window title
window.title("Proximity Alarm")
# generate the GUI
p = MainGUI(window)
# display the GUI and wait for user interaction
window.mainloop()







# Put all of this stuff below into the functions of the GUI



#first, allow the sensor to settle for a bit
#print "Waiting for sensor to settle ({}s)...".format(SETTLE_TIME)
GPIO.output(TRIG, GPIO.LOW)
sleep(SETTLE_TIME)

#next, calibrate the sensor
correction_factor = calibrate()

#then, measure
raw_input("Press enter to begin...")
print "Getting measurements:"
#now start building a list, start by defining it:
distances = []
while (True):
    #get the distance to an object and correct it iwth the correction factor
    print "-Measuring..."
    distance = getDistance() * correction_factor
    sleep(.25)
    #and round to four decimal places
    distance = round(distance, 4)
    distances.append(distance)
    #display the distance measure/calculated
    print "--Distance measured: {}cm".format(distance)
    if (distance <= 7):
      #  MainGUI.self.alert()
        print "ALERT: INTRUDER!!"
        break

    
# leave the stuff alone below this line this remove this comment
###############################################

#finally, cleanup the GPIO pins
print "Done."
GPIO.cleanup()






