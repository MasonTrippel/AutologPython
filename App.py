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