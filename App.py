import tkinter as tk
from tkinter import *
import mysql.connector

root = tk.Tk()
root.title('LOL Auto Log')
root.geometry('')

listbox = Listbox(root, font="Railway", bg="#C10D0D", fg="black", height=3, width=15)
listbox.grid(column=0, row=2)


accounts = ["Trippelindy", "Trippy", "SKTDopa"]
for account in accounts:
    listbox.insert(END, account)


def on_select(event):
    index = event.widget.curselection()[0]
    



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