"""
    Created by: Takumi Iwasa
    Date:       17/05/2016
    
"""
import os.path
import tkinter as tk
import simpleaudio as sa
import time
import Main_engine

class ui_handler():
    def __init__(self, master=None):
        tk.Wm.title(master, 'Hangman')
        self.wave_obj = sa.WaveObject.from_wave_file('simpleaudio/test_audio/c.wav')
        self.audios = None
        self.game = Main_engine.game_logic()
        self.is_game_running = False
        self.current_frame = None
        self.master = master
        self.ran = False
        self.frames =  {}
        self._main_menu()

    def _main_menu(self):
        self.frames['main'] = tk.Frame()

        play_button = tk.Button(self.frames['main'],text='Play',
            command=lambda: (self.frames['main'].pack_forget(),
            self.wave_obj.play(),
            self._game_menu()),
            relief='flat')

        play_button.pack()

        option_button = tk.Button(self.frames['main'],text='Options',
            relief='flat', state='disabled')
        option_button.pack()

        instruction_button = tk.Button(self.frames['main'],text='Instructions',
            relief='flat', state='disabled')
        instruction_button.pack()

        exit_button = tk.Button(self.frames['main'],text='Exit',
            relief='flat',
            command=exit)
        exit_button.pack()

        self.frames['main'].pack()

    def _instruction_menu(self):
        frame = tk.Frame()
        frame.pack()

    def _test_menu(self):
        self.frames['main'] = tk.Frame()

        self.label1_str = tk.StringVar()
        self.label1_str.set("Test label 1")

        label1 = tk.Label(frame,
            textvariable=self.label1_str)
        label1.bind("<Button-1>", self._test_func)
        label1.pack()

        frame.pack()

    def _test_func(self, event):
        self.label1_str.set("clicked at x:{0} y:{1}".format(event.x, event.y))

    def music_loop(self):
        if isinstance(self.audios, sa.PlayObject):
            if (not self.audios.is_playing()):
                self.audios = self.wave_obj.play()
        else:
            self.audios = self.wave_obj.play()
            
    def _game_menu(self):
        self.current_frame = "Game"
        self.ran = False
        self.frames['game'] = tk.Frame(height=100, width=100)
        self.game.start()

        self.frames['game'].bind_all('<Key>', self._game_input)

        self.mystery_word = tk.StringVar()
        mystery_word_label = tk.Label(self.frames['game'], textvariable=self.mystery_word)
        self.mystery_word.set(self.game.get_mystery_word())
        mystery_word_label.pack()

        self.error = tk.StringVar()
        error_label = tk.Label(self.frames['game'], textvariable=self.error, fg='red')
        error_label.pack()

        guessed_word_labelframe = tk.LabelFrame(self.frames['game'], relief='flat')
        guessed_word_labels = {}
        for i in range(26):
            if i > 12:
                row = 1
                col = i-13
            else:
                row = 0
                col = i

            status = 'normal'
            if (self.game.get_guessed_char()[chr(97+i)]):
                status = 'disabled'
            guessed_word_labels[chr(97+i)] = tk.Label(guessed_word_labelframe, text=chr(97+i), state=status)
            guessed_word_labels[chr(97+i)].grid(column=col,row=row)
        guessed_word_labelframe.pack()

        back_button = tk.Button(self.frames['game'],text='Back',
            relief='flat', command=lambda: (self.frames['game'].pack_forget(), self._main_menu()))
        back_button.pack()

        self.frames['game'].pack()
        
    def _game_input(self, event):
        if (not self.game.check_user_input(event.char)):
            self.error.set("{} is not a valid character".format(event.char))
        elif (self.game.is_guessed(event.char)):
            self.error.set("{} is already guessed".format(event.char))
        elif (self.game.check_word(event.char)):
            self.mystery_word.set(self.game.get_mystery_word())
        else:
           self.error.set("{} is not in word".format(event.char))
            
    def check_game(self):
        
        if (self.current_frame == 'Game' and not self.ran):
            if (self.game.is_win() or self.game.is_lose()):
                self.frames['game'].pack_forget()
                self.result_menu(self.game.is_win())
                self.ran = True

    def result_menu(self, win):
        frame = tk.Frame()
        result_str = tk.StringVar()
        result_label = tk.Label(frame, textvariable=result_str)
        if win:
            result_str.set('Congratulation! You guessed the word: {}'.format(self.game.cur_word))
        else:
            result_str.set('you lose! The word was: {}'.format(self.game.cur_word))
        result_label.pack()

        play_again_button = tk.Button(frame,text='Play again',
            command=lambda: (frame.pack_forget(),
            self.wave_obj.play(),
            self._game_menu()),
            relief='flat')

        play_again_button.pack()

        back_to_menu_button = tk.Button(frame, text="Back to main menu",
            command=lambda: (frame.pack_forget(), self._main_menu()),
            relief="flat")
        back_to_menu_button.pack(side="top")

        frame.pack()
global exit
def quit():
    exit = True
exit = False
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', quit)
app = ui_handler(master=root)
while not exit:
    #app.music_loop()
    app.check_game()
    root.update_idletasks()
    root.update()
    time.sleep(0.01)
