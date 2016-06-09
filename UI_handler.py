"""
    Created by: Takumi Iwasa
    Date:       17/05/2016
    
"""
import Main_engine
import os.path
import tkinter as tk

class ui_handler():
    def __init__(self, master=None):
        tk.Wm.title(master, "Aidan is bad")
        tk.Wm.minsize(master, 300, 400)
        self.frame = tk.Frame()
        self.frame.pack()
        self.create_button()
        self.frame.pack_forget()
        self.main_menu()


    def create_button(self):
        new_button = tk.Button()
        new_button["text"] = "Gab is BAD"
        new_button["command"] = self.aidan
        new_button["relief"] = "ridge"
        new_button["state"] = "normal"

        photo = tk.PhotoImage(file="img01.gif")
        new_button["image"] = photo
        new_button.image = photo

        new_button.pack(side="top")

        self.QUIT = tk.Button(text="QUIT", fg="red", command=root.destroy, relief="flat")
        self.QUIT.pack(side="bottom")

    def main_menu(self):
        main_menu_frame = tk.Frame()
        start_button = tk.Button(main_menu_frame, text="1")
        start_button.pack()
        option_button = tk.Button(main_menu_frame, text="2")
        exit_button = tk.Button(main_menu_frame, text="3")
        main_menu_frame.pack() 

    def aidan(self):
        print("Aidan is also bad")


root = tk.Tk()
app = ui_handler(master=root)
root.mainloop()
