#Badminton Performance Management System Actual Code
from tkinter import *
from tkinter import ttk
import math
import random
from tkinter import messagebox
from tkcalendar import Calendar
import sqlite3
from sqlite3 import Error

###Using SQL in python - create connection, execute query, execute read query)
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


###Database Functions
#Select all organizations
def selectOrganizations(database):
    select_organizers = """
    SELECT * from organizations;
    """
    organizations = execute_read_query(create_connection(database), select_organizers)
    return organizations

#Select all users
def selectUsers(database):
    select_users = "SELECT * from users"
    users = execute_read_query(create_connection(database), select_users)
    return users

#Select all users that are organizer
def selectOrganizers(database):
    select_organizers = """
    SELECT * from users
    WHERE identity = 'organizer';
    """
    organizers = execute_read_query(create_connection(database), select_organizers)
    return organizers

#Select all users that are player
def selectPlayers(database):
    select_players = """
    SELECT * from users
    WHERE identity = 'player';
    """
    players = execute_read_query(create_connection(database), select_players)
    return players

#Count the number of players in the whole system
def countPlayers(database):
    count_players = """
    SELECT COUNT(*) FROM users
    WHERE identity = 'player';
    """
    numPlayers = execute_read_query(create_connection(database), count_players)
    return numPlayers[0][0]

#Find the userID given the username
def identifyID(database,username):
    identify_userID = """
    SELECT userID FROM users
    WHERE username = '{}';
    """.format(username)
    id = execute_read_query(create_connection(database), identify_userID)
    return id[0][0]

#Find the userID given the user's full name
def identifyID2(database,name):
    nameFull = name.split(" ")
    identify_userID2 = """
    SELECT * from players
    WHERE firstName = '{}' AND lastName = '{}';
    """.format(nameFull[0],nameFull[1])
    id = execute_read_query(create_connection(database), identify_userID2)
    return id[0][0]

#Find the organizationID given the username
def identifyOrganization(database,username):
    identify_organization = """
    SELECT organizationID FROM users
    WHERE username = '{}';
    """.format(username)
    org = execute_read_query(create_connection(database), identify_organization)
    return org[0][0]

#Find the organization name given the organizationID
def identifyOrganizationName(database,id):
    identify_organization_name = """
    SELECT organizationName FROM organizations
    WHERE organizationID = '{}';
    """.format(id)
    orgName = execute_read_query(create_connection(database), identify_organization_name)
    return orgName[0][0]

#Select the players in the organization, in the order of descending total score and then ascending last name
def orderPlayersOrg(database,org):
    order_players_org = """
    SELECT * from players
    INNER JOIN users ON players.userID = users.userID
    WHERE users.organizationID = '{}' AND users.identity = 'player'
    ORDER BY scoreAve DESC, lastName ASC;
    """.format(org)
    players = execute_read_query(create_connection(database), order_players_org)
    return players

#Select the players in the organization, in the order of ascending last name
def selectPlayersOrg(database,org):
    select_players_org = """
    SELECT * from players
    INNER JOIN users ON players.userID = users.userID
    WHERE users.organizationID = '{}' AND users.identity = 'player'
    ORDER BY lastName ASC;
    """.format(org)
    players = execute_read_query(create_connection(database), select_players_org)
    return players

#Select all players, in the order of descending total score and then ascending last name
def orderPlayersAll(database):
    order_players_all = """
    SELECT * from players
    INNER JOIN users ON players.userID = users.userID
    WHERE users.identity = 'player'
    ORDER BY scoreAve DESC, lastName ASC;
    """
    players = execute_read_query(create_connection(database), order_players_all)
    return players

#Select all players, in the order of ascending last name
def selectPlayersAll(database):
    select_players_all = """
    SELECT * from players
    INNER JOIN users ON players.userID = users.userID
    WHERE users.identity = 'player'
    ORDER BY lastName ASC;
    """
    players = execute_read_query(create_connection(database), select_players_all)
    return players

#Select the matches in the organization, in the order of descending match date
def selectMatchesOrg(database,org):
    select_matches_org = """
    SELECT * from matches
    INNER JOIN users AS u1 ON matches.player1ID = u1.userID
    INNER JOIN users AS u2 ON matches.player2ID = u2.userID
    WHERE matches.organizationID = '{}'
    ORDER BY matchDate DESC;
    """.format(org)
    matches = execute_read_query(create_connection(database), select_matches_org)
    return matches

#Select all matches, in the order of descending match date
def selectMatchesAll(database):
    select_matches_all = """
    SELECT * from matches
    INNER JOIN users AS u1 ON matches.player1ID = u1.userID
    INNER JOIN users AS u2 ON matches.player2ID = u2.userID
    ORDER BY matchDate DESC;
    """
    matches = execute_read_query(create_connection(database), select_matches_all)
    return matches

#Select the specific player information given the userID
def selectPlayer(database,id):
    select_player = """
    SELECT * from players
    INNER JOIN users ON players.userID = users.userID
    WHERE users.userID = '{}' AND users.identity = 'player';
    """.format(id)
    player = execute_read_query(create_connection(database), select_player)
    return player

#Select the specific player information given the player's name
def findPlayerByName(database,name):
    nameFull = name.split(" ")
    find_player_by_name = """
    SELECT * from players
    WHERE firstName = '{}' AND lastName = '{}';
    """.format(nameFull[0],nameFull[1])
    player = execute_read_query(create_connection(database), find_player_by_name)
    return player

#Select the specific user information given the userID
def selectUser(database,id):
    select_user = """
    SELECT * from users
    WHERE users.userID = '{}';
    """.format(id)
    player = execute_read_query(create_connection(database), select_user)
    return player

#Select the specific match information given the matchName
def selectMatch(database,name):
    select_match = """
    SELECT * from matches
    INNER JOIN users AS u1 ON matches.player1ID = u1.userID
    INNER JOIN users AS u2 ON matches.player2ID = u2.userID
    WHERE matches.name = '{}';
    """.format(name)
    matchInfo = execute_read_query(create_connection(database), select_match)
    return matchInfo

usernameSpec = None #Use to record the username used to login
loginChance = 0 #Use to record the number of times the user tries to login, if the user entered wrong login details 5 times, the program closes.

###Login Page
def loginPage():
    login_Page = Tk()

    login_Page.title("Badminton Performance Management - Login")
    login_Page.geometry("475x350")
    login_Page.configure(background = "light blue")
    login_Page.resizable(False,False)

    #Tab control
    tabsystem = ttk.Notebook(login_Page)

    #Tabs - Organizer, Player, Guest
    loginTab1 = Frame(tabsystem)
    loginTab2 = Frame(tabsystem)
    loginTab3 = Frame(tabsystem)
    tabsystem.add(loginTab1, text='Organizer')
    tabsystem.add(loginTab2, text='Player')
    tabsystem.add(loginTab3, text='Guest')
    tabsystem.pack(expand=1, fill="both")

    #Login function as an organizer
    def login1():
        status = False
        username = usernameEnt1.get()
        password = passwordEnt1.get()
        organizers = selectOrganizers('bpmsdatabase')
        for i in organizers:
            if username == i[5] and password == i[6]:
                global usernameSpec
                usernameSpec = username
                status = True
                login_Page.destroy()
                frontPageOrganizer()
        if status != True:
            global loginChance
            if loginChance < 4:
                loginChance += 1
                messagebox.showerror('Login Error', 'Error: The username or password entered is invalid, you have {} more chances'.format(5-loginChance))
            else:
                messagebox.showerror('Login Error', 'Error: The username or password entered is invalid, you have tried too many times')
                login_Page.destroy()

    #Login function as a player
    def login2():
        status = False
        username = usernameEnt2.get()
        password = passwordEnt2.get()
        players = selectPlayers('bpmsdatabase')
        for i in players:
            if username == i[5] and password == i[6]:
                global usernameSpec
                usernameSpec = username
                status = True
                login_Page.destroy()
                frontPagePlayer()
        if status != True:
            global loginChance
            if loginChance < 4:
                loginChance += 1
                messagebox.showerror('Login Error', 'Error: The username or password entered is invalid, you have {} more chances'.format(5-loginChance))
            else:
                messagebox.showerror('Login Error', 'Error: The username or password entered is invalid, you have tried too many times')
                login_Page.destroy()
    
    #Login function as a guest
    def login3():
        login_Page.destroy()
        frontPageGuest()

    #Make the password visible
    def visible(tabNum):
            if tabNum == 1:
                password = passwordEnt1.get()
                if password != "":
                    visibleBtn1.destroy()
                visiblePassL = Label(loginTab1,text = password,background="white")
                visiblePassL.place(x=225,y=190,anchor="center")
                invisibleBtn = Button(loginTab1,text = "invisible",command = lambda: invisible(visiblePassL,invisibleBtn,tabNum))
                invisibleBtn.place(x=350,y=150,anchor="center")
            if tabNum == 2:
                password = passwordEnt2.get()
                if password != "":
                    visibleBtn2.destroy()
                visiblePassL = Label(loginTab2,text = password,background="white")
                visiblePassL.place(x=225,y=190,anchor="center")
                invisibleBtn = Button(loginTab2,text = "invisible",command = lambda: invisible(visiblePassL,invisibleBtn,tabNum))
                invisibleBtn.place(x=350,y=150,anchor="center")
    
    #Make the password invisible (show as '*')
    def invisible(label,button,tabNum):
        label.destroy()
        button.destroy()
        if tabNum == 1:
            visibleBtn = Button(loginTab1,text = "visible",command = lambda: visible(1))
            visibleBtn.place(x=350,y=150,anchor="center")
        if tabNum == 2:
            visibleBtn = Button(loginTab2,text = "visible",command = lambda: visible(2))
            visibleBtn.place(x=350,y=150,anchor="center")

    #Link to the forgotten password page
    def forgotten():
        forgottenPassword()

    #Link to the create account page
    def create():
        createAccount()

    loginL = Label(login_Page,text = "Login")
    loginL.place(x=250,y=80,anchor="center")

    ###Tab 1 - Organizer
    #Lables - username, password
    usernameL = Label(loginTab1,text = "User Name")
    usernameL.place(x=115,y=100,anchor="e")
    passwordL = Label(loginTab1,text = "Password")
    passwordL.place(x=115,y=150,anchor="e")
    #Entries - username, password
    usernameEnt1 = Entry(loginTab1,bg="light blue",relief=RAISED)
    usernameEnt1.place(x=225,y=100,anchor="center")
    passwordEnt1 = Entry(loginTab1,bg="light blue",relief=RAISED,show="*")
    passwordEnt1.place(x=225,y=150,anchor="center")
    #Buttons - login, visible, forgotten password, create account
    login1Btn = Button(loginTab1,text = "Login",command = login1)
    login1Btn.place(x=225,y=260,anchor="center")
    visibleBtn1 = Button(loginTab1,text = "visible",command = lambda: visible(1))
    visibleBtn1.place(x=350,y=150,anchor="center")
    forgottenBtn = Button(loginTab1,text = "Forgotten password?",command = forgotten)
    forgottenBtn.place(x=130,y=220,anchor="center")
    createBtn = Button(loginTab1,text = "Create Account?",command = create)
    createBtn.place(x=310,y=220,anchor="center")

    ###Tab 2 - Player
    #Lables - username, password
    usernameL = Label(loginTab2,text = "User Name")
    usernameL.place(x=115,y=100,anchor="e")
    passwordL = Label(loginTab2,text = "Password")
    passwordL.place(x=115,y=150,anchor="e")
    #Entries - username, password
    usernameEnt2 = Entry(loginTab2,bg="light blue",relief=RAISED)
    usernameEnt2.place(x=225,y=100,anchor="center")
    passwordEnt2 = Entry(loginTab2,bg="light blue",relief=RAISED,show="*")
    passwordEnt2.place(x=225,y=150,anchor="center")
    #Buttons - login, visible, forgotten password, create account
    login2Btn = Button(loginTab2,text = "Login",command = login2)
    login2Btn.place(x=225,y=260,anchor="center")
    visibleBtn2 = Button(loginTab2,text = "visible",command = lambda: visible(2))
    visibleBtn2.place(x=350,y=150,anchor="center")
    forgottenBtn = Button(loginTab2,text = "Forgotten password?",command = forgotten)
    forgottenBtn.place(x=130,y=220,anchor="center")
    createBtn = Button(loginTab2,text = "Create Account?",command = create)
    createBtn.place(x=310,y=220,anchor="center")

    ###Tab 3 - Guest
    #Lables - message
    limitedFuncL = Label(loginTab3,text = "No login details required, but limited functions.")
    limitedFuncL.place(x=225,y=85,anchor="center")
    #Buttons - login, create account
    login3Btn = Button(loginTab3,text = "Login",command = login3)
    login3Btn.place(x=225,y=180,anchor="center")
    createBtn = Button(loginTab3,text = "Create Account?",command = create)
    createBtn.place(x=225,y=130,anchor="center")

    login_Page.mainloop()



