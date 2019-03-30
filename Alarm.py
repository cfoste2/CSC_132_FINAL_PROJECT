#################################################################
# Name:Clark Foster
# Date:6 Feb 2019
# Description: The Reckoner
#################################################################
from Tkinter import *
# the main GUI
class MainGUI(Frame):
    # the constructor
    def __init__(self, parent):
            Frame.__init__(self, parent, bg="white")
            parent.attributes("-fullscreen", True)
            self.setupGUI()
    
        # sets up the GUI
    def setupGUI(self):
            # the calculator uses the TexGyreAdventor font (see
            # https://www.fontsquirrel.com/fonts/tex-gyre-adventor)
            # on most Linux system, simply double-click the font
            # files and install them
            # on the RPi, copy them to /usr/local/share/fonts (with
            # sudo):
            # sudo cp tex*.otf /usr/local/share/fonts
            # then reboot
            # the display
            # right-align text in the display; and set its
            # background to white, its height to 2 characters, and
            # its font to 50 point TexGyreAdventor
            self.display = Label(self, text="", anchor=E, bg="white", height=1, font=("TexGyreAdventor", 45))
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

            # pack the GUI
            self.pack(fill=BOTH, expand=1)


    #arming system:
    def program(self):
        self.display["text"] = "Entr 6-dgt, Press ="
        self.shouldClear = True

    def run(self):
        if (len(self.display["text"]) != 6):
            self.display["text"] = "Error: Entr 6 dgts"
            self.shouldClear = True
        else:
            self.run2() 
            
    def run2(self):
        code1 = self.display["text"]
        self.display["text"] = "Re-Entr, Press **"
        self.shouldClear = True
        return code1

        
    def run3(self):
        if (self.display["text"] == self.run2()):
            self.display["text"] = "Code Stored"
        else:
            self.display["text"] = "Error: Enter Code"
            
    
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
            self.program()
        elif (button == "="):
            self.run()
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

        
        
##############################
# the main part of the program
##############################
# create the window
window = Tk()
# set the window title
window.title("The Reckoner")
# generate the GUI
p = MainGUI(window)
# display the GUI and wait for user interaction
window.mainloop()

