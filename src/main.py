import datetime
import pygame
import math

import tkinter as tk
from tkinter import filedialog
import os

from src.components.textParser import textParser

from src.states.readingState import readingState

def run():
   #pygame setup
    pygame.init()
    w, h, fps, running = 1280, 720, 60, True
    window = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Reader")
    clock = pygame.time.Clock()

    #fonts and renders
    font_text = pygame.font.SysFont("Times New Roman", 32)
    font_help = pygame.font.SysFont("Times New Roman", 20)

    #states
    reading_state = readingState(font_help)
    current_state = reading_state

    #main loop
    while running:
        window.fill((0,0,0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                current_state.handleKey(e.key)

        current_state.update()
        current_state.render(window, font_text, font_help, w, h)
       
        pygame.display.flip()
        clock.tick(fps)/1000
    pygame.quit()
    