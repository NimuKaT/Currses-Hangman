"""
    Created by: Takumi Iwasa
    Date:       17/05/2016
    
"""
import os.path
import tkinter as tk
from tkinter.font import Font
import simpleaudio as sa
import time
import Main_engine
from enum import Enum

class AUDIO(Enum):
    #Values for music
    MENU_MUSIC = 0,
    GAME_MUSIC = 1,

    #Values for sound effects
    DEFAUL_BUTTON_SE = 2,
    GAME_WIN_SE = 3,
    GAME_LOSE_SE = 4
    IN_WORD = 5,
    NOT_IN_WORD = 6,


class ui_handler():
    def __init__(self, master=None):
        #Configuration for the master window
        master.title('Hangman')
        master.minsize(1330, 720)
        master.maxsize(1920, 1080)

        self.test_font = Font(family='Comic Sans', size=30)
       
        self.play_obj = []
        self.music_loop_obj = None
        self.current_audio = 0
        self.playing_audio_loop = 0
        
        self.load_audio()
        self.load_images()
        
        self.game = Main_engine.game_logic()
        self.is_play_music_loop = self.game.return_options('Music')
        self.is_play_sound_effect = self.game.return_options('Sound_effects')
        self.is_game_running = False
        self.current_frame = None
        self.master = master
        self.game_end = False
        self.frames =  {}
        self.toggle_music_loop_button = tk.Button(master, text='music', command=self.toggle_music, relief='groove')
        self.toggle_sound_effect_button = tk.Button(master, text='SE', command=self.toggle_sound_effect, relief='solid')
        self.audio_control()
        self._main_menu()

    def load_audio(self):
        self.wave_obj = {}
        self.wave_obj[AUDIO.MENU_MUSIC] = sa.WaveObject.from_wave_file('Assets/audio/nyan.wav')
        self.wave_obj[AUDIO.GAME_MUSIC] = sa.WaveObject.from_wave_file('simpleaudio/test_audio/notes_2_16_44.wav')
        self.wave_obj[AUDIO.DEFAUL_BUTTON_SE] = sa.WaveObject.from_wave_file('Assets/audio/Blop_Mark_DiAngelo_79054334.wav')
        self.wave_obj[AUDIO.GAME_WIN_SE] = sa.WaveObject.from_wave_file('simpleaudio/test_audio/e.wav')
        self.wave_obj[AUDIO.GAME_LOSE_SE] = sa.WaveObject.from_wave_file('simpleaudio/test_audio/g.wav')


    def load_images(self):
        self.Images = {}
        self.Images['Play_button'] = tk.PhotoImage(file='Assets/Image/Play_button.pbm')
        self.Images['Sound_effects_play'] = tk.PhotoImage(file='Assets/Image/Speaker_icon.pbm')
        self.Images['Sound_effects_mute'] = tk.PhotoImage(file='Assets/Image/Mute_icon.pbm')
        self.Images['music_play'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver.pbm')
        self.Images['music_mute'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver_mute.pbm')
        for i in range(1, 9):
            path = 'Hangman_{}'.format(i)
            self.Images[path] = tk.PhotoImage(file='Assets/Image/{}.pbm'.format(path))
            


    def audio_control(self):
        #Updates the image for the music and SE button according to their state
        #Both are updated to keep them in order
        if self.is_play_music_loop == 'True':
            self.toggle_music_loop_button['image'] = self.Images['music_play']
        else:
            self.toggle_music_loop_button['image'] = self.Images['music_mute']
        self.toggle_music_loop_button.pack(side='left', anchor='nw')

        if self.is_play_sound_effect == 'True':
            self.toggle_sound_effect_button['image'] = self.Images['Sound_effects_play']
        else:
            self.toggle_sound_effect_button['image'] = self.Images['Sound_effects_mute']
        self.toggle_sound_effect_button.pack(side='left', anchor='nw')

    def _main_menu(self):
        self.frames['main'] = tk.Frame()

        self.current_audio = AUDIO.MENU_MUSIC

        word_length_opt = [
            '6',
            '7',
            '8',
            '9',
            '10'
        ]

        current_length = tk.StringVar(self.frames['main'])
        current_length.set(str(self.game.return_options('Word_length')))
        word_lenght = tk.OptionMenu(self.frames['main'], current_length, *word_length_opt)
        word_lenght.pack()


        play_button = tk.Button(self.frames['main'],text='Play',
            command=lambda: (self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._game_menu()),
            relief='flat',
            image=self.Images['Play_button'])
        play_button.image = self.Images['Play_button']
        play_button.pack()

        option_button = tk.Button(self.frames['main'],
            text='Options',
            relief='flat',
            state='disabled',
            font=self.test_font)
        option_button.pack()

        instruction_button = tk.Button(self.frames['main'],
            text='Instructions',
            relief='flat',
            state='disabled',
            font=self.test_font)
        instruction_button.pack()

        exit_button = tk.Button(self.frames['main'],
            text='Exit',
            relief='flat',
            command=lambda:(quit()),
            font=self.test_font)
        exit_button.pack()

        self.frames['main'].pack()

    def _instruction_menu(self):
        frame = tk.Frame()
        frame.pack()

    def music_loop(self):
        #
        if self.is_play_music_loop == 'True':
            if (self.playing_audio_loop == self.current_audio):  
                if isinstance(self.music_loop_obj, sa.PlayObject):
                    if (not self.music_loop_obj.is_playing()):
                        self.music_loop_obj = self.wave_obj[self.current_audio].play()
            else:
                if isinstance(self.music_loop_obj, sa.PlayObject):
                    self.music_loop_obj.stop()
                self.music_loop_obj = self.wave_obj[self.current_audio].play()
                self.playing_audio_loop = self.current_audio
        elif (isinstance(self.music_loop_obj, sa.PlayObject)):
            if self.music_loop_obj.is_playing():
                self.music_loop_obj.stop()
            
    def _game_menu(self):
        self.current_audio = AUDIO.GAME_MUSIC
        self.current_frame = "Game"

        self.frames['game'] = tk.Frame(height=100, width=100)
        self.frames['game'].bind_all('<Key>', self._game_input)
        self.game.start()
        self.game_end = False
        
        self.hangman_label = tk.Label(self.frames['game'],
            relief='solid')
        self.update_hangman()
        self.hangman_label.pack()

        self.mystery_word = tk.StringVar()
        self.mystery_word.set(self.game.get_mystery_word())

        mystery_word_label = tk.Label(self.frames['game'],
            textvariable=self.mystery_word,
            font=self.test_font)
        mystery_word_label.pack()

        self.error = tk.StringVar()
        error_label = tk.Label(self.frames['game'], textvariable=self.error, fg='red')
        error_label.pack()

        self.guessed_word_labelframe = tk.LabelFrame(self.frames['game'], relief='flat')
        
        self.guessed_word_labels = {}
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
            self.guessed_word_labels[chr(97+i)] = tk.Label(self.guessed_word_labelframe, text=chr(97+i), state=status, font=self.test_font)
            self.guessed_word_labels[chr(97+i)].grid(column=col,row=row)
        self.guessed_word_labelframe.pack()

        back_button = tk.Button(self.frames['game'],text='Back',
            relief='flat',
            command=lambda:(self.frames['game'].pack_forget(),self._main_menu()),
            font=self.test_font)

        back_button.pack()

        self.frames['game'].pack()
        
    def _game_input(self, event):
        if (not self.game.check_user_input(event.char)):
            self.error.set("{} is not a valid character".format(event.char))
        else:
            if (ord(event.char) >= ord('a') and ord(event.char) <= ord('z')):
                input = event.char
            elif  (ord(event.char) >= ord('A') and ord(event.char) <= ord('Z')):
                input = chr(97+ord(event.char)-65 )
            if (self.game.is_guessed(input)):
                self.error.set("{} is already guessed".format(input))
            else:
                if (self.game.check_word(input)):
                    self.mystery_word.set(self.game.get_mystery_word())
                    self.guessed_word_labels[input] = tk.Label(self.guessed_word_labelframe, text=input, fg='green', font=self.test_font)
                else:
                    self.error.set("{} is not in word".format(input))
                    self.guessed_word_labels[input] = tk.Label(self.guessed_word_labelframe, text=input, fg='red', font=self.test_font)
                char_num = ord(input) - 97
                if char_num > 12:
                    row = 1
                    col = char_num-13
                else:
                    row = 0
                    col = char_num
                self.guessed_word_labels[input].grid(column=col, row=row)
        if (self.current_frame == 'Game' and not self.game_end):
            if (self.game.is_win() or self.game.is_lose()):
                self.frames['game'].pack_forget()
                self.result_menu(self.game.is_win())
                self.game_end = True
        self.update_hangman()
        time.sleep(0.1)
                 
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
            self.wave_obj[AUDIO.DEFAUL_BUTTON_SE].play(),
            self._game_menu()),
            relief='flat')

        play_again_button.pack()

        back_to_menu_button = tk.Button(frame, text="Back to main menu",
            command=lambda: (frame.pack_forget(), self._main_menu()),
            relief="flat")
        back_to_menu_button.pack(side="top")

        frame.pack()

    def toggle_music(self):
        if self.is_play_music_loop == 'True':
            self.is_play_music_loop = 'False'
        else:
            self.is_play_music_loop = 'True'
        self.game.change_options('Music', self.is_play_music_loop)
        self.audio_control()

    def play_sound_effect(self, key):
        if (self.is_play_sound_effect == 'True'):
            self.play_obj.append(self.wave_obj[key].play())

    def toggle_sound_effect(self):
        if self.is_play_sound_effect == 'True':
            self.is_play_sound_effect = 'False'
            for se in self.play_obj:
                se.stop()
            self.play_obj.clear()
        else:
            self.is_play_sound_effect = 'True'
        self.game.change_options('Sound_effects', self.is_play_sound_effect)
        self.audio_control()

    def update_hangman(self):
        img_num = self.game.return_count()
        if img_num <= 7:
            current_hangman = 'Hangman_{}'.format(self.game.return_count()+1)
            self.hangman_label['image'] = self.Images[current_hangman]
            self.hangman_label.image = self.Images[current_hangman]
            self.hangman_label.pack()
        



#Initializes a global variable and function to exit the main loop of tkinter
global exit
exit = False
def quit():
    global exit
    exit = True

#Assigns root as the Top-Level window and binds the exit protocol to the global
#exit function to prevent tkinter from sending errors
root = tk.Tk()
root.protocol('WM_DELETE_WINDOW', quit)

#Initialize the application while passing the root window so the application can 
#assign images into the window
app = ui_handler(master=root)

#Main loop of tkinter with the update calls for the application
while not exit:
    app.music_loop()
    root.update_idletasks()
    root.update()
    time.sleep(0.01)
root.destroy()