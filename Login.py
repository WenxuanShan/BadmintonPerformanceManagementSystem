#Login
from tkinter import *
import math
from tkinter import messagebox

master = Tk()

master.title("Badminton Performance Management - User Identity")
master.geometry("450x300")
master.configure(background = "light blue")
master.resizable(False,False)

def login():
    print("Login")

#Labels
loginL = Label(master,text = "Login",
              padx=20,pady=20,bg="light blue")
loginL.place(x=225,y=50,anchor="center")
userNameL = Label(master,text = "User Name",
                 padx=20,pady=20,bg="light blue")
userNameL.place(x=115,y=100,anchor="e")
passwordL = Label(master,text = "Password",
                 padx=20,pady=20,bg="light blue")
passwordL.place(x=115,y=150,anchor="e")

#Entries
userNameEnt = Entry(master,bg="light blue",relief=RAISED)
userNameEnt.place(x=225,y=100,anchor="center")
passwordEnt = Entry(master,bg="light blue",relief=RAISED)
passwordEnt.place(x=225,y=150,anchor="center")

#Buttons
loginBtn = Button(master,text = "Login",command = login)
loginBtn.place(x=225,y=200,anchor="center")

master.mainloop()