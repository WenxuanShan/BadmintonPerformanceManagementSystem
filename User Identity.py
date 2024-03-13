from tkinter import *
import math
from tkinter import messagebox

master = Tk()

master.title("Badminton Performance Management - User Identity")
master.geometry("450x300")
master.configure(background = "light blue")
master.resizable(False,False)

def organizer():
    print("organizer")
    #pop up a login window for organizer
    
def player():
    print("player")
    #pop up a login window for player

def guest():
    print("guest")
    #pop up the main page

#Labels
userIdentity = Label(master,text = "Choose your user identity",
                     padx=20,pady=20,bg="light blue")
userIdentity.place(x=225,y=50, anchor = "center")

#Buttons
organizerBtn = Button(master,text = "Organizer",command = organizer)
organizerBtn.place(x=225,y=100, anchor = "center")
playerBtn = Button(master,text = "Player",command = player)
playerBtn.place(x=225, y=150, anchor = "center")
guestBtn = Button(master,text = "Guest",command = guest)
guestBtn.place(x=225, y=200, anchor = "center")

master.mainloop()