###Create Account Page
def createAccount():
    create_Account = Tk()

    create_Account.title("Badminton Performance Management - Create Account")
    create_Account.geometry("450x300")
    create_Account.configure(background = "light blue")
    create_Account.resizable(False,False)

    #Link back to the login page (destroy the creat account page only, as the login page is not destroyed when this is opened)
    def back():
        create_Account.destroy()

    #Create organizer account page
    def newOrganizer():
        new_Organizer = Toplevel()

        new_Organizer.title("Create an organizer account")
        new_Organizer.geometry("450x300")
        new_Organizer.configure(background = "light blue")
        new_Organizer.resizable(False,False)

        #Create a new organizer account
        def create():
            title = titleEnt.get()
            firstName = firstNameEnt.get()
            lastName = lastNameEnt.get()
            orgID = orgIDEnt.get()
            username = usernameEnt.get()
            email = emailEnt.get()
            password = str(passwordEnt.get())
            confirmPassword = str(confirmPasswordEnt.get())
            if title != "" and firstName != "" and lastName != "" and orgID != "" and username != ""  and email != "" and password == confirmPassword:
                organizations = selectOrganizations('bpmsdatabase')
                organizationIDs = [org[0] for org in organizations]
                if int(orgID) not in organizationIDs:
                    messagebox.showerror('Create Account Error', 'Error: The Organization does not exist, cannot create user.')
                    return
                else: 
                    create_users = """
                    INSERT INTO users (title, firstName, lastName, organizationID, username, password, email, identity)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', 'organizer');
                    """.format(title, firstName, lastName, orgID, username, password, email)
                    execute_query(create_connection('bpmsdatabase'), create_users)
                    messagebox.showinfo('Create Account Successful', 'Your account is created.')
                    new_Organizer.destroy()
                    create_Account.destroy()
            elif password != confirmPassword:
                messagebox.showerror('Create Account Error', 'Error: The passwords entered are not matched.')
            else:
                messagebox.showerror('Create Account Error', 'Error: Something went wrong, please try again.')

        #Labels
        Label(new_Organizer,text = "Title",background = "light blue").grid(row=0,column=0,sticky="e")
        Label(new_Organizer,text = "First Name",background = "light blue").grid(row=1,column=0,sticky="e")
        Label(new_Organizer,text = "Last Name",background = "light blue").grid(row=2,column=0,sticky="e")
        Label(new_Organizer,text = "Organization ID",background = "light blue").grid(row=3,column=0,sticky="e")
        Label(new_Organizer,text = "Username",background = "light blue").grid(row=4,column=0,sticky="e")
        Label(new_Organizer,text = "Email",background = "light blue").grid(row=5,column=0,sticky="e")
        Label(new_Organizer,text = "Password",background = "light blue").grid(row=6,column=0,sticky="e")
        Label(new_Organizer,text = "Confirm Password",background = "light blue").grid(row=7,column=0,sticky="e")
        #Entries
        titleEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        titleEnt.grid(row=0,column=1,sticky="e")
        firstNameEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        firstNameEnt.grid(row=1,column=1,sticky="e")
        lastNameEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        lastNameEnt.grid(row=2,column=1,sticky="e")
        orgIDEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        orgIDEnt.grid(row=3,column=1,sticky="e")
        usernameEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        usernameEnt.grid(row=4,column=1,sticky="e")
        emailEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        emailEnt.grid(row=5,column=1,sticky="e")
        passwordEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        passwordEnt.grid(row=6,column=1,sticky="e")
        confirmPasswordEnt = Entry(new_Organizer,bg="light blue",relief=RAISED)
        confirmPasswordEnt.grid(row=7,column=1,sticky="e")
        #Buttons
        Button(new_Organizer,text="Submit",command = create).grid(row=8,column=0,sticky="e")
    
    #Create player account page
    def newPlayer():
        new_Player = Toplevel()

        new_Player.title("Create a player account")
        new_Player.geometry("450x300")
        new_Player.configure(background = "light blue")
        new_Player.resizable(False,False)

        #Create a new organizer account
        def create():
            title = titleEnt.get()
            firstName = firstNameEnt.get()
            lastName = lastNameEnt.get()
            orgID = orgIDEnt.get()
            username = usernameEnt.get()
            email = emailEnt.get()
            password = passwordEnt.get()
            confirmPassword = confirmPasswordEnt.get()
            if title != "" and firstName != "" and lastName != "" and orgID != "" and username != ""  and email != "" and password == confirmPassword:
                organizations = selectOrganizations('bpmsdatabase')
                organizationIDs = [org[0] for org in organizations]
                if int(orgID) not in organizationIDs:
                    messagebox.showerror('Create Account Error', 'Error: The Organization does not exist, cannot create user.')
                    return
                else:
                    create_users = """
                    INSERT INTO users (title, firstName, lastName, organizationID, username, password, email, identity)
                    VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', 'player');
                    """.format(title, firstName, lastName, orgID, username, password, email)
                    execute_query(create_connection('bpmsdatabase'), create_users)
                    messagebox.showinfo('Create Account Successful', 'Your account is created.')
                    new_Player.destroy()
                    create_Account.destroy()
            elif password != confirmPassword:
                messagebox.showerror('Create Account Error', 'Error: The passwords entered are not matched.')
            else:
                messagebox.showerror('Create Account Error', 'Error: Something went wrong, please try again.')

        #Labels
        Label(new_Player,text = "Title",background = "light blue").grid(row=0,column=0,sticky="e")
        Label(new_Player,text = "First Name",background = "light blue").grid(row=1,column=0,sticky="e")
        Label(new_Player,text = "Last Name",background = "light blue").grid(row=2,column=0,sticky="e")
        Label(new_Player,text = "Organization ID",background = "light blue").grid(row=3,column=0,sticky="e")
        Label(new_Player,text = "Username",background = "light blue").grid(row=4,column=0,sticky="e")
        Label(new_Player,text = "Email",background = "light blue").grid(row=5,column=0,sticky="e")
        Label(new_Player,text = "Password",background = "light blue").grid(row=6,column=0,sticky="e")
        Label(new_Player,text = "Confirm Password",background = "light blue").grid(row=7,column=0,sticky="e")
        #Entries
        titleEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        titleEnt.grid(row=0,column=1,sticky="e")
        firstNameEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        firstNameEnt.grid(row=1,column=1,sticky="e")
        lastNameEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        lastNameEnt.grid(row=2,column=1,sticky="e")
        orgIDEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        orgIDEnt.grid(row=3,column=1,sticky="e")
        usernameEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        usernameEnt.grid(row=4,column=1,sticky="e")
        emailEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        emailEnt.grid(row=5,column=1,sticky="e")
        passwordEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        passwordEnt.grid(row=6,column=1,sticky="e")
        confirmPasswordEnt = Entry(new_Player,bg="light blue",relief=RAISED)
        confirmPasswordEnt.grid(row=7,column=1,sticky="e")
        #Buttons
        Button(new_Player,text="Submit",command = create).grid(row=8,column=0,sticky="e")

    #Buttons
    newOrgaBtn = Button(create_Account,text="Want to be an organizer?",command = newOrganizer)
    newOrgaBtn.place(x=50,y=150,anchor="w")
    newPlayBtn = Button(create_Account,text="Want to be a player?",command = newPlayer)
    newPlayBtn.place(x=400,y=150,anchor="e")
    backBtn = Button(create_Account,text="back",command = back)
    backBtn.place(x=300,y=200,anchor="center")

    create_Account.mainloop()

###Forgotten Password Page
def forgottenPassword():
    forgotten_Password = Tk()

    forgotten_Password.title("Badminton Performance Management - Forgotten Password")
    forgotten_Password.geometry("450x300")
    forgotten_Password.configure(background = "light blue")
    forgotten_Password.resizable(False,False)

    #Check if the verification code is correct; Link to the reset password page, if it is correct.
    def submit(emailAddress,code):
        verify = verifyEnt.get()
        if verify == str(code):
            resetPassword(emailAddress)
            forgotten_Password.destroy()
        else:
             messagebox.showerror('Forgotten Password Error', 'Error: Please enter the verification code sent to your email.')

    #Check if the email entered has an account; Generate a verification code (and send to the email), if it is.
    def sendCode():
        status = False
        emailSpec = str(emailEnt.get())
        users = selectUsers('bpmsdatabase')
        if emailSpec != "":
            for i in users:
                if emailSpec == i[7]:
                    status = True
                    submitBtn = Button(forgotten_Password,text="Submit",command = lambda: submit(emailSpec,verifyCode))
                    submitBtn.grid(row=2,column=1,sticky="w")
                    verifyCode = random.randint(1000,9999)
                    verifyCodeL = Label(forgotten_Password,text=str(verifyCode),background="light blue")
                    verifyCodeL.grid(row=2,column=1,sticky="e")
                    return emailSpec,verifyCode
        if status == False:
             messagebox.showerror('Forgotten Password Error', 'Error: Please enter a valid email.')

    #Labels
    Label(forgotten_Password,text = "Email",background = "light blue").grid(row=0,column=0,sticky="e")
    Label(forgotten_Password,text = "Verification Code",background = "light blue").grid(row=1,column=0,sticky="e")
    #Entries
    emailEnt = Entry(forgotten_Password,bg="light blue",relief=RAISED)
    emailEnt.grid(row=0,column=1,sticky="e")
    verifyEnt = Entry(forgotten_Password,bg="light blue",relief=RAISED)
    verifyEnt.grid(row=1,column=1,sticky="e")
    #Buttons
    sendCodeBtn = Button(forgotten_Password,text="Send Code",command = sendCode)
    sendCodeBtn.grid(row=1,column=2,sticky="e")

    forgotten_Password.mainloop()

