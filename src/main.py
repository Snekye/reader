import datetime
import pygame
import math

import tkinter as tk
from tkinter import filedialog
import os

from ebooklib import epub, ITEM_DOCUMENT
import ebooklib
from bs4 import BeautifulSoup

def run():
   #pygame setup
    pygame.init()
    w, h, fps, running = 1280, 720, 60, True
    window = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Reader")
    clock = pygame.time.Clock()

    #tk setup
    root = tk.Tk()
    root.withdraw()

    #setup
    text, words = "", [["Welcome! Press F9 to select a file."]] #empty  setup, see F9 event

    wordcount = 0
    wordcount_ch = 0
    ch_count = 0
    index = 0
    index_ch=0

    wpms = [60, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    wpm_index = 3
    wpm = wpms[wpm_index]
    paused = True
    finished = False
    loaded = False
    timepoint = datetime.datetime.now()
    aa = True                   #text antialiasing
    notif_text = ""
    notif_timepoint = datetime.datetime.now()

    #fonts and renders
    font_text = pygame.font.SysFont("Times New Roman", 32)
    font_help = pygame.font.SysFont("Times New Roman", 20)

    #pre_loading default ; see "render" section in main loop
    r_words = font_help.render(f"Chapter : -/- | Words (Chapter) : -/-", True, (255, 255, 255))

    help_keybinds = font_help.render(
        "SPACE = Pause/Unpause | LEFT = Back 5s | RIGHT = Forward 5s | UP = Raise WPM | DOWN = Lower WPM",
        True, (255, 255, 255)
    )
    help_keybinds2 = font_help.render(
        "[Not yet] F5 = Change new chapter mode | O = Previous chapter | P = Next chapter",
        True, (255, 255, 255)
    )
    help_keybinds3 = font_help.render(
        "F9 = Select text file | [Not yet] F10 = Change newline mode | [Not yet] F11 = GOTO | F12 = Antialiasing ON/OFF",
        True, (255, 255, 255)
    )

    #
    while running:
        window.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                match e.key:
                    case pygame.K_SPACE:
                        if paused:
                            timepoint = datetime.datetime.now()
                            notif_text = "Unpaused"
                        else:
                            notif_text = "Paused"
                        paused = not paused
                        
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_LEFT:
                        finished = False
                        if index == 0:
                            if index_ch > 0:
                                index_ch -=1
                                wordcount_ch = len(words[index_ch])

                        index -= math.ceil(5 * wpm/60)
                        if index < 0:
                            index = 0

                        notif_text = "Rewind"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_RIGHT:
                        index += math.ceil(5 * wpm/60)
                        if index >= wordcount_ch:
                            if index_ch+1 >= ch_count:
                                finished = True
                                index = wordcount_ch
                            else:
                                index = 0
                                index_ch += 1
                                paused = True
                                wordcount_ch = len(words[index_ch])
                        

                        notif_text = "Forward"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_UP:
                        wpm_index +=1
                        if wpm_index >= len(wpms):
                            wpm_index -= 1
                        wpm = wpms[wpm_index]

                        notif_text = f"WPM : {wpm}"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_DOWN:
                        wpm_index -=1
                        if wpm_index < 0:
                            wpm_index = 0
                        wpm = wpms[wpm_index]

                        notif_text = f"WPM : {wpm}"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_o:
                        finished = False
                        paused = True
                        if index == 0 and index_ch > 0:
                            index_ch -= 1
                            wordcount_ch = len(words[index_ch])
                        index = 0

                        notif_text = f"Previous chapter : {index_ch+1}/{ch_count}"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_p:
                        paused = True
                        if index_ch+1 >= ch_count:
                            finished = True
                            index = wordcount_ch
                        else:
                            index = 0
                            index_ch += 1
                            paused = True
                            wordcount_ch = len(words[index_ch])

                        notif_text = f"Next chapter : {index_ch+1}/{ch_count}"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_F9:
                        index, index_ch, paused = 0, 0, True
                        file_path = filedialog.askopenfilename(
                            title="Select a File",
                            filetypes=[("Text files", "*.txt *.epub")]
                        )
                        ext = file_path.split(".")[-1]
                        match ext:
                            case "txt" : 
                                with open(file_path, "r") as f:
                                    text = f.read()
                                    f.close()
                                words = [text.split()] #put in a single "chapter"
                                wordcount = len(words[0])
                                ch_count = 1
                                wordcount_ch = wordcount

                            case "epub" :
                                ### LLM gen section
                                book = epub.read_epub(file_path)
                                chapters = []
                                for item in book.get_items_of_type(ITEM_DOCUMENT):
                                    soup = BeautifulSoup(item.get_content(), "html.parser")
                                    # Remove scripts/styles if present
                                    for tag in soup(["script", "style"]):
                                        tag.decompose()
                                    text = soup.get_text(separator="\n", strip=True)
                                    if text:
                                        chapters.append(text)
                                ###

                                words = []
                                for c in chapters:
                                    c = c.replace("Chapter ", "Chapter⠀") #U+2800 Blank
                                    c = c.replace("Table of Contents", "Table⠀of⠀Contents")
                                    words += [c.split()] 
                                    wordcount += len(c)
                                wordcount_ch = len(words[0])
                                ch_count = len(words)

                        loaded = True
                        notif_text = f"Text file opened : {file_path}"
                        notif_timepoint = datetime.datetime.now()

                    case pygame.K_F12:
                        aa = not aa

                        notif_text = f"Antialiasing : {"ON" if aa else "OFF"}"
                        notif_timepoint = datetime.datetime.now()

                    case _:
                        continue

        if not paused and not finished and (datetime.datetime.now() - timepoint).total_seconds() > (60 / wpm):
            timepoint = datetime.datetime.now()
            index += 1
            if index >= wordcount_ch:
                if index_ch+1 >= ch_count:
                    finished = True
                else:
                    index = 0
                    index_ch += 1
                    paused = True
                    wordcount_ch = len(words[index_ch])

        #render
        render = font_text.render("[File ended]" if finished else words[index_ch][index], aa, (255, 255, 255))
        r_paused = font_help.render("Paused" if paused else "Unpaused", True, (255, 255, 255))
        if loaded:
            r_words = font_help.render(f"Chapter : {index_ch+1}/{ch_count} | Words (Chapter) : {index}/{wordcount_ch}", True, (255, 255, 255))
        r_wpm = font_help.render(f"WPM : {wpm}", True, (255, 255, 255))

        notif_alpha = max(0, 1 - max((datetime.datetime.now() - notif_timepoint).total_seconds() - 1, 0)) # 1 when ts < 1 ; 0 when ts > 2 ; inverse when ts € [1,2]
        r_notif = font_help.render(notif_text, True, (220, 220, 220))
        r_notif.set_alpha(int(notif_alpha * 255))

        #display
        window.blit(render, (w//2 - render.get_width()//2, h//2 - render.get_height()//2))
        window.blit(r_notif, (w//2 - r_notif.get_width()//2, h//2 + render.get_height()//2))
        window.blit(help_keybinds3, (w//2 - help_keybinds3.get_width()//2, h - 16 - help_keybinds2.get_height()))
        window.blit(help_keybinds2, (w//2 - help_keybinds2.get_width()//2, h - 16 - help_keybinds.get_height() - help_keybinds2.get_height()))
        window.blit(help_keybinds, (w//2 - help_keybinds.get_width()//2, h - 16 - help_keybinds.get_height() - help_keybinds2.get_height() - help_keybinds3.get_height()))
        window.blit(r_paused, (8, 8))
        window.blit(r_words, (8, 8 + r_paused.get_height()))
        window.blit(r_wpm, (8, 8 + r_paused.get_height() + r_words.get_height()))

        #
        pygame.display.flip()
        clock.tick(fps)/1000
    pygame.quit()
    