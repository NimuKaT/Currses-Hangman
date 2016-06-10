"""
    Created by: Takumi Iwasa
    Date:       17/05/2016
    
"""
import os.path
import tkinter as tk
class ui_handler(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack
        self.create_button()

    def create_button(self):
        new_button = tk.Button(self)
        new_button["text"] = "Gab is BAD"
        new_button["command"] = self.aidan
        new_button.pack(side="top")

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.QUIT.pack(side="bottom")

    def aidan(self):
        print("Aidan is also bad")
root = tk.Tk()
app = ui_handler(master=root)
app.mainloop()