###Reset Password Page
def resetPassword(emailAddress):
    reset_Password = Tk()

    reset_Password.title("Badminton Performance Management - Reset Password")
    reset_Password.geometry("450x300")
    reset_Password.configure(background = "light blue")
    reset_Password.resizable(False,False)

    #Check if the password entered and the confirm password entered match, and update the password for the user in the database.
    def reset(emailAddress):
        password = passwordEnt.get()
        confirmPassword = confirmPasswordEnt.get()
        if password != "" and password == confirmPassword:
            resetPassword = """
            UPDATE users
            SET password = '{}'
            WHERE email = '{}';
            """.format(password,emailAddress)
            execute_query(create_connection('bpmsdatabase'), resetPassword)
            messagebox.showinfo('Reset Password Successful', 'Your password is changed.')
            reset_Password.destroy()
        elif password != confirmPassword:
            messagebox.showerror('Reset Password Error', 'Error: The passwords entered are not matched.')
        else:
            messagebox.showerror('Reset Password Error', 'Error: Something went wrong, please try again.')

    #Labels
    Label(reset_Password,text = "New Password",background = "light blue").grid(row=0,column=0,sticky="e")
    Label(reset_Password,text = "Confirm Password",background = "light blue").grid(row=1,column=0,sticky="e")
    #Entries
    passwordEnt = Entry(reset_Password,bg="light blue",relief=RAISED)
    passwordEnt.grid(row=0,column=1,sticky="e")
    confirmPasswordEnt = Entry(reset_Password,bg="light blue",relief=RAISED)
    confirmPasswordEnt.grid(row=1,column=1,sticky="e")
    #Buttons
    SubmitBtn = Button(reset_Password,text="Submit",command = lambda: reset(emailAddress))
    SubmitBtn.grid(row=1,column=2,sticky="e")

    reset_Password.mainloop()



###Front Page
#Front Page for the users who logged in as an organizer.
def frontPageOrganizer():
    front_Page_Organizer = Tk()

    front_Page_Organizer.title("Badminton Performance Management - Organizer")
    front_Page_Organizer.geometry("1000x600")
    front_Page_Organizer.configure(background = "light blue")
    front_Page_Organizer.resizable(False,False)

    #Tab control
    tabsystem = ttk.Notebook(front_Page_Organizer)

    #Tabs
    tab1 = Frame(tabsystem)
    tab2 = Frame(tabsystem)
    tab3 = Frame(tabsystem)
    tab4 = Frame(tabsystem)
    tab5 = Frame(tabsystem)
    tab6 = Frame(tabsystem)
    tab7 = Frame(tabsystem)
    tabsystem.add(tab1, text='Home')
    tabsystem.add(tab2, text='Leader Board')
    tabsystem.add(tab3, text='Players')
    tabsystem.add(tab4, text='Matches')
    tabsystem.add(tab5, text='Matching Players')
    tabsystem.add(tab6, text='Record a Match')
    tabsystem.add(tab7, text='My Profile')
    tabsystem.pack(expand=1, fill="both")

    ###Tab 1 - Home
    tab1.configure(background = "light blue")
    #Lables
    welcomeL = Label(tab1,text = "Welcome to the\nBadminton Performace Management System",background="light blue")
    welcomeL.place(x=500,y=200,anchor="center")
    orgL = Label(tab1,text = "You belongs to "+str(identifyOrganizationName('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))),background="light blue")
    orgL.place(x=700,y=275,anchor="e")

    ###Tab 2 - Leader Board
    tab2.configure(background = "light blue")
    #Lables
    rankingL = Label(tab2,text = "Ranking",background="light blue")
    rankingL.place(x=100,y=50,anchor="center")
    playerNameL = Label(tab2,text = "Player Name",background="light blue")
    playerNameL.place(x=200,y=50,anchor="center")
    scoreTotalL = Label(tab2,text = "Score Total",background="light blue")
    scoreTotalL.place(x=300,y=50,anchor="center")
    scoreAveL = Label(tab2,text = "Score Average",background="light blue")
    scoreAveL.place(x=400,y=50,anchor="center")
    matchTotalL = Label(tab2,text = "Match Total",background="light blue")
    matchTotalL.place(x=500,y=50,anchor="center")
    matchWinL = Label(tab2,text = "Match Win",background="light blue")
    matchWinL.place(x=600,y=50,anchor="center")
    #Display the players with ranking
    for i, player in enumerate(orderPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab2, text=str(i+1), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab2, text=player[1]+" "+player[2], background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[6]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[7]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[9]), background="light blue").place(x=600, y=50+25*(i+1), anchor="center")
        
    #Check if the player name entered matches one of the player names stored in the system. If so, display a button for accessing the player's profile.
    def searchPlayer():
        playerName = playerNameEnt.get()
        players = selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))
        playerNames = [player[1]+" "+player[2] for player in players]
        if playerName not in playerNames:
            messagebox.showerror('Search Error', 'Error: The player is not found.')
            return
        else:
            playerID = identifyID2('bpmsdatabase',playerName)
            playerProfileBtn = Button(tab3,text = "Player Profile - "+str(playerName),command = lambda: playerProfile(playerID,'n'))
            playerProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 3 - Players
    tab3.configure(background = "light blue")
    #Lables
    playerNameL = Label(tab3,text = "Player Name",background="light blue")
    playerNameL.place(x=100,y=50,anchor="center")
    scoreTotalL = Label(tab3,text = "Score Total",background="light blue")
    scoreTotalL.place(x=200,y=50,anchor="center")
    scoreAveL = Label(tab3,text = "Score Average",background="light blue")
    scoreAveL.place(x=300,y=50,anchor="center")
    matchTotalL = Label(tab3,text = "Match Total",background="light blue")
    matchTotalL.place(x=400,y=50,anchor="center")
    matchWinL = Label(tab3,text = "Match Win",background="light blue")
    matchWinL.place(x=500,y=50,anchor="center")
    for i, player in enumerate(selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab3, text=player[1]+" "+player[2], background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[6]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[7]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[8]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[9]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchPlayerL = Label(tab3,text = "Search",background="light blue")
    searchPlayerL.place(x=100,y=25,anchor="center")
    #Entries
    playerNameEnt = Entry(tab3,bg="light blue",relief=RAISED)
    playerNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchPlayerBtn = Button(tab3,text = "Search",command = searchPlayer)
    searchPlayerBtn.place(x=400,y=25,anchor="center")

    #Check if the match name entered matches one of the match names stored in the system. If so, display a button for accessing the match's profile.
    def searchMatch():
        matchName = matchNameEnt.get()
        matches = selectMatchesOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))
        matchNames = [match[2] for match in matches]
        if str(matchName) not in matchNames:
            messagebox.showerror('Search Error', 'Error: The match is not found.')
            return
        else:
            matchProfileBtn = Button(tab4,text = "Match Profile - "+str(matchName),command = lambda: matchProfile(matchName))
            matchProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 4 - Matches
    tab4.configure(background = "light blue")
    #Lables
    matchNameL = Label(tab4,text = "Match Name",background="light blue")
    matchNameL.place(x=100,y=50,anchor="center")
    matchDateL = Label(tab4,text = "Date",background="light blue")
    matchDateL.place(x=200,y=50,anchor="center")
    playerName1L = Label(tab4,text = "Player 1",background="light blue")
    playerName1L.place(x=300,y=50,anchor="center")
    playerName2L = Label(tab4,text = "Player 2",background="light blue")
    playerName2L.place(x=400,y=50,anchor="center")
    scoreL = Label(tab4,text = "Score",background="light blue")
    scoreL.place(x=500,y=50,anchor="center")
    for i, match in enumerate(selectMatchesOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab4, text=str(match[2]), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[3]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[11]+" "+match[12]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[20]+" "+match[21]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[7])+" vs "+str(match[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchMatchL = Label(tab4,text = "Search",background="light blue")
    searchMatchL.place(x=100,y=25,anchor="center")
    #Entries
    matchNameEnt = Entry(tab4,bg="light blue",relief=RAISED)
    matchNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchMatchBtn = Button(tab4,text = "Search",command = searchMatch)
    searchMatchBtn.place(x=400,y=25,anchor="center")

    #Matching players function for tab5
    def matching():
        different = False
        while different == False:
            player1ID = random.choice(selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec)))[0]
            player2ID = random.choice(selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec)))[0]
            if player1ID != player2ID:
                different = True
        player1 = selectPlayer('bpmsdatabase',player1ID)[0]
        player2 = selectPlayer('bpmsdatabase',player2ID)[0]
        Label(tab5, text=str(player1[1]+" "+player1[2]), background="light blue",padx=20).place(x=250, y=100, anchor="center")
        Label(tab5, text=str(player2[1]+" "+player2[2]), background="light blue",padx=20).place(x=500, y=100, anchor="center")

    ###Tab 5 - Matching Players
    tab5.configure(background = "light blue")
    #Lables
    player1L = Label(tab5,text = "Player 1",background="light blue")
    player1L.place(x=250,y=50,anchor="center")
    player2L = Label(tab5,text = "Player 2",background="light blue")
    player2L.place(x=500,y=50,anchor="center")
    #Buttons
    matchBtn = Button(tab5,text = "Match",command = matching)
    matchBtn.place(x=250,y=200,anchor="center")

    #Record a match function for tab6
    def next():
        matchName = matchNamingEnt.get()
        date = dateEnt.selection_get()
        link = linkEnt.get()
        player1 = player1nameEnt.get()
        player2 = player2nameEnt.get()
        player1score = player1scoreEnt.get()
        player2score = player2scoreEnt.get()
        if matchName != "" and date != "" and link != "" and player1 != "" and player2 != "" and player1score != "" and player2score != "":
            players = selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))
            playerNames = [player[1]+" "+player[2] for player in players]
            if player1 not in playerNames or player2 not in playerNames:
                messagebox.showerror('Record Match Error', 'Error: The player does not exist, cannot record the match.')
                return
            else:
                if player1score.isnumeric() and player2score.isnumeric():
                    player1ID = findPlayerByName('bpmsdatabase',player1)[0][0]
                    player2ID = findPlayerByName('bpmsdatabase',player2)[0][0]
                    create_match =  """
                    INSERT INTO
                    matches (organizationID,name,matchDate,vedioLink,player1ID,player2ID,player1Score,player2Score)
                    VALUES
                        ('{}', '{}', '{}','{}','{}','{}','{}','{}');
                    """.format(identifyOrganization('bpmsdatabase',usernameSpec),matchName,date,link,player1ID,player2ID,player1score,player2score)
                    execute_query(create_connection('bpmsdatabase'),create_match)
                    messagebox.showinfo('Record Match Successful', 'The match is recorded, please fill in how the players scored each point.')
                    if player1score != "0":
                        player1score = int(player1score)-1
                        successfulShots("1",int(player1score),int(player2score),player1ID,player2ID)
                    elif player1score == "0" and player2score != "0":
                        player2score = int(player2score)-1
                        successfulShots("2",int(player1score),int(player2score),player1ID,player2ID)
                else:
                    messagebox.showinfo('Record Error', 'Error: Please enter integers for the scores.')
        else:
            messagebox.showerror('Record Error', 'Error: Please fill in all fields.')
    
    ###Tab 6 - Record a Match
    tab6.configure(background = "light blue")
    #Lables
    player1L = Label(tab6,text = "Player 1",background="light blue")
    player1L.place(x=250,y=50,anchor="center")
    player2L = Label(tab6,text = "Player 2",background="light blue")
    player2L.place(x=500,y=50,anchor="center")
    nameL = Label(tab6,text = "Name:",background="light blue")
    nameL.place(x=100,y=100,anchor="center")
    scoresL = Label(tab6,text = "Scores:",background="light blue")
    scoresL.place(x=100,y=150,anchor="center")
    matchNamingL = Label(tab6,text = "Match Name:",bg="light blue")
    matchNamingL.place(x=100,y=200,anchor="center")
    dateL = Label(tab6,text = "Date:",bg="light blue")
    dateL.place(x=100,y=300,anchor="center")
    linkL = Label(tab6,text = "Link:",bg="light blue")
    linkL.place(x=100,y=250,anchor="center")
    #Entries
    player1nameEnt = Entry(tab6,bg="light blue",relief=RAISED)
    player1nameEnt.place(x=250,y=100,anchor="center")
    player2nameEnt = Entry(tab6,bg="light blue",relief=RAISED)
    player2nameEnt.place(x=500,y=100,anchor="center")
    player1scoreEnt = Entry(tab6,bg="light blue",relief=RAISED)
    player1scoreEnt.place(x=250,y=150,anchor="center")
    player2scoreEnt = Entry(tab6,bg="light blue",relief=RAISED)
    player2scoreEnt.place(x=500,y=150,anchor="center")
    matchNamingEnt = Entry(tab6,bg="light blue",relief=RAISED)
    matchNamingEnt.place(x=250,y=200,anchor="center")
    dateEnt = Calendar(tab6,bg="light blue",selectmode='day')
    dateEnt.place(x=250,y=300,anchor="n")
    linkEnt = Entry(tab6,bg="light blue",relief=RAISED)
    linkEnt.place(x=250,y=250,anchor="center")
    #Buttons
    nextBtn = Button(tab6,text = "Next",command = next)
    nextBtn.place(x=250,y=500,anchor="center")
    
    def changePassword(usernameSpec):
        change_Password = Tk()

        change_Password.title("Badminton Performance Management - Reset Password")
        change_Password.geometry("450x300")
        change_Password.configure(background = "light blue")
        change_Password.resizable(False,False)

        def reset(username):
            password = passwordEnt.get()
            confirmPassword = confirmPasswordEnt.get()
            if password != "" and password == confirmPassword:
                resetPassword = """
                UPDATE users
                SET password = '{}'
                WHERE username = '{}';
                """.format(password,username)
                execute_query(create_connection('bpmsdatabase'), resetPassword)
                messagebox.showinfo('Change Password Successful', 'Your password is changed.')
                change_Password.destroy()
            elif password != confirmPassword:
                messagebox.showerror('Change Password Error', 'Error: The passwords entered are not matched.')
            else:
                messagebox.showerror('Change Password Error', 'Error: Something went wrong, please try again.')

        #Labels
        Label(change_Password,text = "New Password",background = "light blue").grid(row=0,column=0,sticky="e")
        Label(change_Password,text = "Confirm Password",background = "light blue").grid(row=1,column=0,sticky="e")
        #Entries
        passwordEnt = Entry(change_Password,bg="light blue",relief=RAISED)
        passwordEnt.grid(row=0,column=1,sticky="e")
        confirmPasswordEnt = Entry(change_Password,bg="light blue",relief=RAISED)
        confirmPasswordEnt.grid(row=1,column=1,sticky="e")
        #Buttons
        SubmitBtn = Button(change_Password,text="Submit",command = lambda: reset(usernameSpec))
        SubmitBtn.grid(row=1,column=2,sticky="e")

        change_Password.mainloop()

    ###Tab 7 - My Profile
    tab7.configure(background = "light blue")
    #Take the user's information from the database
    userID = identifyID('bpmsdatabase',usernameSpec)
    userTitle = selectUser('bpmsdatabase',userID)[0][1]
    userFirstName = selectUser('bpmsdatabase',userID)[0][2]
    userLastName = selectUser('bpmsdatabase',userID)[0][3]
    userOrganizationName = identifyOrganizationName('bpmsdatabase',selectUser('bpmsdatabase',userID)[0][4])
    userEmail = selectUser('bpmsdatabase',userID)[0][7]
    #Lables
    userIDL = Label(tab7,text = "User ID",background="light blue")
    userIDL.place(x=100,y=50,anchor="center")
    userIDSpec = Label(tab7,text = str(userID),background="light blue")
    userIDSpec.place(x=250,y=50,anchor="center")
    titleDoneL = Label(tab7,text = "Title",background="light blue")
    titleDoneL.place(x=100,y=75,anchor="center")
    titleSpecL = Label(tab7,text = str(userTitle),background="light blue")
    titleSpecL.place(x=250,y=75,anchor="center")
    firstNameDoneL = Label(tab7,text = "First Name",background="light blue")
    firstNameDoneL.place(x=100,y=100,anchor="center")
    firstNameSpecL = Label(tab7,text = str(userFirstName),background="light blue")
    firstNameSpecL.place(x=250,y=100,anchor="center")
    lastNameDoneL = Label(tab7,text = "Last Name",background="light blue")
    lastNameDoneL.place(x=100,y=125,anchor="center")
    lastNameSpecL = Label(tab7,text = str(userLastName),background="light blue")
    lastNameSpecL.place(x=250,y=125,anchor="center")
    organizationNameDoneL = Label(tab7,text = "Organization Name",background="light blue")
    organizationNameDoneL.place(x=100,y=150,anchor="center")
    organizationNameSpecL = Label(tab7,text = str(userOrganizationName),background="light blue")
    organizationNameSpecL.place(x=250,y=150,anchor="center")
    usernameDoneL = Label(tab7,text = "Username",background="light blue")
    usernameDoneL.place(x=100,y=175,anchor="center")
    usernameSpecL = Label(tab7,text = str(usernameSpec),background="light blue")
    usernameSpecL.place(x=250,y=175,anchor="center")
    emailDoneL = Label(tab7,text = "Email",background="light blue")
    emailDoneL.place(x=100,y=200,anchor="center")
    emailSpecL = Label(tab7,text = str(userEmail),background="light blue")
    emailSpecL.place(x=250,y=200,anchor="center")
    passwordDoneL = Label(tab7,text = "Password",background="light blue")
    passwordDoneL.place(x=100,y=225,anchor="center")
    #Buttons
    changePasswordBtn = Button(tab7,text = "Change Password",command = lambda: changePassword(usernameSpec))
    changePasswordBtn.place(x=250,y=225,anchor="center")

    front_Page_Organizer.mainloop()


