import datetime
import pygame
import math

import tkinter as tk
from tkinter import filedialog
import os

from src.components.textParser import textParser
from src.components.configManager import configManager
from src.states._abstractState import _abstractState
from src.states.configState import configState

class readingState(_abstractState):
    def __init__(self, changeState):
        #config load
        self.cm = configManager()
        self.cfg = self.cm.load()

        #tk setup
        self.root = tk.Tk()
        self.root.withdraw()

        #states
        self.change_state = changeState

        #components
        self.tp = textParser()

        #setup
        self.text, self.words = "", [["Welcome! Press F9 to select a file."]] #empty  setup, see F9 event

        self.wordcount = 0
        self.wordcount_ch = 0
        self.ch_count = 0
        self.index = 0
        self.index_ch=0

        self.wpms = self.cfg["wpms"]
        self.wpm_index = 3
        self.wpm = self.wpms[self.wpm_index]
        self.paused = True
        self.finished = False
        self.loaded = False
        self.timepoint = datetime.datetime.now()
        self.notif_text = ""
        self.notif_timepoint = datetime.datetime.now()

        self.txts()

    def txts(self):
        self.cfg = self.cm.load()

        #fonts
        self.font_text = pygame.font.SysFont(self.cfg["fonts"]["text"]["font"], self.cfg["fonts"]["text"]["size"])
        self.font_notif = pygame.font.SysFont(self.cfg["fonts"]["notif"]["font"], self.cfg["fonts"]["notif"]["size"])
        self.font_help = pygame.font.SysFont(self.cfg["fonts"]["help"]["font"], self.cfg["fonts"]["help"]["size"])
        self.col_text = self.cfg["fonts"]["text"]["color"]
        self.col_notif = self.cfg["fonts"]["notif"]["color"]
        self.col_help = self.cfg["fonts"]["help"]["color"]

        #static renders
        self.r_words = self.font_help.render(f"Chapter : -/- | Words (Chapter) : -/-",  self.cfg["aa"], self.col_help) #default
        self.help_keybinds = self.font_help.render(
            "SPACE = Pause/Unpause | LEFT = Back 5s | RIGHT = Forward 5s | UP = Raise WPM | DOWN = Lower WPM",
            self.cfg["aa"], self.col_help
        )
        self.help_keybinds2 = self.font_help.render(
            "O = Previous chapter | P = Next chapter",
             self.cfg["aa"], self.col_help
        )
        self.help_keybinds3 = self.font_help.render(
            "F9 = Select text file | [Not yet] F11 = GOTO | F12 = Settings",
             self.cfg["aa"], self.col_help
        )

    def handleKey(self, key):
        match key:
            case pygame.K_SPACE:
                if self.loaded:
                    if self.paused:
                        self.timepoint = datetime.datetime.now()
                        self.notif_text = "Unpaused"
                    else:
                        self.notif_text = "Paused"
                    self.paused = not self.paused
                    
                    self.notif_timepoint = datetime.datetime.now()

            case pygame.K_LEFT:
                if self.loaded:
                    self.finished = False
                    if self.index == 0:
                        if self.index_ch > 0:
                            self.index_ch -=1
                            self.wordcount_ch = len(self.words[self.index_ch])

                    self.index -= math.ceil(5 * self.wpm/60)
                    if self.index < 0:
                        self.index = 0

                    self.notif_text = "Rewind"
                    self.notif_timepoint = datetime.datetime.now()

            case pygame.K_RIGHT:
                if self.loaded:
                    self.index += math.ceil(5 * self.wpm/60)
                    if self.index >= self.wordcount_ch:
                        if self.index_ch+1 >= self.ch_count:
                            self.finished = True
                            self.index = self.wordcount_ch
                        else:
                            self.index = 0
                            self.index_ch += 1
                            if self.cfg["ch_pause"]:
                                self.paused = True
                            self.wordcount_ch = len(self.words[self.index_ch])
                    

                    self.notif_text = "Forward"
                    self.notif_timepoint = datetime.datetime.now()

            case pygame.K_UP:
                self.wpm_index +=1
                if self.wpm_index >= len(self.wpms):
                    self.wpm_index -= 1
                self.wpm = self.wpms[self.wpm_index]

                self.notif_text = f"WPM : {self.wpm}"
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_DOWN:
                self.wpm_index -=1
                if self.wpm_index < 0:
                    self.wpm_index = 0
                self.wpm = self.wpms[self.wpm_index]

                self.notif_text = f"WPM : {self.wpm}"
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_o:
                self.finished = False
                if self.cfg["ch_pause"]:
                    self.paused = True
                if self.index == 0 and self.index_ch > 0:
                    self.index_ch -= 1
                    self.wordcount_ch = len(self.words[self.index_ch])
                self.index = 0

                self.notif_text = f"Previous chapter : {self.index_ch+1}/{self.ch_count}"
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_p:
                if self.cfg["ch_pause"]:
                    self.paused = True
                if self.index_ch+1 >= self.ch_count:
                    self.finished = True
                    self.index = self.wordcount_ch
                else:
                    self.index = 0
                    self.index_ch += 1
                    self.paused = True
                    self.wordcount_ch = len(self.words[self.index_ch])

                self. notif_text = f"Next chapter : {self.index_ch+1}/{self.ch_count}"
                self. notif_timepoint = datetime.datetime.now()

            case pygame.K_F9:
                self.index, self.index_ch, self.paused = 0, 0, True
                file_path = filedialog.askopenfilename(
                    title="Select a File",
                    filetypes=[("Text files", "*.txt *.epub")]
                )
                try:
                    self.words, self.wordcount, self.wordcount_ch, self.ch_count = self.tp.parse(file_path)
                    self.notif_text = f"Text file opened : {file_path}"
                    self.loaded = True
                except:
                    self.notif_text = f"Error opening : {file_path}"
                    self.loaded = False
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_F12:
                self.paused = True
                self.change_state(configState(self, self.change_state))

            case _:
                return

    def update(self):
        #text forward logic
        if not self.paused and not self.finished and (datetime.datetime.now() - self.timepoint).total_seconds() > (60 / self.wpm):
            self.timepoint = datetime.datetime.now()
            self.index += 1
            if self.index >= self.wordcount_ch:
                if self.index_ch+1 >= self.ch_count:
                    self.finished = True
                else:
                    self. index = 0
                    self. index_ch += 1
                    if self.cfg["ch_pause"]:
                        self.paused = True
                    self.wordcount_ch = len(self.words[self.index_ch])

    def render(self, window, w, h):
        #render
        render = self.font_text.render("[File ended]" if self.finished else self.words[self.index_ch][self.index],  self.cfg["aa"], self.col_text)
        r_paused = self.font_help.render("Paused" if self.paused else "Unpaused",  self.cfg["aa"], self.col_help)
        if self.loaded:
            self.r_words = self.font_help.render(f"Chapter : {self.index_ch+1}/{self.ch_count} | Words (Chapter) : {self.index}/{self.wordcount_ch}",  self.cfg["aa"], self.col_help)
        r_wpm = self.font_help.render(f"WPM : {self.wpm}",  self.cfg["aa"], self.col_help)

        if self.cfg["floats"]:
            notif_alpha = max(0, 1 - max((datetime.datetime.now() - self.notif_timepoint).total_seconds() - 1, 0)) # 1 when ts < 1 ; 0 when ts > 2 ; inverse when ts € [1,2]
            r_notif = self.font_help.render(self.notif_text,  self.cfg["aa"], self.col_notif)
            r_notif.set_alpha(int(notif_alpha * 255))
            window.blit(r_notif, (w//2 - r_notif.get_width()//2, h//2 + render.get_height()//2))

        #display
        h1, h2, h3 = self.help_keybinds, self.help_keybinds2, self.help_keybinds3
        window.blit(render, (w//2 - render.get_width()//2, h//2 - render.get_height()//2))
        window.blit(h3, (w//2 - h3.get_width()//2, h - 16 - h2.get_height()))
        window.blit(h2, (w//2 - h2.get_width()//2, h - 16 - h1.get_height() - h2.get_height()))
        window.blit(h1, (w//2 - h1.get_width()//2, h - 16 - h1.get_height() - h2.get_height() - h3.get_height()))
        window.blit(r_paused, (8, 8))
        window.blit(self.r_words, (8, 8 + r_paused.get_height()))
        window.blit(r_wpm, (8, 8 + r_paused.get_height() + self.r_words.get_height()))