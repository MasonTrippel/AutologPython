from tkinter import *

class Application:
    def __init__(self, master=None):
        self.master = master
        self.label = Label(text="Hello Tkinter")
        self.label.pack()

if __name__ == "__main__":
    root = Tk()
    app = Application(master=root)
    root.mainloop()