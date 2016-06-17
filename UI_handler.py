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

        self.master = master
        self.button_font = Font(family='Century', size=30)
        self.game = Main_engine.game_logic()
        self.is_play_music_loop = self.game.return_options('Music')
        self.is_play_sound_effect = self.game.return_options('Sound_effects')
        self.play_obj = []
        self.music_loop_obj = None
        self.current_audio = 0
        self.playing_audio_loop = 0
        self.game_end = False
        self.frames =  {}
        
        self.load_audio()
        self.load_images()
 
        self.toggle_music_loop_button = tk.Button(master,
            text='music',
            command=self.toggle_music,
            relief='groove'
            )
        self.toggle_sound_effect_button = tk.Button(master,
            text='SE',
            command=self.toggle_sound_effect,
            relief='solid'
            )
        self.audio_control()
        self._main_menu()

    def load_audio(self):
        #loads all music file in a dictionary 'WAVE_OBJ'
        self.WAVE_OBJ = {}
        self.WAVE_OBJ[AUDIO.MENU_MUSIC] = sa.WaveObject.from_wave_file('Assets/audio/Lobby_music.wav')
        self.WAVE_OBJ[AUDIO.GAME_MUSIC] = sa.WaveObject.from_wave_file('Assets/audio/Game_music.wav')
        self.WAVE_OBJ[AUDIO.DEFAUL_BUTTON_SE] = sa.WaveObject.from_wave_file('Assets/audio/Blop_Mark_DiAngelo_79054334.wav')
        self.WAVE_OBJ[AUDIO.GAME_WIN_SE] = sa.WaveObject.from_wave_file('simpleaudio/test_audio/e.wav')
        self.WAVE_OBJ[AUDIO.GAME_LOSE_SE] = sa.WaveObject.from_wave_file('simpleaudio/test_audio/g.wav')

    def music_loop(self):
        #Is called by the main loop and runs the selected music under 'current_audio'
        #if 'is_play_music_loop' is true. It re-initializes the PlayObject if is
        #has finished running as 'music_loop_obj'
        if self.is_play_music_loop == 'True':
            #Checks whether the selected audio track under 'current_audio' is equal
            #to that of the 'playing_audio_loop' and if not terminates the current
            #loop and initializes the selected one as 'music_loop_obj'
            if (self.playing_audio_loop == self.current_audio):  
                if isinstance(self.music_loop_obj, sa.PlayObject):
                    if (not self.music_loop_obj.is_playing()):
                        self.music_loop_obj = self.WAVE_OBJ[self.current_audio].play()
            else:
                if isinstance(self.music_loop_obj, sa.PlayObject):
                    self.music_loop_obj.stop()
                self.music_loop_obj = self.WAVE_OBJ[self.current_audio].play()
                self.playing_audio_loop = self.current_audio
        #If the PlayObject instance exists terminates the audio 
        elif (isinstance(self.music_loop_obj, sa.PlayObject)):
            if self.music_loop_obj.is_playing():
                self.music_loop_obj.stop()

    def play_sound_effect(self, key):
        #If sound effects are not turned off, appends the PlayObject into play_obj
        #Which can later be used to terminate when toggled off
        if (self.is_play_sound_effect == 'True'):
            self.play_obj.append(self.WAVE_OBJ[key].play())
   
    def audio_control(self):
        #Updates the image for the music and SE button according to their state
        #Both are updated to keep them in order
        if self.is_play_music_loop == 'True':
            self.toggle_music_loop_button['image'] = self.IMAGES['music_play']
        else:
            self.toggle_music_loop_button['image'] = self.IMAGES['music_mute']
        self.toggle_music_loop_button.pack(side='left', anchor='nw')

        if self.is_play_sound_effect == 'True':
            self.toggle_sound_effect_button['image'] = self.IMAGES['Sound_effects_play']
        else:
            self.toggle_sound_effect_button['image'] = self.IMAGES['Sound_effects_mute']
        self.toggle_sound_effect_button.pack(side='left', anchor='nw')

    def toggle_music(self):
        #Toggles music on and off which allows 'music_loop' to play or stop music
        #when necessary
        if self.is_play_music_loop == 'True':
            self.is_play_music_loop = 'False'
        else:
            self.is_play_music_loop = 'True'
        self.game.change_options('Music', self.is_play_music_loop)
        #Calls 'audio_control' to update the images of the button
        self.audio_control()

    def toggle_sound_effect(self):
        #When called toggles the sound effects on and off terminating all currently
        #running sound effects only
        if self.is_play_sound_effect == 'True':
            self.is_play_sound_effect = 'False'
            for se in self.play_obj:
                se.stop()
            self.play_obj.clear()
        else:
            self.is_play_sound_effect = 'True'
        #Inserts the changes into the options file and into the dictionary 'options'
        self.game.change_options('Sound_effects', self.is_play_sound_effect)
        #Calls to update the images of the buttons
        self.audio_control()





    def load_images(self):
        #loads all the image files in to a dictionary 'IMAGES'
        self.IMAGES = {}
        self.IMAGES['Play_button'] = tk.PhotoImage(file='Assets/Image/Play_button.pbm')
        self.IMAGES['Sound_effects_play'] = tk.PhotoImage(file='Assets/Image/Speaker_icon.pbm')
        self.IMAGES['Sound_effects_mute'] = tk.PhotoImage(file='Assets/Image/Mute_icon.pbm')
        self.IMAGES['music_play'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver.pbm')
        self.IMAGES['music_mute'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver_mute.pbm')
        self.IMAGES['instructions'] = tk.PhotoImage(file='Assets/Image/Instructions.pbm')
        self.IMAGES['Logo'] = tk.PhotoImage(file='Assets/Image/Hangman_8.pbm')
        for i in range(1, 9):
            path = 'Hangman_{}'.format(i)
            self.IMAGES[path] = tk.PhotoImage(file='Assets/Image/{}.pbm'.format(path))
            

    
    def _main_menu(self):
        self.frames['main'] = tk.Frame()
        self.frames['main'].pack()

        self.current_audio = AUDIO.MENU_MUSIC

        game_logo = tk.Label(
            self.frames['main'],
            image=self.IMAGES['Logo'])
        game_logo.image = self.IMAGES['Logo']
        game_logo.pack()

        game_start_lable_frame = tk.LabelFrame(self.frames['main'])
        game_start_lable_frame.pack()

        word_length_opt = [
            '6',
            '7',
            '8',
            '9',
            '10',
            '11',
            '12',
            '13',
            '14',
            '15',
            ]

        self.current_length = tk.StringVar(self.frames['main'])
        self.current_length.set(self.game.return_options('Word_length'))

        word_lenght = tk.OptionMenu(game_start_lable_frame,
            self.current_length,
            *word_length_opt
            )
        word_lenght.pack(side='right')


        play_button = tk.Button(
            game_start_lable_frame,
            text='Play',
            command=lambda: (self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._word_len_opt(),
            self._game_menu()),
            relief='flat',
            image=self.IMAGES['Play_button']
            )
        play_button.image = self.IMAGES['Play_button']
        play_button.pack(side='left')

        option_button = tk.Button(
            self.frames['main'],
            text='Options',
            relief='flat',
            state='disabled',
            font=self.button_font,
            )
        option_button.pack()

        instruction_button = tk.Button(
            self.frames['main'],
            text='Instructions',
            relief='flat',
            state='active',
            font=self.button_font,
            command=lambda:(self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._instruction_menu())
            )
        instruction_button.pack()

        exit_button = tk.Button(self.frames['main'],
            text='Exit',
            relief='flat',
            command=lambda:(quit()),
            font=self.button_font
            )
        exit_button.pack()

        

    def _word_len_opt(self):
        new_length =  self.current_length.get()
        self.game.change_options('Word_length', new_length)


    def _instruction_menu(self):
        self.frames['instructions'] = tk.Frame()
        self.frames['instructions'].pack()

        instruction_image_label = tk.Label(self.frames['instructions'],
            image=self.IMAGES['instructions'],
            relief='solid')
        instruction_image_label.pack()

        back_main_menu_button = tk.Button(self.frames['instructions'], text="Back to main menu",
            command=lambda:(self.frames['instructions'].pack_forget(),
             self._main_menu()),
            relief="flat")
        back_main_menu_button.pack(
            side="bottom",
            anchor='sw'
            )


    
            
    def _game_menu(self):
        self.current_audio = AUDIO.GAME_MUSIC
        self.frames['game'] = tk.Frame(height=100, width=100)
        self.frames['game'].bind_all('<Key>', self._game_input)
        self.frames['game'].pack()
        self.game.start()
        self.game_end = False

        self.hangman_label = tk.Label(
            self.frames['game'],
            relief='solid'
            )
        self.update_hangman()
        self.hangman_label.pack()

        self.mystery_word = tk.StringVar(self.frames['game'])
        self.mystery_word.set(self.game.get_mystery_word())

        mystery_word_label = tk.Label(
            self.frames['game'],
            textvariable=self.mystery_word,
            font=self.button_font
            )
        mystery_word_label.pack()

        self.error = tk.StringVar(self.frames['game'])
        error_label = tk.Label(
            self.frames['game'],
            textvariable=self.error,
            fg='red'
            )
        error_label.pack()

        self.guessed_word_labelframe = tk.LabelFrame(
            self.frames['game'],
            relief='flat'
            )
        self.guessed_word_labelframe.pack()

        self.guessed_word_labels = {}
        for i in range(26):
            if i > 12:
                row = 1
                col = i-13
            else:
                row = 0
                col = i
            self.guessed_word_labels[chr(97+i)] = tk.Label(
                self.guessed_word_labelframe,
                text=chr(97+i),
                font=self.button_font
                )
            self.guessed_word_labels[chr(97+i)].grid(column=col,row=row)
        

        back_button = tk.Button(
            self.frames['game'],
            text='Back',
            relief='groove',
            command=lambda:(self.frames['game'].pack_forget(),
                self._main_menu()),
            font=self.button_font
            )

        back_button.pack()

        
        
    def _game_input(self, event):
        input = event.char.lower()
        if (not self.game.check_user_input(event.char)):
            self.error.set("{} is not a valid character".format(event.char))
        else:
            if (self.game.is_guessed(input)):
                self.error.set("{} is already guessed".format(input))
            else:
                if (self.game.check_word(input)):
                    self.mystery_word.set(self.game.get_mystery_word())
                    self.guessed_word_labels[input] = tk.Label(self.guessed_word_labelframe, text=input, fg='green', font=self.button_font)
                else:
                    self.error.set("{} is not in word".format(input))
                    self.guessed_word_labels[input] = tk.Label(self.guessed_word_labelframe, text=input, fg='red', font=self.button_font)
                char_num = ord(input) - 97
                if char_num > 12:
                    row = 1
                    col = char_num-13
                else:
                    row = 0
                    col = char_num
                self.guessed_word_labels[input].grid(column=col, row=row)
        if (not self.game_end):
            if (self.game.is_win() or self.game.is_lose()):
                self.frames['game'].pack_forget()
                self.result_menu(self.game.is_win())
                self.game_end = True
        self.update_hangman()
        time.sleep(0.1)
                 
    def result_menu(self, win):
        self.frames['result'] = tk.Frame()
        result_str = tk.StringVar()
        result_label = tk.Label(
            self.frames['result'],
            textvariable=result_str,
            font=self.button_font)
        if win:
            result_str.set('Congratulation! You guessed the word: {}'.format(self.game.cur_word))
            result_label.config(fg='green')
        else:
            result_str.set('you lose! The word was: {}'.format(self.game.cur_word))
            result_label.config(fg='red')
            loss_image = tk.Label(self.frames['result'],
                image=self.IMAGES['Hangman_8'])
            loss_image.pack()
        result_label.pack()

        play_again_button = tk.Button(self.frames['result'],text='Play again',
            command=lambda: (self.frames['result'].pack_forget(),
            self.WAVE_OBJ[AUDIO.DEFAUL_BUTTON_SE].play(),
            self._game_menu()),
            relief='groove',
            font=self.button_font
            )
        play_again_button.pack()

        back_to_menu_button = tk.Button(
            self.frames['result'],
            text="Back to main menu",
            command=lambda:(
                self.frames['result'].pack_forget(),
                self._main_menu()),
            relief="groove",
            font=self.button_font
            )
        back_to_menu_button.pack(side="top")

        self.frames['result'].pack()

    
    def update_hangman(self):
        #Changes the hangman image displayed in the game frame according to the
        #number of wrong guesses
        img_num = self.game.return_count()
        if img_num <= 7:
            current_hangman = 'Hangman_{}'.format(self.game.return_count()+1)
            self.hangman_label['image'] = self.IMAGES[current_hangman]
            self.hangman_label.image = self.IMAGES[current_hangman]
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

#Main loop of tkinter with the update calls for the application as 
while not exit:
    app.music_loop()
    root.update_idletasks()
    root.update()
    time.sleep(0.01)
root.destroy()