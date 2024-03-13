#Badminton Performance Management
from tkinter import *
import math
from tkinter import messagebox

master = Tk()

master.title("Badminton Performance Management")
master.geometry("600x500")
master.configure(background = "light blue")
master.resizable(True,True)

#Menubar
menubar = Menu(master)
master.config(menu = menubar)

#Leader Board
option1 = Menu(menubar)
menubar.add_cascade(label = "Leader Board", menu=option1)
#Players
option2 = Menu(menubar)
menubar.add_cascade(label = "Players", menu=option2)
#Matches
option3 = Menu(menubar)
menubar.add_cascade(label = "Matches", menu=option3)

###Organizer only
#Create Account
optionO1 = Menu(menubar)
menubar.add_cascade(label = "Create Account", menu=optionO1)
#Enter Data
optionO2 = Menu(menubar)
menubar.add_cascade(label = "Enter Data", menu=optionO2)

###Player only
#View Profile
optionP1 = Menu(menubar)
menubar.add_cascade(label = "View Profile", menu=optionP1)

###Guest only
#Login
optionG1 = Menu(menubar)
menubar.add_cascade(label = "Login", menu=optionG1)
optionG1.add_command(label = "Want to be an organizer?")
optionG1.add_command(label = "Want to be a player?")

#Info option
info = Menu(menubar) #Set of options under info option
menubar.add_cascade(label = "Info", menu=info)
info.add_command(label = "About") ###Don't need () after .aboutInfo ???
info.add_command(label = "Help")
info.add_separator()
info.add_command(label = "Setting")

master.mainloop()