import tkinter as tk
from tkinter import *
import mysql.connector

#initialize gui
root = tk.Tk()
root.title('LOL Auto Log')
root.geometry('')
canvas = tk.Canvas(root,width = 600,height = 300)
canvas.grid(rowspan=10)

#initialize sql connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='mason123',
    database='lol_val'
)

#create list of accounts (this will be replaced with a database query)
listbox = Listbox(root, font="Railway", bg="#C10D0D", fg="black", height=3, width=15)
listbox.grid(column=0, row=5)

cursor = conn.cursor()

cursor.execute("Select username from usernamepass")

usernames = []
for row in cursor:
    usernames.append(row[0])

cursor.close()

for username in usernames:
    listbox.insert(END, username)


def on_select(event):
    index = event.widget.curselection()[0]
    #add login function here


listbox.bind('<<ListboxSelect>>', on_select)   

root.mainloop()