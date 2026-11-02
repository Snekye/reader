import datetime
import pygame
import math

import tkinter as tk
from tkinter import filedialog
import os

from src.components.textParser import textParser
from src.states._abstractState import _abstractState

class readingState(_abstractState):
    def __init__(self, font_help):
        #tk setup
        self.root = tk.Tk()
        self.root.withdraw()

        #components
        self.tp = textParser()

        #setup
        self.text, self.words = "", [["Welcome! Press F9 to select a file."]] #empty  setup, see F9 event

        self.wordcount = 0
        self.wordcount_ch = 0
        self.ch_count = 0
        self.index = 0
        self.index_ch=0

        self.wpms = [60, 120, 150, 180, 210, 240, 270, 300, 330, 360]
        self.wpm_index = 3
        self.wpm = self.wpms[self.wpm_index]
        self.paused = True
        self.finished = False
        self.loaded = False
        self.timepoint = datetime.datetime.now()
        self.aa = True                   #text antialiasing
        self.notif_text = ""
        self.notif_timepoint = datetime.datetime.now()

        #pre_loading default ; see "render" section in main loop
        self.r_words = font_help.render(f"Chapter : -/- | Words (Chapter) : -/-", True, (255, 255, 255))

        self.help_keybinds = font_help.render(
            "SPACE = Pause/Unpause | LEFT = Back 5s | RIGHT = Forward 5s | UP = Raise WPM | DOWN = Lower WPM",
            True, (255, 255, 255)
        )
        self.help_keybinds2 = font_help.render(
            "[Not yet] F5 = Change new chapter mode | O = Previous chapter | P = Next chapter",
            True, (255, 255, 255)
        )
        self.help_keybinds3 = font_help.render(
            "F9 = Select text file | [Not yet] F10 = Change newline mode | [Not yet] F11 = GOTO | F12 = Antialiasing ON/OFF",
            True, (255, 255, 255)
        )

    def handleKey(self, key):
        match key:
            case pygame.K_SPACE:
                if self.paused:
                    self.timepoint = datetime.datetime.now()
                    self.notif_text = "Unpaused"
                else:
                    self.notif_text = "Paused"
                self.paused = not self.paused
                
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_LEFT:
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
                self.index += math.ceil(5 * self.wpm/60)
                if self.index >= self.wordcount_ch:
                    if self.index_ch+1 >= self.ch_count:
                        self.finished = True
                        self.index = self.wordcount_ch
                    else:
                        self.index = 0
                        self.index_ch += 1
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
                self.paused = True
                if self.index == 0 and self.index_ch > 0:
                    self.index_ch -= 1
                    self.wordcount_ch = len(self.words[self.index_ch])
                self.index = 0

                self.notif_text = f"Previous chapter : {self.index_ch+1}/{self.ch_count}"
                self.notif_timepoint = datetime.datetime.now()

            case pygame.K_p:
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
                self.aa = not self.aa

                self.notif_text = f"Antialiasing : {"ON" if self.aa else "OFF"}"
                self.notif_timepoint = datetime.datetime.now()

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
                    self.paused = True
                    self.wordcount_ch = len(self.words[self.index_ch])

    def render(self, window, font_text, font_help, w, h):
        #render
        render = font_text.render("[File ended]" if self.finished else self.words[self.index_ch][self.index], self.aa, (255, 255, 255))
        r_paused = font_help.render("Paused" if self.paused else "Unpaused", True, (255, 255, 255))
        if self.loaded:
            self.r_words = font_help.render(f"Chapter : {self.index_ch+1}/{self.ch_count} | Words (Chapter) : {self.index}/{self.wordcount_ch}", True, (255, 255, 255))
        r_wpm = font_help.render(f"WPM : {self.wpm}", True, (255, 255, 255))

        notif_alpha = max(0, 1 - max((datetime.datetime.now() - self.notif_timepoint).total_seconds() - 1, 0)) # 1 when ts < 1 ; 0 when ts > 2 ; inverse when ts € [1,2]
        r_notif = font_help.render(self.notif_text, True, (220, 220, 220))
        r_notif.set_alpha(int(notif_alpha * 255))

        #display
        h1, h2, h3 = self.help_keybinds, self.help_keybinds2, self.help_keybinds3
        window.blit(render, (w//2 - render.get_width()//2, h//2 - render.get_height()//2))
        window.blit(r_notif, (w//2 - r_notif.get_width()//2, h//2 + render.get_height()//2))
        window.blit(h3, (w//2 - h3.get_width()//2, h - 16 - h2.get_height()))
        window.blit(h2, (w//2 - h2.get_width()//2, h - 16 - h1.get_height() - h2.get_height()))
        window.blit(h1, (w//2 - h1.get_width()//2, h - 16 - h1.get_height() - h2.get_height() - h3.get_height()))
        window.blit(r_paused, (8, 8))
        window.blit(self.r_words, (8, 8 + r_paused.get_height()))
        window.blit(r_wpm, (8, 8 + r_paused.get_height() + self.r_words.get_height()))