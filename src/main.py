import datetime
import pygame
import math

from src.components.configManager import configManager

from src.states.readingState import readingState
from src.states.configState import configState

def changeState(state):
    global current_state
    current_state = state

def run():
    global current_state
   #pygame setup
    pygame.init()
    w, h, fps, running = 1280, 720, 60, True
    window = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Reader")
    clock = pygame.time.Clock()

    #states
    reading_state = readingState(changeState)
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
        current_state.render(window, w, h)
       
        pygame.display.flip()
        clock.tick(fps)/1000
    pygame.quit()
    