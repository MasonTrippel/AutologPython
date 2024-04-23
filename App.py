import tkinter as tk
from tkinter import *
import mysql.connector
import hashlib
from tkinter import messagebox
import os
import subprocess
import time
import pyautogui

#initialize gui
root = tk.Tk()
root.title('LOL Auto Log')
root.geometry('')
canvas = tk.Canvas(root,width = 600,height = 300)
canvas.grid(rowspan=10)
currentGame = 'League'
dbCurrent = 'lol_val'
#initialize sql connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database= 'master'
)

hashedMasterPass = IntVar()
# Create username and password entry fields
username_var = StringVar()
password_var = StringVar()

username_entry = Entry(root, textvariable=username_var)
password_entry = Entry(root, textvariable=password_var, show='*')

username_entry.grid(column=0, row=0)
password_entry.grid(column=0, row=1)

def get_hash_code(input):
    result = subprocess.run(['GetHashCode.exe', input], capture_output=True, text=True)
    return int(result.stdout)

def decryptGamePassword(hashedPassword):
    global hashedMasterPass
    if hashedMasterPass < 0:
        hashedMasterPass *= -1

    while hashedMasterPass > 10:
        hashedMasterPass /= 10

    result = []

    for c in hashedPassword:
        x = chr(ord(c) - int(hashedMasterPass))
        result.append(x)
        hashedMasterPass += 1
    return ''.join(result)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def switch_game(game_db, listbox, game_name, label):
    
    label.config(text='Current Game: ' + game_name)
    # Switch the database
    conn.database = game_db
    cursor = conn.cursor()
    # Update the list of accounts
    cursor.execute("SELECT username FROM usernamepass")
    usernames = [row[0] for row in cursor]
    listbox.delete(0, END)
    for username in usernames:
        listbox.insert(END, username)
    global currentGame
    currentGame = game_name



def loginToGame(currentGame, listbox):
    if listbox is not None:
        username = listbox
    else:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT pass FROM usernamepass WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result is None:
        messagebox.showerror('Error', 'Invalid username or password')
    else:
        decryptGamePassword(result[0])
        if (dbCurrent == 'lol_val'):
            os.system('"C:\\Riot Games\\Riot Client\\RiotClientServices.exe"')
            time.sleep(5)
            pyautogui.write(username + '{TAB}')
            pyautogui.write(decryptGamePassword(result[0]) + '{ENTER}')
            if currentGame == 'League':
                for _ in range(7):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                for _ in range(7):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                
            elif currentGame == 'Valorant':
                for _ in range(9):
                    pyautogui.press('tab')
                pyautogui.press('enter')
                for _ in range(7):
                    pyautogui.press('tab')
                pyautogui.press('enter')
        else:
            os.system('C:\\Program Files (x86)\\Ubisoft\\Ubisoft Game Launcher\\UbisoftConnect.exe')
            time.sleep(8)
            pyautogui.write(username)
            pyautogui.press('tab')
            pyautogui.write(decryptGamePassword(result[0]))
            pyautogui.press('enter')    
            time.sleep(5)
            pyautogui.press('left')
            pyautogui.press('down')  
            pyautogui.press('enter') 
            pyautogui.press('right')
            pyautogui.press('down')
            pyautogui.press('enter') 
            pyautogui.press('enter') 
# Function to check username and password that also gives access to the list of accounts in the database
def check_credentials():
    
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username_var.get(),))
    result = cursor.fetchone()
    
    if result is None:
        messagebox.showinfo('Failure', 'Username not found')
    elif hash_password(password_var.get()) == result[0]:
        messagebox.showinfo('Success', 'Logged in successfully')
        conn.database = 'lol_val'
        #store the hashed master password and delete the plaintext version
        global hashedMasterPass
        hashedMasterPass = get_hash_code(password_var.get())
        password_entry.delete(0, END)

        #delete master login fields
        username_entry.destroy()
        password_entry.destroy()
        login_button.destroy()
        create_account_button.destroy()

        # Create list of accounts
        listbox = Listbox(root, font="Railway", bg="#C10D0D", fg="black", height=3, width=15, state='normal')
        listbox.grid(column=0, row=2)

        cursor.execute("Select username from usernamepass")

        usernames = []
        for row in cursor:
            usernames.append(row[0])            

    
        for username in usernames:
            listbox.insert(END, username)
                          
            #add login function here
            #add login function here

        #listbox.bind('<<ListboxSelect>>', on_select)  

        current_game_label = Label(root, text='Current Game: League', font="Railway", fg="black")
        current_game_label.grid(column=0, row=1)
        global currentGame
        game_login_button = Button(root, text='Login', command=lambda: loginToGame(currentGame, listbox.get(listbox.curselection())))
        game_login_button.grid(column=0, row=5) 
    
       
       
        switch_game('lol_val', listbox, 'League', current_game_label)

        
        league_button = Button(root, text='League', command=lambda: switch_game('lol_val',listbox, 'League', current_game_label))
        league_button.grid(column=0, row=2, sticky='w', padx=50) 

        valorant_button = Button(root, text='Valorant', command=lambda: switch_game('lol_val',listbox, 'Valorant', current_game_label))
        valorant_button.grid(column=0, row=3, sticky='w', padx=50)

        rainbow_button = Button(root, text='Rainbow 6', command=lambda: switch_game('r6',listbox, 'Rainbow 6', current_game_label))
        rainbow_button.grid(column=0, row=4, sticky='w', padx=50)

    else:
        messagebox.showerror('Error', 'Invalid username or password')
        
    cursor.close()

# Create login button
login_button = Button(root, text='Login', command=check_credentials)
login_button.grid(column=0, row=2)

def create_account(username, password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hash_password(password)))
    conn.commit()
    cursor.close()

    messagebox.showinfo('Success', 'Account created successfully')

def open_create_account_window():
    # Create a new window
    create_account_window = Toplevel(root)

    # Create StringVar objects for the new username and password
    new_username_var = StringVar()
    new_password_var = StringVar()

    # Create entry fields for the new username and password
    new_username_entry = Entry(create_account_window, textvariable=new_username_var)
    new_password_entry = Entry(create_account_window, textvariable=new_password_var, show='*')

    # Place the entry fields in the window
    new_username_entry.grid(column=0, row=0)
    new_password_entry.grid(column=0, row=1)

    # Create a "Create Account" button
    create_account_button = Button(create_account_window, text='Create Account', command=lambda: create_account(new_username_var.get(), new_password_var.get()))

    # Place the button in the window
    create_account_button.grid(column=0, row=2)


create_account_button = Button(root, text='Create Account', command=open_create_account_window)
create_account_button.grid(column=0, row=3)


root.mainloop()
