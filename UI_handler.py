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
    GAME_WIN_SE = 2,
    GAME_LOSE_SE = 3,
    DEFAUL_BUTTON_SE = 4,
    IN_WORD = 5,
    NOT_IN_WORD = 6,
    NULL =7


class ui_handler():
    def __init__(self, master=None):
        
        #Configuration for the master window
        master.title('Hangman')
        master.minsize(1330, 720)
        master.maxsize(1330, 720)

        #Initializes base variables
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
        self.DEFAULT_BG = 'pink'
        self.BUTTON_BG = 'grey'

        #Create background image
        bg_frame = tk.Label(
            master,
            bg=self.DEFAULT_BG
            )
        bg_frame.place(
            relwidth=1,
            relheight=1
            )
        
        #Creates a frame containing the audio toggle buttons
        self.control_frame = tk.Frame(self.master, bg=self.DEFAULT_BG)
        self.control_frame.pack(anchor='nw', side='left')
        self.toggle_music_loop_button = tk.Button(self.control_frame,
            text='music',
            command=self.toggle_music,
            relief='groove'
            )
        self.toggle_sound_effect_button = tk.Button(self.control_frame,
            text='SE',
            command=self.toggle_sound_effect,
            relief='groove'
            )
        self.audio_control()

        #opens main menu
        self._main_menu()

    def load_audio(self):
       
        #loads all music file in a dictionary 'WAVE_OBJ'
        self.WAVE_OBJ = {}
        self.WAVE_OBJ[AUDIO.MENU_MUSIC] = sa.WaveObject.from_wave_file('Assets/audio/Lobby_music.wav')
        self.WAVE_OBJ[AUDIO.GAME_MUSIC] = sa.WaveObject.from_wave_file('Assets/audio/Game_music.wav')
        self.WAVE_OBJ[AUDIO.DEFAUL_BUTTON_SE] = sa.WaveObject.from_wave_file('Assets/audio/Blop_Mark_DiAngelo_79054334.wav')
        self.WAVE_OBJ[AUDIO.GAME_WIN_SE] = sa.WaveObject.from_wave_file('Assets/audio/win.wav')
        self.WAVE_OBJ[AUDIO.GAME_LOSE_SE] = sa.WaveObject.from_wave_file('Assets/audio/fail.wav')
        self.WAVE_OBJ[AUDIO.IN_WORD] = sa.WaveObject.from_wave_file('Assets/audio/correct.wav')
        self.WAVE_OBJ[AUDIO.NOT_IN_WORD] = sa.WaveObject.from_wave_file('Assets/audio/wrong.wav')

    def music_loop(self):
        
        #Is called by the main loop and runs the selected music under 'current_audio'
        #if 'is_play_music_loop' is true. It re-initializes the PlayObject if is
        #has finished running as 'music_loop_obj'
        if self.current_audio == AUDIO.NULL:
            if (isinstance(self.music_loop_obj, sa.PlayObject)):
                if self.music_loop_obj.is_playing():
                    self.music_loop_obj.stop()
        elif self.is_play_music_loop == 'True':

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
        if self.is_play_music_loop == 'True':
            self.toggle_music_loop_button['image'] = self.IMAGES['music_play']
        else:
            self.toggle_music_loop_button['image'] = self.IMAGES['music_mute']
        self.toggle_music_loop_button.pack(side='left', anchor='nw')

        if self.is_play_sound_effect == 'True':
            self.toggle_sound_effect_button['image'] = self.IMAGES['sound_effects_play']
        else:
            self.toggle_sound_effect_button['image'] = self.IMAGES['sound_effects_off']
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
        self.IMAGES['play_button'] = tk.PhotoImage(file='Assets/Image/play_button.pbm')
        self.IMAGES['sound_effects_play'] = tk.PhotoImage(file='Assets/Image/Speaker_icon.pbm')
        self.IMAGES['sound_effects_off'] = tk.PhotoImage(file='Assets/Image/Mute_icon.pbm')
        self.IMAGES['music_play'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver.pbm')
        self.IMAGES['music_mute'] = tk.PhotoImage(file='Assets/Image/Linecons_quaver_mute.pbm')
        self.IMAGES['instructions_1'] = tk.PhotoImage(file='Assets/Image/Instructions_1.pbm')
        self.IMAGES['instructions_2'] = tk.PhotoImage(file='Assets/Image/Instructions_2.pbm')
        self.IMAGES['logo'] = tk.PhotoImage(file='Assets/Image/Logo.pbm')
        self.IMAGES['win'] = tk.PhotoImage(file='Assets/Image/Hangman_win.pbm')
        self.IMAGES['loss'] = tk.PhotoImage(file='Assets/Image/Hangman_8.pbm')
        for i in range(1, 9):
            path = 'Hangman_{}'.format(i)
            self.IMAGES[path.lower()] = tk.PhotoImage(file='Assets/Image/{}.pbm'.format(path))
                
    def _main_menu(self):
       
        #Re-create audio frame
        self.control_frame.pack(anchor='nw', side='left')
       
        #Initialize main menu frame
        self.frames['main'] = tk.Frame(self.master, bg=self.DEFAULT_BG)
        self.frames['main'].pack()
       
        #Selects current audio
        self.current_audio = AUDIO.MENU_MUSIC

        #Places game logo
        game_logo = tk.Label(
            self.frames['main'],
            image=self.IMAGES['logo'],
            relief='solid')
        game_logo.image = self.IMAGES['logo']
        game_logo.pack()

        #Creates label frame containing the play button and word length drop down
        game_start_lable_frame = tk.LabelFrame(
            self.frames['main'],
            bg=self.BUTTON_BG
            )
        game_start_lable_frame.pack()

        #List of all possible values for word length
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
        #initializes tkinter string variable that is used to retrieve current value
        self.current_length = tk.StringVar(self.frames['main'])
        self.current_length.set(self.game.return_options('Word_length'))

        #Creates a tkinter option menu which contains the options from 'word_length_opt'
        #and return the values to 'current_length'
        word_lenght_menu = tk.OptionMenu(game_start_lable_frame,
            self.current_length,
            *word_length_opt
            )
        word_lenght_menu.config(font=self.button_font, relief='groove',
            bg=self.BUTTON_BG)
        word_lenght_menu.pack(side='right')

        #Creates a button within 'game_start_label_frame', which clears the main menu
        #plays and SE, calls to retrieve the current word length and launch the game menu
        play_button = tk.Button(
            game_start_lable_frame,
            text='Play',
            command=lambda: (self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._word_len_opt(),
            self._game_menu()),
            relief='flat',
            font=self.button_font,
            bg=self.BUTTON_BG
            #image=self.IMAGES['play_button']
            )
        play_button.image = self.IMAGES['play_button']
        play_button.pack(side='left')

        #Creates a button dose functions similar to the play button but dose not
        #retrieve word length and launches the option window
        option_button = tk.Button(
            self.frames['main'],
            text='Options',
            relief='flat',
            font=self.button_font,
            bg=self.BUTTON_BG,
            command=lambda:(self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._option_menu())
            )
        option_button.pack()

        #Creates a button dose functions similar to the option button but launches the
        #instruction menu
        instruction_button = tk.Button(
            self.frames['main'],
            text='Instructions',
            relief='flat',
            font=self.button_font,
            bg=self.BUTTON_BG,
            command=lambda:(self.frames['main'].pack_forget(),
            self.play_sound_effect(AUDIO.DEFAUL_BUTTON_SE),
            self._instruction_menu())
            )
        instruction_button.pack()

        #Creates a button that calls the exit function
        exit_button = tk.Button(self.frames['main'],
            text='Exit',
            relief='flat',
            bg=self.BUTTON_BG,
            command=lambda:(quit()),
            font=self.button_font

            )
        exit_button.pack()

    def _word_len_opt(self):
        
        #Retrieves the word length in 'current_length' and updates the options in 'game_logic'
        new_length =  self.current_length.get()
        self.game.change_options('Word_length', new_length)

    def _instruction_menu(self):
        self.control_frame.pack_forget()
        
        #Creates the frame for instruction
        self.frames['instructions'] = tk.Frame(self.master, bg=self.DEFAULT_BG)
        self.frames['instructions'].pack()

        #Creates label containing heading
        instruction_label = tk.Label(self.frames['instructions'],
            text='Instructions',
            relief='flat',
            font=self.button_font,
            bg=self.DEFAULT_BG)
        instruction_label.pack()

        #Creates label containing the image for instructions
        self.current_instruction = 1
        self.instruction_image_label = tk.Label(self.frames['instructions'],
            image=self.IMAGES['instructions_1'],
            relief='solid')
        self.instruction_image_label.bind('<Button-1>', self.toggle_instruction)
        self.instruction_image_label.pack()

        #Creates button which closes the current frame and return to the main menu
        back_main_menu_button = tk.Button(self.frames['instructions'], text="Back to main menu",
            command=lambda:(self.frames['instructions'].pack_forget(),
             self._main_menu()),
            relief="flat",
            font=self.button_font,
            bg=self.BUTTON_BG
            )
        back_main_menu_button.pack(
            side="bottom",
            anchor='sw'
            )

    def toggle_instruction(self, event):
        #Toggles the instruction image from 1 to 2 and vise versa
        if self.current_instruction == 1:
            self.instruction_image_label.config(image=self.IMAGES['instructions_2'])
            self.current_instruction = 2
        else:
            self.current_instruction = 1
            self.instruction_image_label.config(image=self.IMAGES['instructions_1'])
        self.instruction_image_label.bind('<Button-1>', self.toggle_instruction)

    def _option_menu(self):
        self.control_frame.pack_forget()
        self.frames['options'] = tk.Frame(self.master, bg=self.DEFAULT_BG)
        self.frames['options'].pack(pady=50, expand=True)
        LABEL_WIDTH = 30
        BUTTON_WIDTH = 8

        #Title label for the frame
        title_label = tk.Label(self.frames['options'],
            text='Options',
            font=self.button_font,
            bg=self.DEFAULT_BG)
        title_label.pack(pady=30)

        #Label frame which contains the dictionary configurations
        dictionary_option_label_frame = tk.LabelFrame(self.frames['options'],
            bg=self.BUTTON_BG)
        dictionary_option_label_frame.pack()
        
        dictionary_label = tk.Label(dictionary_option_label_frame,
            text='Dictionary',
            font=self.button_font,
            width=LABEL_WIDTH,
            bg=self.BUTTON_BG
            )
        dictionary_label.grid(column=0, row=0)
        
        #Button that toggles the dictionary to custom sinking and disabling itself
        #and rising and activating the default button
        dictionary_button_custom = tk.Button(dictionary_option_label_frame,
            text='Custom',
            font=self.button_font,
            bg=self.BUTTON_BG,
            width=BUTTON_WIDTH,
            command=lambda:(dictionary_button_custom.config(relief='sunken', state='disabled'),
                dictionary_button_default.config(relief='raised', state='normal'),
                self.game.change_options('Dictionary', 'Custom'))
            )
        dictionary_button_custom.grid(column=1, row=0)

        #Button that toggles the dictionary to default sinking and disabling itself
        #and rising and activating the custom button
        dictionary_button_default = tk.Button(dictionary_option_label_frame,
            text='Default',
            font=self.button_font,
            width=BUTTON_WIDTH,
            bg=self.BUTTON_BG,
            command=lambda:(dictionary_button_custom.config(relief='raised', state='normal'),
                dictionary_button_default.config(relief='sunken', state='disabled'),
                self.game.change_options('Dictionary', 'Default'))
            )
        dictionary_button_default.grid(column=2, row=0)

        #Activates and rises the current dictionary used and disables the other
        #Default option is the Default button
        if self.game.return_options('Dictionary') == 'Custom':
            dictionary_button_custom.config(relief='sunken', state='disabled')
            dictionary_button_default.config(relief='raised', state='normal')
        else:
            dictionary_button_custom.config(relief='raised', state='normal')
            dictionary_button_default.config(relief='sunken', state='disabled')

        #Label frame which contains the music configurations
        musci_option_label_frame = tk.LabelFrame(self.frames['options'],
            bg=self.BUTTON_BG)
        musci_option_label_frame.pack()
        
        music_label = tk.Label(musci_option_label_frame,
            text='Music',
            font=self.button_font,
            bg=self.BUTTON_BG,
            width=LABEL_WIDTH
            )
        music_label.grid(column=0, row=0)

        #Button that toggles the music on sinking and disabling itself
        #and rising and activating the off button
        music_button_on = tk.Button(musci_option_label_frame,
            text='On',
            font=self.button_font,
            width=BUTTON_WIDTH,
            bg=self.BUTTON_BG,
            command=lambda:(music_button_on.config(relief='sunken', state='disabled'),
                music_button_off.config(relief='raised', state='normal'),
                self.toggle_music()
                )
            )
        music_button_on.grid(column=1, row=0)

        #Button that toggles the music off sinking and disabling itself
        #and rising and activating the on button
        music_button_off = tk.Button(musci_option_label_frame,
            text='Off',
            font=self.button_font,
            width=BUTTON_WIDTH,
            bg=self.BUTTON_BG,
            command=lambda:(music_button_on.config(relief='raised', state='normal'),
                music_button_off.config(relief='sunken', state='disabled'),
                self.toggle_music()
                )
            )
        music_button_off.grid(column=2, row=0)

        #Activates and rises the current music option and disables the other
        #Default option is the off button
        if self.game.return_options("Music") == 'True':
            music_button_on.config(relief='sunken', state='disabled')
            music_button_off.config(relief='raised', state='normal')
        else:
            music_button_on.config(relief='raised', state='normal')
            music_button_off.config(relief='sunken', state='disabled')

        #Label frame which contains the music configurations
        sound_effects_option_label_frame = tk.LabelFrame(self.frames['options'],
            bg=self.BUTTON_BG)
        sound_effects_option_label_frame.pack()
        sound_effect_label = tk.Label(sound_effects_option_label_frame,
            text='Sound Effects',
            bg=self.BUTTON_BG,
            font=self.button_font,
            width=LABEL_WIDTH
            )
        sound_effect_label.grid(column=0, row=0)
        
        #Button that toggles the sound effect on sinking and disabling itself
        #and rising and activating the off button
        sound_effect_button_on = tk.Button(sound_effects_option_label_frame,
            text='On',
            font=self.button_font,
            width=BUTTON_WIDTH,
            bg=self.BUTTON_BG,
            command=lambda:(
                sound_effect_button_on.config(relief='sunken', state='disabled'),
                sound_effect_button_off.config(relief='raised', state='normal'),
                self.toggle_sound_effect())
            )
        sound_effect_button_on.grid(column=1, row=0)
        
        #Button that toggles the sound effect off sinking and disabling itself
        #and rising and activating the on button
        sound_effect_button_off = tk.Button(sound_effects_option_label_frame,
            text='Off',
            font=self.button_font,
            width=BUTTON_WIDTH,
            bg=self.BUTTON_BG,
            command=lambda:(
                sound_effect_button_on.config(relief='raised', state='normal'),
                sound_effect_button_off.config(relief='sunken', state='disabled'),
                self.toggle_sound_effect())
            )
        sound_effect_button_off.grid(column=2, row=0)

        #Activates and rises the current sound effect option and disables the other
        #Default option is the off button
        if self.game.return_options("Sound_effects") == 'True':
            sound_effect_button_on.config(relief='sunken', state='disabled')
            sound_effect_button_off.config(relief='raised', state='normal')
        else:
            sound_effect_button_on.config(relief='raised', state='normal')
            sound_effect_button_off.config(relief='sunken', state='disabled')

        #Creates a button that returns to main menu
        back_main_menu_button = tk.Button(self.frames['options'], text="Back to main menu",
            command=lambda:(self.frames['options'].pack_forget(),
             self._main_menu()),
            relief="flat",
            font=self.button_font,
            bg=self.BUTTON_BG
            )
        back_main_menu_button.pack(
            side="bottom"
            )
               
    def _game_menu(self):
        self.control_frame.pack(anchor='nw', side='left')
        self.current_audio = AUDIO.GAME_MUSIC
        self.frames['game'] = tk.Frame(self.master,
            height=100,
            width=100,
            bg=self.DEFAULT_BG
            )

        #Binds the game menu frame so that when a key is pressed it will
        #call the '_game_input' function which will register the input as a guess if valid
        self.frames['game'].bind_all('<Key>', self._game_input)
        self.frames['game'].pack()
        
        #Initializes the variables for the game
        self.game.start()
        self.game_end = False

        #Label which contains the image of hangman
        self.hangman_label = tk.Label(
            self.frames['game'],
            relief='solid',
            bg=self.DEFAULT_BG
            )
        self.update_hangman()
        self.hangman_label.pack()

        #Assigns the mystery word to a tkinter updateable StringVar
        self.mystery_word = tk.StringVar(self.frames['game'])
        self.mystery_word.set(self.game.get_mystery_word())

        #Creates a label which the mystery word which can be updated
        mystery_word_label = tk.Label(
            self.frames['game'],
            textvariable=self.mystery_word,
            font=self.button_font,
            bg=self.DEFAULT_BG
            )
        mystery_word_label.pack()

        #Displays an error when the input is not valid
        self.error = tk.StringVar(self.frames['game'])
        error_label = tk.Label(
            self.frames['game'],
            textvariable=self.error,
            fg='red',
            bg=self.DEFAULT_BG,
            font=self.button_font
            )
        error_label.pack()

        #Label frame which contains all character of the alphabet which update as
        #they are guessed
        self.guessed_word_labelframe = tk.LabelFrame(
            self.frames['game'],
            relief='flat',
            bg=self.DEFAULT_BG
            )
        self.guessed_word_labelframe.pack()

        #Creates all the labels which contain a single character and ordered into 2 rows
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
                font=self.button_font,
                bg=self.DEFAULT_BG
                )
            self.guessed_word_labels[chr(97+i)].grid(column=col,row=row)
        
        #Creates a button which clears the current frame and returns to main menu
        back_button = tk.Button(
            self.frames['game'],
            text='Back',
            relief='groove',
            bg=self.BUTTON_BG,
            command=lambda:(self.frames['game'].pack_forget(),
                self._main_menu()),
            font=self.button_font
            )

        back_button.pack()
      
    def _game_input(self, event):
        
        #Converts the character input in to lower if present
        input = event.char.lower()
       
        #Checks whether the input is a valid single character
        if (not self.game.check_user_input(event.char)):
            self.error.set("{} is not a valid character".format(event.char))
        else:
            
            #Return an error if it has already been guessed
            if (self.game.is_guessed(input)):
                self.error.set("{} is already guessed".format(input))
            else:
               
                #Checks whether the character is in the mystery word and updates the guess character dictionary
                if (self.game.check_word(input)):
                    
                    #Retrieves an updated mystery word and changes the guessed character to green
                    #and plays a correct sound
                    self.mystery_word.set(self.game.get_mystery_word())
                    self.play_sound_effect(AUDIO.IN_WORD)
                    self.guessed_word_labels[input].config(fg='green')
                else:
                   
                    #Changes the guessed character to red and plays a wrong sound
                    self.error.set("{} is not in word".format(input))
                    self.play_sound_effect(AUDIO.NOT_IN_WORD)
                    self.guessed_word_labels[input].config(fg='red')
                
                #Gets the position of the label withing the grid and places it accordingly
                char_num = ord(input) - 97
                if char_num > 12:
                    row = 1
                    col = char_num-13
                else:
                    row = 0
                    col = char_num
                self.guessed_word_labels[input].grid(column=col, row=row)
        
        #Checks whether the player has lost or won and if either is true
        #Closes the current frame into the result screen passing the state
        if (not self.game_end):
            if (self.game.is_win() or self.game.is_lose()):
                self.frames['game'].pack_forget()
                self.result_menu(self.game.is_win())
                self.game_end = True
        self.update_hangman()
        time.sleep(0.1)
                 
    def result_menu(self, win):
        self.audio_control()
        self.frames['result'] = tk.Frame(self.master, bg=self.DEFAULT_BG)
        self.current_audio = AUDIO.NULL
        
        #Creates a variable label which contains output regarding their results
        result_str = tk.StringVar()
        result_label = tk.Label(
            self.frames['result'],
            textvariable=result_str,
            font=self.button_font,
            bg=self.DEFAULT_BG)
        if win:
            
            #Assigns output text and image when won
            result_str.set('Congratulation! You guessed the word: {}'.format(self.game.cur_word))
            result_label.config(fg='green')
            result_image = tk.Label(
                self.frames['result'],
                image=self.IMAGES['win'],
                relief='solid'
                )
            result_image.image = self.IMAGES['win']
            self.play_sound_effect(AUDIO.GAME_WIN_SE)
        else:
            
            #Assigns output text and image when lost
            result_str.set('you lose! The word was: {}'.format(self.game.cur_word))
            result_label.config(fg='red')
            result_image = tk.Label(
                self.frames['result'],
                image=self.IMAGES['loss'],
                relief='solid'
                )
            result_image.image = self.IMAGES['loss']
            self.play_sound_effect(AUDIO.GAME_LOSE_SE)
        result_image.pack()
        result_label.pack()

        #Creates a button that re-initializes the game menu with new data
        play_again_button = tk.Button(self.frames['result'],text='Play again',
            command=lambda: (self.frames['result'].pack_forget(),
            self.WAVE_OBJ[AUDIO.DEFAUL_BUTTON_SE].play(),
            self._game_menu()),
            relief='groove',
            font=self.button_font,
            bg=self.BUTTON_BG
            )
        play_again_button.pack()

        #Creates a button that returns to the main_menu
        back_to_menu_button = tk.Button(
            self.frames['result'],
            text="Back to main menu",
            command=lambda:(
                self.frames['result'].pack_forget(),
                self._main_menu()),
            relief="groove",
            font=self.button_font,
            bg=self.BUTTON_BG
            )
        back_to_menu_button.pack(side="top")

        self.frames['result'].pack()
    
    def update_hangman(self):
        #Changes the hangman image displayed in the game frame according to the
        #number of wrong guesses
        img_num = self.game.return_count()
        if img_num <= 7:
            current_hangman = 'hangman_{}'.format(self.game.return_count()+1)
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