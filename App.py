import tkinter as tk
from tkinter import *
import mysql.connector
import hashlib
from tkinter import messagebox

#initialize gui
root = tk.Tk()
root.title('LOL Auto Log')
root.geometry('')
canvas = tk.Canvas(root,width = 600,height = 300)
canvas.grid(rowspan=10)

dbCurrent = 'lol_val'
#initialize sql connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password123',
    database= 'master'
)




# Create username and password entry fields
username_var = StringVar()
password_var = StringVar()

username_entry = Entry(root, textvariable=username_var)
password_entry = Entry(root, textvariable=password_var, show='*')

username_entry.grid(column=0, row=0)
password_entry.grid(column=0, row=1)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check username and password

def check_credentials():
    
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username_var.get(),))
    result = cursor.fetchone()

    if result is None:
        messagebox.showinfo('Failure', 'Username not found')
    elif hash_password(password_var.get()) == result[0]:
        messagebox.showinfo('Success', 'Logged in successfully')
        conn.database = 'lol_val'
        # Create list of accounts
        listbox = Listbox(root, font="Railway", bg="#C10D0D", fg="black", height=3, width=15, state='normal')
        listbox.grid(column=0, row=5)

        cursor.execute("Select username from usernamepass")

        usernames = []
        for row in cursor:
            usernames.append(row[0])            

    
        for username in usernames:
            listbox.insert(END, username)


        def on_select(event):
            index = event.widget.curselection()[0]
            #add login function here


        listbox.bind('<<ListboxSelect>>', on_select)   
    


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