#Front Page for the users who logged in as a player. All the functions a player has access to are the same to the organizer's, other than my profile page button in my profile.
def frontPagePlayer():
    front_Page_Player = Tk()

    front_Page_Player.title("Badminton Performance Management - Player")
    front_Page_Player.geometry("1000x600")
    front_Page_Player.configure(background = "light blue")
    front_Page_Player.resizable(False,False)

    #Tab control
    tabsystem = ttk.Notebook(front_Page_Player)

    #Tabs
    tab1 = Frame(tabsystem)
    tab2 = Frame(tabsystem)
    tab3 = Frame(tabsystem)
    tab4 = Frame(tabsystem)
    tab5 = Frame(tabsystem)
    tabsystem.add(tab1, text='Home')
    tabsystem.add(tab2, text='Leader Board')
    tabsystem.add(tab3, text='Players')
    tabsystem.add(tab4, text='Matches')
    tabsystem.add(tab5, text='My Profile')
    tabsystem.pack(expand=1, fill="both")

    ###Tab 1 - Home
    tab1.configure(background = "light blue")
    #Lables
    welcomeL = Label(tab1,text = "Welcome to the\nBadminton Performace Management System",background="light blue")
    welcomeL.place(x=500,y=200,anchor="center")
    orgL = Label(tab1,text = "You belongs to "+str(identifyOrganizationName('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))),background="light blue")
    orgL.place(x=700,y=275,anchor="e")

    ###Tab 2 - Leader Board
    tab2.configure(background = "light blue")
    #Lables
    rankingL = Label(tab2,text = "Ranking",background="light blue")
    rankingL.place(x=100,y=50,anchor="center")
    playerNameL = Label(tab2,text = "Player Name",background="light blue")
    playerNameL.place(x=200,y=50,anchor="center")
    scoreTotalL = Label(tab2,text = "Score Total",background="light blue")
    scoreTotalL.place(x=300,y=50,anchor="center")
    scoreAveL = Label(tab2,text = "Score Average",background="light blue")
    scoreAveL.place(x=400,y=50,anchor="center")
    matchTotalL = Label(tab2,text = "Match Total",background="light blue")
    matchTotalL.place(x=500,y=50,anchor="center")
    matchWinL = Label(tab2,text = "Match Win",background="light blue")
    matchWinL.place(x=600,y=50,anchor="center")
    for i, player in enumerate(orderPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab2, text=str(i+1), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab2, text=player[1]+" "+player[2], background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[6]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[7]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[9]), background="light blue").place(x=600, y=50+25*(i+1), anchor="center")
    
    def searchPlayer():
        playerName = playerNameEnt.get()
        players = selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))
        playerNames = [player[1]+" "+player[2] for player in players]
        if playerName not in playerNames:
            messagebox.showerror('Search Error', 'Error: The player is not found.')
            return
        else:
            playerID = identifyID2('bpmsdatabase',playerName)
            playerProfileBtn = Button(tab3,text = "Player Profile - "+str(playerName),command = lambda: playerProfile(playerID,'n'))
            playerProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 3 - Players
    tab3.configure(background = "light blue")
    #Lables
    playerNameL = Label(tab3,text = "Player Name",background="light blue")
    playerNameL.place(x=100,y=50,anchor="center")
    scoreTotalL = Label(tab3,text = "Score Total",background="light blue")
    scoreTotalL.place(x=200,y=50,anchor="center")
    scoreAveL = Label(tab3,text = "Score Average",background="light blue")
    scoreAveL.place(x=300,y=50,anchor="center")
    matchTotalL = Label(tab3,text = "Match Total",background="light blue")
    matchTotalL.place(x=400,y=50,anchor="center")
    matchWinL = Label(tab3,text = "Match Win",background="light blue")
    matchWinL.place(x=500,y=50,anchor="center")
    for i, player in enumerate(selectPlayersOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab3, text=player[1]+" "+player[2], background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[6]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[7]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[8]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[9]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchPlayerL = Label(tab3,text = "Search",background="light blue")
    searchPlayerL.place(x=100,y=25,anchor="center")
    #Entries
    playerNameEnt = Entry(tab3,bg="light blue",relief=RAISED)
    playerNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchPlayerBtn = Button(tab3,text = "Search",command = searchPlayer)
    searchPlayerBtn.place(x=400,y=25,anchor="center")
    
    def searchMatch():
        matchName = matchNameEnt.get()
        matches = selectMatchesOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))
        matchNames = [match[2] for match in matches]
        if str(matchName) not in matchNames:
            messagebox.showerror('Search Error', 'Error: The match is not found.')
            return
        else:
            matchProfileBtn = Button(tab4,text = "Match Profile - "+str(matchName),command = lambda: matchProfile(matchName))
            matchProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 4 - Matches
    tab4.configure(background = "light blue")
    #Lables
    matchNameL = Label(tab4,text = "Match Name",background="light blue")
    matchNameL.place(x=100,y=50,anchor="center")
    DateL = Label(tab4,text = "Date",background="light blue")
    DateL.place(x=200,y=50,anchor="center")
    playerName1L = Label(tab4,text = "Player 1",background="light blue")
    playerName1L.place(x=300,y=50,anchor="center")
    playerName2L = Label(tab4,text = "Player 2",background="light blue")
    playerName2L.place(x=400,y=50,anchor="center")
    scoreL = Label(tab4,text = "Score",background="light blue")
    scoreL.place(x=500,y=50,anchor="center")
    for i, match in enumerate(selectMatchesOrg('bpmsdatabase',identifyOrganization('bpmsdatabase',usernameSpec))):
        Label(tab4, text=str(match[2]), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[3]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[11]+" "+match[12]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[20]+" "+match[21]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[7])+" vs "+str(match[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchMatchL = Label(tab4,text = "Search",background="light blue")
    searchMatchL.place(x=100,y=25,anchor="center")
    #Entries
    matchNameEnt = Entry(tab4,bg="light blue",relief=RAISED)
    matchNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchMatchBtn = Button(tab4,text = "Search",command = searchMatch)
    searchMatchBtn.place(x=400,y=25,anchor="center")

    def changePassword(usernameSpec):
        change_Password = Tk()

        change_Password.title("Badminton Performance Management - Reset Password")
        change_Password.geometry("450x300")
        change_Password.configure(background = "light blue")
        change_Password.resizable(False,False)

        def reset(username):
            password = passwordEnt.get()
            confirmPassword = confirmPasswordEnt.get()
            if password != "" and password == confirmPassword:
                resetPassword = """
                UPDATE users
                SET password = '{}'
                WHERE username = '{}';
                """.format(password,username)
                execute_query(create_connection('bpmsdatabase'), resetPassword)
                messagebox.showinfo('Change Password Successful', 'Your password is changed.')
                change_Password.destroy()
            elif password != confirmPassword:
                messagebox.showerror('Change Password Error', 'Error: The passwords entered are not matched.')
            else:
                messagebox.showerror('Change Password Error', 'Error: Something went wrong, please try again.')

        #Labels
        Label(change_Password,text = "New Password",background = "light blue").grid(row=0,column=0,sticky="e")
        Label(change_Password,text = "Confirm Password",background = "light blue").grid(row=1,column=0,sticky="e")
        #Entries
        passwordEnt = Entry(change_Password,bg="light blue",relief=RAISED)
        passwordEnt.grid(row=0,column=1,sticky="e")
        confirmPasswordEnt = Entry(change_Password,bg="light blue",relief=RAISED)
        confirmPasswordEnt.grid(row=1,column=1,sticky="e")
        #Buttons
        SubmitBtn = Button(change_Password,text="Submit",command = lambda: reset(usernameSpec))
        SubmitBtn.grid(row=1,column=2,sticky="e")

        change_Password.mainloop()

    def myPlayerProfile(username):
        userID = identifyID('bpmsdatabase',username)
        playerProfile(userID,True)
    
    ###Tab 5 - My Profile
    tab5.configure(background = "light blue")
        #Take the user's information from the database
    userID = identifyID('bpmsdatabase',usernameSpec)
    userTitle = selectUser('bpmsdatabase',userID)[0][1]
    userFirstName = selectUser('bpmsdatabase',userID)[0][2]
    userLastName = selectUser('bpmsdatabase',userID)[0][3]
    userOrganizationName = identifyOrganizationName('bpmsdatabase',selectUser('bpmsdatabase',userID)[0][4])
    userEmail = selectUser('bpmsdatabase',userID)[0][7]
    #Lables
    userIDL = Label(tab5,text = "User ID",background="light blue")
    userIDL.place(x=100,y=50,anchor="center")
    userIDSpec = Label(tab5,text = str(userID),background="light blue")
    userIDSpec.place(x=250,y=50,anchor="center")
    titleDoneL = Label(tab5,text = "Title",background="light blue")
    titleDoneL.place(x=100,y=75,anchor="center")
    titleSpecL = Label(tab5,text = str(userTitle),background="light blue")
    titleSpecL.place(x=250,y=75,anchor="center")
    firstNameDoneL = Label(tab5,text = "First Name",background="light blue")
    firstNameDoneL.place(x=100,y=100,anchor="center")
    firstNameSpecL = Label(tab5,text = str(userFirstName),background="light blue")
    firstNameSpecL.place(x=250,y=100,anchor="center")
    lastNameDoneL = Label(tab5,text = "Last Name",background="light blue")
    lastNameDoneL.place(x=100,y=125,anchor="center")
    lastNameSpecL = Label(tab5,text = str(userLastName),background="light blue")
    lastNameSpecL.place(x=250,y=125,anchor="center")
    organizationNameDoneL = Label(tab5,text = "Organization Name",background="light blue")
    organizationNameDoneL.place(x=100,y=150,anchor="center")
    organizationNameSpecL = Label(tab5,text = str(userOrganizationName),background="light blue")
    organizationNameSpecL.place(x=250,y=150,anchor="center")
    usernameDoneL = Label(tab5,text = "Username",background="light blue")
    usernameDoneL.place(x=100,y=175,anchor="center")
    usernameSpecL = Label(tab5,text = str(usernameSpec),background="light blue")
    usernameSpecL.place(x=250,y=175,anchor="center")
    emailDoneL = Label(tab5,text = "Email",background="light blue")
    emailDoneL.place(x=100,y=200,anchor="center")
    emailSpecL = Label(tab5,text = str(userEmail),background="light blue")
    emailSpecL.place(x=250,y=200,anchor="center")
    passwordDoneL = Label(tab5,text = "Password",background="light blue")
    passwordDoneL.place(x=100,y=225,anchor="center")
    playerProfileL = Label(tab5,text = "My Profile",background="light blue")
    playerProfileL.place(x=100,y=250,anchor="center")
    #Buttons
    changePasswordBtn = Button(tab5,text = "Change Password",command = lambda: changePassword(usernameSpec))
    changePasswordBtn.place(x=250,y=225,anchor="center")
    myPlayerProfileBtn = Button(tab5,text = "My Player Profile",command = lambda: myPlayerProfile(usernameSpec))
    myPlayerProfileBtn.place(x=250,y=250,anchor="center")

    front_Page_Player.mainloop()


#Front Page for the users who logged in as a guest. All the functions a guest has access to are the almost same to the organizer's, other than login tab.
#Additionally, the guest can view all players and matches from all organizations, whereas an organizer and a player can only see the players and matches in the organization that they are in.
def frontPageGuest():
    front_Page_Guest = Tk()

    front_Page_Guest.title("Badminton Performance Management - Guest")
    front_Page_Guest.geometry("1000x600")
    front_Page_Guest.configure(background = "light blue")
    front_Page_Guest.resizable(False,False)

    def login():
        front_Page_Guest.destroy()
        loginPage()

    #Tab control
    tabsystem = ttk.Notebook(front_Page_Guest)

    #Tabs
    tab1 = Frame(tabsystem)
    tab2 = Frame(tabsystem)
    tab3 = Frame(tabsystem)
    tab4 = Frame(tabsystem)
    tab5 = Frame(tabsystem)
    tabsystem.add(tab1, text='Home')
    tabsystem.add(tab2, text='Leader Board')
    tabsystem.add(tab3, text='Players')
    tabsystem.add(tab4, text='Matches')
    tabsystem.add(tab5, text='Login')
    tabsystem.pack(expand=1, fill="both")

    ###Tab 1 - Home
    tab1.configure(background = "light blue")
    #Lables
    welcomeL = Label(tab1,text = "Welcome to the\nBadminton Performace Management System",background="light blue")
    welcomeL.place(x=500,y=200,anchor="center")

    ###Tab 2 - Leader Board
    tab2.configure(background = "light blue")
    #Lables
    rankingL = Label(tab2,text = "Ranking",background="light blue")
    rankingL.place(x=100,y=50,anchor="center")
    playerNameL = Label(tab2,text = "Player Name",background="light blue")
    playerNameL.place(x=200,y=50,anchor="center")
    scoreTotalL = Label(tab2,text = "Score Total",background="light blue")
    scoreTotalL.place(x=300,y=50,anchor="center")
    scoreAveL = Label(tab2,text = "Score Average",background="light blue")
    scoreAveL.place(x=400,y=50,anchor="center")
    matchTotalL = Label(tab2,text = "Match Total",background="light blue")
    matchTotalL.place(x=500,y=50,anchor="center")
    matchWinL = Label(tab2,text = "Match Win",background="light blue")
    matchWinL.place(x=600,y=50,anchor="center")
    for i, player in enumerate(orderPlayersAll('bpmsdatabase')):
        Label(tab2, text=str(i+1), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab2, text=player[1]+" "+player[2], background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[6]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[7]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
        Label(tab2, text=str(player[9]), background="light blue").place(x=600, y=50+25*(i+1), anchor="center")
    
    def searchPlayer():
        playerName = playerNameEnt.get()
        players = selectPlayersAll('bpmsdatabase')
        playerNames = [player[1]+" "+player[2] for player in players]
        if playerName not in playerNames:
            messagebox.showerror('Search Error', 'Error: The player is not found.')
            return
        else:
            playerID = identifyID2('bpmsdatabase',playerName)
            playerProfileBtn = Button(tab3,text = "Player Profile - "+str(playerName),command = lambda: playerProfile(playerID,'n'))
            playerProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 3 - Players
    tab3.configure(background = "light blue")
    #Lables
    playerNameL = Label(tab3,text = "Player Name",background="light blue")
    playerNameL.place(x=100,y=50,anchor="center")
    scoreTotalL = Label(tab3,text = "Score Total",background="light blue")
    scoreTotalL.place(x=200,y=50,anchor="center")
    scoreAveL = Label(tab3,text = "Score Average",background="light blue")
    scoreAveL.place(x=300,y=50,anchor="center")
    matchTotalL = Label(tab3,text = "Match Total",background="light blue")
    matchTotalL.place(x=400,y=50,anchor="center")
    matchWinL = Label(tab3,text = "Match Win",background="light blue")
    matchWinL.place(x=500,y=50,anchor="center")
    for i, player in enumerate(selectPlayersAll('bpmsdatabase')):
        Label(tab3, text=player[1]+" "+player[2], background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[6]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[7]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[8]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab3, text=str(player[9]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchPlayerL = Label(tab3,text = "Search",background="light blue")
    searchPlayerL.place(x=100,y=25,anchor="center")
    #Entries
    playerNameEnt = Entry(tab3,bg="light blue",relief=RAISED)
    playerNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchPlayerBtn = Button(tab3,text = "Search",command = searchPlayer)
    searchPlayerBtn.place(x=400,y=25,anchor="center")
    
    def searchMatch():
        matchName = matchNameEnt.get()
        matches = selectMatchesAll('bpmsdatabase')
        matchNames = [match[2] for match in matches]
        if str(matchName) not in matchNames:
            messagebox.showerror('Search Error', 'Error: The match is not found.')
            return
        else:
            matchProfileBtn = Button(tab4,text = "Match Profile - "+str(matchName),command = lambda: matchProfile(matchName))
            matchProfileBtn.place(x=600,y=25,anchor="center")

    ###Tab 4 - Matches
    tab4.configure(background = "light blue")
    #Lables
    matchNameL = Label(tab4,text = "Match Name",background="light blue")
    matchNameL.place(x=100,y=50,anchor="center")
    DateL = Label(tab4,text = "Date",background="light blue")
    DateL.place(x=200,y=50,anchor="center")
    playerName1L = Label(tab4,text = "Player 1",background="light blue")
    playerName1L.place(x=300,y=50,anchor="center")
    playerName2L = Label(tab4,text = "Player 2",background="light blue")
    playerName2L.place(x=400,y=50,anchor="center")
    scoreL = Label(tab4,text = "Score",background="light blue")
    scoreL.place(x=500,y=50,anchor="center")
    for i, match in enumerate(selectMatchesAll('bpmsdatabase')):
        Label(tab4, text=str(match[2]), background="light blue").place(x=100, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[3]), background="light blue").place(x=200, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[11]+" "+match[12]), background="light blue").place(x=300, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[20]+" "+match[21]), background="light blue").place(x=400, y=50+25*(i+1), anchor="center")
        Label(tab4, text=str(match[7])+" vs "+str(match[8]), background="light blue").place(x=500, y=50+25*(i+1), anchor="center")
    searchMatchL = Label(tab4,text = "Search",background="light blue")
    searchMatchL.place(x=100,y=25,anchor="center")
    #Entries
    matchNameEnt = Entry(tab4,bg="light blue",relief=RAISED)
    matchNameEnt.place(x=250,y=25,anchor="center")
    #Buttons
    searchMatchBtn = Button(tab4,text = "Search",command = searchMatch)
    searchMatchBtn.place(x=400,y=25,anchor="center")

    ###Tab 5 - Login
    tab5.configure(background = "light blue")
    loginBtn = Button(tab5,text = "Login",command = login)
    loginBtn.place(x=500,y=200,anchor="center")

    front_Page_Guest.mainloop()

###Successful Shots Page (For recording how the player scored each point)
def successfulShots(playerNum,player1score,player2score,player1ID,player2ID):
    successful_Shots = Tk()

    successful_Shots.title("Badminton Performance Management - Successful Shots")
    successful_Shots.geometry("1000x600")
    successful_Shots.configure(background = "light blue")
    successful_Shots.resizable(False,False)
    
    if str(playerNum) == '1':
        opponentNum = '2'
    elif str(playerNum) == '2':
        opponentNum = '1'

    #To go to how the next point is scored.
    def nextShot(playerNum,player1score,player2score,player1ID,player2ID):
        state = True
        done = False
        hitT = hit.get()
        failureShotT = failureShot.get()
        foulT = foul.get()
        print(hitT,failureShotT,foulT)
        if (hitT != True and failureShotT != True and foulT != True) or (hitT == True and (failureShotT == True or foulT == True)) or (failureShotT == True and (hitT == True or foulT == True)):
            messagebox.showerror('Record Match Error', 'Error: Tick one of hit, failure shot and foul.')
            state = False
            if hitT == True:
                foreHandT = foreHand.get()
                backHandT = backHand.get()
                if foreHandT != True and backHandT != True:
                    messagebox.showerror('Record Match Error', 'Error: Tick one of forehand and backhand.')
                    state = False
                overShoulderT = overShoulder.get()
                belowShoulderT = belowShoulder.get()
                if overShoulderT != True and belowShoulderT != True:
                    messagebox.showerror('Record Match Error', 'Error: Tick one of over shoulder and below shoulder.')
                    state = False
                backCourt1T = backCourt1.get()
                foreCourt1T = foreCourt1.get()
                midCourt1T = midCourt1.get()
                if (backCourt1T != True and foreCourt1T != True and midCourt1T != True) or (backCourt1T == True and (foreCourt1T == True or midCourt1T != True)) or (foreCourt1T == True and (backCourt1T == True or midCourt1T != True)):
                    messagebox.showerror('Record Match Error', 'Error: Tick one of back court, fore court and mid court.')
                    state = False
                leftCourt1T = leftCourt1.get()
                rightCourt1T = rightCourt1.get()
                if leftCourt1T != True and rightCourt1T != True:
                    messagebox.showerror('Record Match Error', 'Error: Tick one of left court and right court.')
                    state = False
                backCourt2T = backCourt2.get()
                foreCourt2T = foreCourt2.get()
                midCourt2T = midCourt2.get()
                if (backCourt2T != True and foreCourt2T != True and midCourt2T != True) or (backCourt2T == True and (foreCourt2T == True or midCourt2T != True)) or (foreCourt2T == True and (backCourt2T == True or midCourt2T != True)):
                    messagebox.showerror('Record Match Error', 'Error: Tick one of back court, fore court and mid court.')
                    state = False
                leftCourt2T = leftCourt2.get()
                rightCourt2T = rightCourt2.get()
                if leftCourt2T != True and rightCourt2T != True:
                    messagebox.showerror('Record Match Error', 'Error: Tick one of left court and right court.')
                    state = False
                highT = high.get()
                lowT = low.get()
                if highT != True and lowT != True:
                    messagebox.showerror('Record Match Error', 'Error: Tick one of high and low court.')
                    state = False
                if state == False:
                    return
                else:
                    if playerNum == "1":
                        if foreHandT == True:
                            update_players_foreHand = """
                            UPDATE players
                            SET foreHand = foreHand + 1
                            WHERE userID = '{}';
                            """.format(player1ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_foreHand)
                        elif backHandT == True:
                            update_players_backHand = """
                            UPDATE players
                            SET backHand = backHand + 1
                            WHERE userID = '{}';
                            """.format(player1ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_backHand)
                        if highT == True:
                            update_players_high = """
                            UPDATE players
                            SET highShots = highShots + 1
                            WHERE userID = '{}';
                            """.format(player1ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_high)
                        elif lowT == True:
                            update_players_low = """
                            UPDATE players
                            SET lowShots = lowShots + 1
                            WHERE userID = '{}';
                            """.format(player1ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_low)
                        update_players_miss = """
                        UPDATE players
                        SET miss = miss + 1
                        WHERE userID = '{}';
                        """.format(player2ID)
                        execute_query(create_connection('bpmsdatabase'), update_players_miss)
                        done = True
                    elif playerNum == "2":
                        if foreHandT == True:
                            update_players_foreHand = """
                            UPDATE players
                            SET foreHand = foreHand + 1
                            WHERE userID = '{}';
                            """.format(player2ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_foreHand)
                        elif backHandT == True:
                            update_players_backHand = """
                            UPDATE players
                            SET backHand = backHand + 1
                            WHERE userID = '{}';
                            """.format(player2ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_backHand)
                        if highT == True:
                            update_players_high = """
                            UPDATE players
                            SET highShots = highShots + 1
                            WHERE userID = '{}';
                            """.format(player2ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_high)
                        elif lowT == True:
                            update_players_low = """
                            UPDATE players
                            SET lowShots = lowShots + 1
                            WHERE userID = '{}';
                            """.format(player2ID)
                            execute_query(create_connection('bpmsdatabase'), update_players_low)
                        update_players_miss = """
                        UPDATE players
                        SET miss = miss + 1
                        WHERE userID = '{}';
                        """.format(player1ID)
                        execute_query(create_connection('bpmsdatabase'), update_players_miss)
                        done = True
            elif failureShotT == True:
                serveErrorT = serveError.get()
                outOfBoundsT = outOfBounds.get()
                didNotCrossNetT = didNotCrossNet.get()
                if playerNum == "1":
                    update_players_failure = """
                    UPDATE players
                    SET failure = failure + 1
                    WHERE userID = '{}';
                    """.format(player2ID)
                    execute_query(create_connection('bpmsdatabase'), update_players_failure)
                    done = True
                elif playerNum == "2":
                    update_players_failure = """
                    UPDATE players
                    SET failure = failure + 1
                    WHERE userID = '{}';
                    """.format(player1ID)
                    execute_query(create_connection('bpmsdatabase'), update_players_failure)
                    done = True
            elif foulT == True:
                doubleHitT = doubleHit.get()
                touchNetT = touchNet.get()
                otherT = other.get()
                if otherT == True:
                    reason = otherEnt.get()
                if playerNum == "1":
                    update_players_foul = """
                    UPDATE players
                    SET foul = foul + 1
                    WHERE userID = '{}';
                    """.format(player2ID)
                    execute_query(create_connection('bpmsdatabase'), update_players_foul)
                    done = True
                elif playerNum == "2":
                    update_players_foul = """
                    UPDATE players
                    SET foul = foul + 1
                    WHERE userID = '{}';
                    """.format(player1ID)
                    execute_query(create_connection('bpmsdatabase'), update_players_foul)
                    done = True
        if done == True:
            if player1score != 0:
                player1score -= 1
                successful_Shots.destroy()
                successfulShots("1",player1score,player2score,player1ID,player2ID)
            elif player1score == 0 and player2score != 0:
                player2score -= 1
                successful_Shots.destroy()
                successfulShots("2",player1score,player2score,player1ID,player2ID)
            else:
                messagebox.showinfo('Record Match Successful', 'The match is fully recorded.')

    #Labels
    topLineL = Label(successful_Shots,text = "How did player "+str(playerNum)+" score each point?",background="light blue")
    topLineL.place(x=25,y=25,anchor="w")
    oneL = Label(successful_Shots,text = "1. At player "+str(playerNum)+"'s half court",background="light blue")
    oneL.place(x=50,y=75,anchor="w")
    one1L = Label(successful_Shots,text = "1.",background="light blue")
    one1L.place(x=75,y=100,anchor="w")
    one2L = Label(successful_Shots,text = "2.",background="light blue")
    one2L.place(x=75,y=125,anchor="w")
    one3L = Label(successful_Shots,text = "3.",background="light blue")
    one3L.place(x=75,y=150,anchor="w")
    one4L = Label(successful_Shots,text = "4.",background="light blue")
    one4L.place(x=75,y=175,anchor="w")
    twoL = Label(successful_Shots,text = "2. To player "+str(playerNum)+"'s half court",background="light blue")
    twoL.place(x=50,y=200,anchor="w")
    two1L = Label(successful_Shots,text = "1.",background="light blue")
    two1L.place(x=75,y=225,anchor="w")
    two2L = Label(successful_Shots,text = "2.",background="light blue")
    two2L.place(x=75,y=250,anchor="w")
    two3L = Label(successful_Shots,text = "3.",background="light blue")
    two3L.place(x=75,y=275,anchor="w")
    secondOneL = Label(successful_Shots,text = "1.",background="light blue")
    secondOneL.place(x=50,y=325,anchor="w")
    secondTwoL = Label(successful_Shots,text = "2.",background="light blue")
    secondTwoL.place(x=50,y=350,anchor="w")
    secondTwo1L = Label(successful_Shots,text = "1.",background="light blue")
    secondTwo1L.place(x=75,y=375,anchor="w")
    secondThreeL = Label(successful_Shots,text = "3.",background="light blue")
    secondThreeL.place(x=50,y=400,anchor="w")
    thirdOneL = Label(successful_Shots,text = "1.",background="light blue")
    thirdOneL.place(x=50,y=450,anchor="w")
    #Checkbuttons
    hit = BooleanVar()
    hitCheck = Checkbutton(successful_Shots,text = "Hit (the other player missed)",background="light blue",variable=hit)
    hitCheck.place(x=50,y=50,anchor="w")
    failureShot = BooleanVar()
    failureShotCheck = Checkbutton(successful_Shots,text = "Player "+str(playerNum)+"'s failure shot",background="light blue",variable=failureShot)
    failureShotCheck.place(x=50,y=300,anchor="w")
    foul = BooleanVar()
    foulCheck = Checkbutton(successful_Shots,text = "Foul",background="light blue",variable=foul)
    foulCheck.place(x=50,y=425,anchor="w")
    foreHand = BooleanVar()
    foreHandCheck = Checkbutton(successful_Shots,text = "Forehand",background="light blue",variable=foreHand)
    foreHandCheck.place(x=100,y=100,anchor="w")
    backHand = BooleanVar()
    backHandCheck = Checkbutton(successful_Shots,text = "Backhand",background="light blue",variable=backHand)
    backHandCheck.place(x=225,y=100,anchor="w")
    overShoulder = BooleanVar()
    overShoulderCheck = Checkbutton(successful_Shots,text = "Over Shoulder",background="light blue",variable=overShoulder)
    overShoulderCheck.place(x=100,y=125,anchor="w")
    belowShoulder = BooleanVar()
    belowShoulderCheck = Checkbutton(successful_Shots,text = "Below Shoulder",background="light blue",variable=belowShoulder)
    belowShoulderCheck.place(x=225,y=125,anchor="w")
    backCourt1 = BooleanVar()
    backCourt1Check = Checkbutton(successful_Shots,text = "Backcourt",background="light blue",variable=backCourt1)
    backCourt1Check.place(x=100,y=150,anchor="w")
    foreCourt1 = BooleanVar()
    foreCourt1Check = Checkbutton(successful_Shots,text = "Forecourt",background="light blue",variable=foreCourt1)
    foreCourt1Check.place(x=225,y=150,anchor="w")
    midCourt1 = BooleanVar()
    midCourt1Check = Checkbutton(successful_Shots,text = "Midcourt",background="light blue",variable=midCourt1)
    midCourt1Check.place(x=350,y=150,anchor="w")
    leftCourt1 = BooleanVar()
    leftCourt1Check = Checkbutton(successful_Shots,text = "Leftcourt",background="light blue",variable=leftCourt1)
    leftCourt1Check.place(x=100,y=175,anchor="w")
    rightCourt1 = BooleanVar()
    rightCourt1Check = Checkbutton(successful_Shots,text = "Rightcourt",background="light blue",variable=rightCourt1)
    rightCourt1Check.place(x=225,y=175,anchor="w")
    backCourt2 = BooleanVar()
    backCourt2Check = Checkbutton(successful_Shots,text = "Backcourt",background="light blue",variable=backCourt2)
    backCourt2Check.place(x=100,y=225,anchor="w")
    foreCourt2 = BooleanVar()
    foreCourt2Check = Checkbutton(successful_Shots,text = "Forecourt",background="light blue",variable=foreCourt2)
    foreCourt2Check.place(x=225,y=225,anchor="w")
    midCourt2 = BooleanVar()
    midCourt2Check = Checkbutton(successful_Shots,text = "Midcourt",background="light blue",variable=midCourt2)
    midCourt2Check.place(x=350,y=225,anchor="w")
    leftCourt2 = BooleanVar()
    leftCourt2Check = Checkbutton(successful_Shots,text = "Leftcourt",background="light blue",variable=leftCourt2)
    leftCourt2Check.place(x=100,y=250,anchor="w")
    rightCourt2 = BooleanVar()
    rightCourt2Check = Checkbutton(successful_Shots,text = "Rightcourt",background="light blue",variable=rightCourt2)
    rightCourt2Check.place(x=225,y=250,anchor="w")
    high = BooleanVar()
    highCheck = Checkbutton(successful_Shots,text = "High",background="light blue",variable=high)
    highCheck.place(x=100,y=275,anchor="w")
    low = BooleanVar()
    lowCheck = Checkbutton(successful_Shots,text = "Low",background="light blue",variable=low)
    lowCheck.place(x=225,y=275,anchor="w")
    serveError = BooleanVar()
    serveErrorCheck = Checkbutton(successful_Shots,text = "Serve error",background="light blue",variable=serveError)
    serveErrorCheck.place(x=75,y=325,anchor="w")
    outOfBounds = BooleanVar()
    outOfBoundsCheck = Checkbutton(successful_Shots,text = "Out of bounds",background="light blue",variable=outOfBounds)
    outOfBoundsCheck.place(x=75,y=350,anchor="w")
    opponentCourt = BooleanVar()
    opponentCourtCheck = Checkbutton(successful_Shots,text = "Player "+str(opponentNum)+"'s court",background="light blue",variable=opponentCourt)
    opponentCourtCheck.place(x=100,y=375,anchor="w")
    ownCourt = BooleanVar()
    ownCourtCheck = Checkbutton(successful_Shots,text = "Player "+str(playerNum)+"'s court",background="light blue",variable=ownCourt)
    ownCourtCheck.place(x=225,y=375,anchor="w")
    didNotCrossNet = BooleanVar()
    didNotCrossNetCheck = Checkbutton(successful_Shots,text = "Did not cross the net",background="light blue",variable=didNotCrossNet)
    didNotCrossNetCheck.place(x=75,y=400,anchor="w")
    doubleHit = BooleanVar()
    doubleHitCheck = Checkbutton(successful_Shots,text = "Double Hit",background="light blue",variable=doubleHit)
    doubleHitCheck.place(x=75,y=450,anchor="w")
    touchNet = BooleanVar()
    touchNetCheck = Checkbutton(successful_Shots,text = "Touch the net",background="light blue",variable=touchNet)
    touchNetCheck.place(x=200,y=450,anchor="w")
    other = BooleanVar()
    otherCheck = Checkbutton(successful_Shots,text = "Other",background="light blue",variable=other)
    otherCheck.place(x=325,y=450,anchor="w")
    #Entries
    otherEnt = Entry(successful_Shots,bg="light blue",relief=RAISED)
    otherEnt.place(x=400,y=450,anchor="w")
    #Buttons
    nextShotButton = Button(successful_Shots,text = "next shot",command = lambda: nextShot(playerNum,player1score,player2score,player1ID,player2ID))
    nextShotButton.place(x=100,y=500,anchor="center")

    successful_Shots.mainloop()


###Player Profile Page (Each player account has an individual page)
def playerProfile(userID,personal):
    player_Profile = Tk()

    player_Profile.title("Badminton Performance Management - Player Profile")
    player_Profile.geometry("800x750")
    player_Profile.configure(background = "light blue")
    player_Profile.resizable(False,False)

    #Save changes to the entries: yearGroup, gender, and dominantHand.
    def saveChanges(userID):
        yearGroup = yearGroupEnt.get()
        gender = genderEnt.get()
        dominantHand = dominantHandEnt.get()
        save_changes = """
        UPDATE players
        SET yearGroup = '{}',
            gender = '{}',
            dominantHand = '{}'
        WHERE userID = '{}';
        """.format(yearGroup,gender,dominantHand,userID)
        execute_query(create_connection('bpmsdatabase'), save_changes)

    #Changes to the entries in player profile can only be saved if the profile is accessed from the player's account.
    if personal == True:
        #Buttons
        saveChangesBtn = Button(player_Profile,text = "Save Changes",command = lambda: saveChanges(userID))
        saveChangesBtn.place(x=600,y=50,anchor="center")
    
    #Take the player's information from the database
    userFirstName = selectPlayer('bpmsdatabase',userID)[0][1]
    userLastName = selectPlayer('bpmsdatabase',userID)[0][2]
    userYearGroup = selectPlayer('bpmsdatabase',userID)[0][3]
    userGender = selectPlayer('bpmsdatabase',userID)[0][4]
    userDominantHand = selectPlayer('bpmsdatabase',userID)[0][5]
    userScoreTotal = selectPlayer('bpmsdatabase',userID)[0][6]
    userScoreAve = selectPlayer('bpmsdatabase',userID)[0][7]
    userMatchTotal = selectPlayer('bpmsdatabase',userID)[0][8]
    userWonTotal = selectPlayer('bpmsdatabase',userID)[0][9]
    userForeHand= selectPlayer('bpmsdatabase',userID)[0][10]
    userBackHand = selectPlayer('bpmsdatabase',userID)[0][11]
    userHighShots = selectPlayer('bpmsdatabase',userID)[0][12]
    userLowShots = selectPlayer('bpmsdatabase',userID)[0][13]
    userForeCourt = selectPlayer('bpmsdatabase',userID)[0][14]
    userMidCourt = selectPlayer('bpmsdatabase',userID)[0][15]
    userBackCourt = selectPlayer('bpmsdatabase',userID)[0][16]
    userLeftCourt = selectPlayer('bpmsdatabase',userID)[0][17]
    userRightCourt = selectPlayer('bpmsdatabase',userID)[0][18]
    userMiss = selectPlayer('bpmsdatabase',userID)[0][19]
    userFailure = selectPlayer('bpmsdatabase',userID)[0][20]
    userFoul = selectPlayer('bpmsdatabase',userID)[0][21]
    #Lables
    firstNameL = Label(player_Profile,text = "First Name",background="light blue")
    firstNameL.place(x=125,y=75,anchor="e")
    lastNameL = Label(player_Profile,text = "Last Name",background="light blue")
    lastNameL.place(x=125,y=100,anchor="e")
    yearGroupL = Label(player_Profile,text = "Year Group",background="light blue")
    yearGroupL.place(x=125,y=125,anchor="e")
    genderL = Label(player_Profile,text = "Gender",background="light blue")
    genderL.place(x=125,y=150,anchor="e")
    dominantHandL = Label(player_Profile,text = "Dominant Hand",background="light blue")
    dominantHandL.place(x=125,y=175,anchor="e")
    scoreTotaoL = Label(player_Profile,text = "Total Score",background="light blue")
    scoreTotaoL.place(x=125,y=200,anchor="e")
    userScoreTotaoL = Label(player_Profile,text = str(userScoreTotal),background="light blue")
    userScoreTotaoL.place(x=250,y=200,anchor="e")
    scoreAveL = Label(player_Profile,text = "Average Score",background="light blue")
    scoreAveL.place(x=125,y=225,anchor="e")
    userScoreAveL = Label(player_Profile,text = str(userScoreAve),background="light blue")
    userScoreAveL.place(x=250,y=225,anchor="e")
    matchTotalL = Label(player_Profile,text = "Total Match",background="light blue")
    matchTotalL.place(x=125,y=250,anchor="e")
    userMatchTotalL = Label(player_Profile,text = str(userMatchTotal),background="light blue")
    userMatchTotalL.place(x=250,y=250,anchor="e")
    wonTotalL = Label(player_Profile,text = "Total Match Won",background="light blue")
    wonTotalL.place(x=125,y=275,anchor="e")
    userWonTotalL = Label(player_Profile,text = str(userWonTotal),background="light blue")
    userWonTotalL.place(x=250,y=275,anchor="e")
    successfulStats = Label(player_Profile,text = "Successful Shots Statistics",background="light blue")
    successfulStats.place(x=100,y=325,anchor="center")
    #Calculate percentages of successful shots.
    if userScoreTotal != 0:
        foreHandL = Label(player_Profile,text = "Forehand",background="light blue")
        foreHandL.place(x=100,y=350,anchor="center")
        userForeHandL = Label(player_Profile,text = str("%.2f"%((userForeHand/userScoreTotal)*100))+"%",background="light blue")
        userForeHandL.place(x=200,y=350,anchor="center")
        backHandL = Label(player_Profile,text = "Backhand",background="light blue")
        backHandL.place(x=300,y=350,anchor="center")
        userBackHandL = Label(player_Profile,text = str("%.2f"%((userBackHand/userScoreTotal)*100))+"%",background="light blue")
        userBackHandL.place(x=400,y=350,anchor="center")
        highShotsL = Label(player_Profile,text = "High Shots",background="light blue")
        highShotsL.place(x=100,y=375,anchor="center")
        userHighShotsL = Label(player_Profile,text = str("%.2f"%((userHighShots/userScoreTotal)*100))+"%",background="light blue")
        userHighShotsL.place(x=200,y=375,anchor="center")
        lowShotsL = Label(player_Profile,text = "Low Shots",background="light blue")
        lowShotsL.place(x=300,y=375,anchor="center")
        userLowShotsL = Label(player_Profile,text = str("%.2f"%((userLowShots/userScoreTotal)*100))+"%",background="light blue")
        userLowShotsL.place(x=400,y=375,anchor="center")
        foreCourtL = Label(player_Profile,text = "Fore Court",background="light blue")
        foreCourtL.place(x=100,y=400,anchor="center")
        userForeCourtL = Label(player_Profile,text = str("%.2f"%((userForeCourt/userScoreTotal)*100))+"%",background="light blue")
        userForeCourtL.place(x=200,y=400,anchor="center")
        midCourtL = Label(player_Profile,text = "Mid Court",background="light blue")
        midCourtL.place(x=300,y=400,anchor="center")
        userMidCourtL = Label(player_Profile,text = str("%.2f"%((userMidCourt/userScoreTotal)*100))+"%",background="light blue")
        userMidCourtL.place(x=400,y=400,anchor="center")
        backCourtL = Label(player_Profile,text = "Back Court",background="light blue")
        backCourtL.place(x=500,y=400,anchor="center")
        userBackCourtL = Label(player_Profile,text = str("%.2f"%((userBackCourt/userScoreTotal)*100))+"%",background="light blue")
        userBackCourtL.place(x=600,y=400,anchor="center") 
        leftCourtL = Label(player_Profile,text = "Left Court",background="light blue")
        leftCourtL.place(x=100,y=425,anchor="center")
        userLeftCourtL = Label(player_Profile,text = str("%.2f"%((userLeftCourt/userScoreTotal)*100))+"%",background="light blue")
        userLeftCourtL.place(x=200,y=425,anchor="center")
        rightCourtL = Label(player_Profile,text = "Right Court",background="light blue")
        rightCourtL.place(x=300,y=425,anchor="center")
        userRightCourtL = Label(player_Profile,text = str("%.2f"%((userRightCourt/userScoreTotal)*100))+"%",background="light blue")
        userRightCourtL.place(x=400,y=425,anchor="center")
    else:
        Label(player_Profile,text = "No successful shots recorded",background="light blue").place(x=100,y=350,anchor="w")
    unsuccessfulStats = Label(player_Profile,text = "Unsuccessful Shots Statistics",background="light blue")
    unsuccessfulStats.place(x=100,y=450,anchor="center")
    #Calculate percentages of unsuccessful shots.
    unsuccessfulShots = userMatchTotal*21-userScoreTotal
    if unsuccessfulShots != 0:
        missL = Label(player_Profile,text = "Miss",background="light blue")
        missL.place(x=100,y=475,anchor="center")
        userMissL = Label(player_Profile,text = str("%.2f"%((userMiss/unsuccessfulShots)*100))+"%",background="light blue")
        userMissL.place(x=200,y=475,anchor="center")
        failureL = Label(player_Profile,text = "Failure",background="light blue")
        failureL.place(x=300,y=475,anchor="center")
        userFailureL = Label(player_Profile,text = str("%.2f"%((userFailure/unsuccessfulShots)*100))+"%",background="light blue")
        userFailureL.place(x=400,y=475,anchor="center") 
        foulL = Label(player_Profile,text = "Foul",background="light blue")
        foulL.place(x=500,y=475,anchor="center")
        userFoulL = Label(player_Profile,text = str("%.2f"%((userFoul/unsuccessfulShots)*100))+"%",background="light blue")
        userFoulL.place(x=600,y=475,anchor="center")
    else:
        Label(player_Profile,text = "No unsuccessful shots recorded",background="light blue").place(x=100,y=475,anchor="w")
    #Entries
    playerFirstNameEnt = Entry(player_Profile,bg="light blue",relief=RAISED)
    playerFirstNameEnt.place(x=250,y=75,anchor="center")
    playerFirstNameEnt.insert(0, str(userFirstName))
    playerLastNameEnt = Entry(player_Profile,bg="light blue",relief=RAISED)
    playerLastNameEnt.place(x=250,y=100,anchor="center")
    playerLastNameEnt.insert(0, str(userLastName))
    yearGroupEnt = Entry(player_Profile,bg="light blue",relief=RAISED)
    yearGroupEnt.place(x=250,y=125,anchor="center")
    yearGroupEnt.insert(0, str(userYearGroup))
    genderEnt = Entry(player_Profile,bg="light blue",relief=RAISED)
    genderEnt.place(x=250,y=150,anchor="center")
    genderEnt.insert(0, str(userGender))
    dominantHandEnt = Entry(player_Profile,bg="light blue",relief=RAISED)
    dominantHandEnt.place(x=250,y=175,anchor="center")
    dominantHandEnt.insert(0, str(userDominantHand))

    player_Profile.mainloop()

###Match Profile Page (Each match has an individual page)
def matchProfile(matchName):
    match_Profile = Tk()

    match_Profile.title("Badminton Performance Management - Match Profile")
    match_Profile.geometry("400x400")
    match_Profile.configure(background = "light blue")
    match_Profile.resizable(False,False)

    #Lables
    matchNameL = Label(match_Profile,text = "Match Name:",bg="light blue")
    matchNameL.place(x=100,y=50,anchor="center")
    dateL = Label(match_Profile,text = "Date:",bg="light blue")
    dateL.place(x=100,y=75,anchor="center")
    linkL = Label(match_Profile,text = "Link:",bg="light blue")
    linkL.place(x=100,y=100,anchor="center")
    player1L = Label(match_Profile,text = "Player 1",background="light blue")
    player1L.place(x=100,y=125,anchor="center")
    player2L = Label(match_Profile,text = "Player 2",background="light blue")
    player2L.place(x=100,y=150,anchor="center")
    scoresL = Label(match_Profile,text = "Scores:",background="light blue")
    scoresL.place(x=100,y=175,anchor="center")
    matchSpec = selectMatch('bpmsdatabase',matchName)[0]
    Label(match_Profile, text=str(matchSpec[2]), background="light blue").place(x=250, y=50, anchor="center")
    Label(match_Profile, text=str(matchSpec[3]), background="light blue").place(x=250, y=75, anchor="center")
    Label(match_Profile, text=str(matchSpec[4]), background="light blue").place(x=250, y=100, anchor="center")
    Label(match_Profile, text=str(matchSpec[11]+" "+matchSpec[12]), background="light blue").place(x=250, y=125, anchor="center")
    Label(match_Profile, text=str(matchSpec[20]+" "+matchSpec[21]), background="light blue").place(x=250, y=150, anchor="center")
    Label(match_Profile, text=str(matchSpec[7])+" vs "+str(matchSpec[8]), background="light blue").place(x=250, y=175, anchor="center")

    match_Profile.mainloop()


###Procedure of the programm
def start():
    create_connection('bpmsdatabase')
    
    loginPage() #Start with opening the login page, the user chooses identity for different front page functions.


start()