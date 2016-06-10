"""
    Created by: Takumi Iwasa
    Date:       17/05/2016
    
"""
import Main_engine
import os.path
import tkinter as tk
<<<<<<< HEAD

class ui_handler():
    def __init__(self, master=None):
        tk.Wm.title(master, "Aidan is bad")
        tk.Wm.minsize(master, 300, 400)
        self.frame = tk.Frame()
        self.frame.pack()
=======
import simpleaudio as sa

class ui_handler(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
>>>>>>> 231f0905f16104b0ac388119c3aface968f20c3a
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

<<<<<<< HEAD
        self.QUIT = tk.Button(text="QUIT", fg="red", command=root.destroy, relief="flat")
=======
        img = tk.PhotoImage(file="img01.pbm")
        label = tk.Button(image=img)
        label.image = img

        wave_object = sa.WaveObject.from_wave_file("simpleaudio/test_audio/c.wav")
        play = lambda: wave_object.play()
        label["command"] = play
        label.pack()

        self.QUIT = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
>>>>>>> 231f0905f16104b0ac388119c3aface968f20c3a
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
<<<<<<< HEAD
root.mainloop()
=======
app.mainloop()
>>>>>>> 231f0905f16104b0ac388119c3aface968f20c3a
