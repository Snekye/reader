import pygame

from src.states._abstractState import _abstractState

from src.components.configManager import configManager

class configState(_abstractState):
    def __init__(self, callback, changeState):
        self.callback = callback
        self.change_state = changeState
        
        self.cm = configManager()
        self.cfg = self.cm.load()

        self.txts()

    def txts(self):
        self.font_help = pygame.font.SysFont(self.cfg["fonts"]["help"]["font"], self.cfg["fonts"]["help"]["size"])
        self.col_help = self.cfg["fonts"]["help"]["color"]
        self.label1 = self.font_help.render("F1 | 'Text' Font [Not yet]", self.cfg["aa"], self.col_help)
        self.label2 = self.font_help.render("F2 | 'Notif' Font [Not yet]", self.cfg["aa"], self.col_help)
        self.label3 = self.font_help.render("F3 | 'Help' Font [Not yet]", self.cfg["aa"], self.col_help)
        self.label4 = self.font_help.render("F4 | Antialiasing", self.cfg["aa"], self.col_help)

        self.label5 = self.font_help.render("F5 | Floating notifications", self.cfg["aa"], self.col_help)
        self.label6 = self.font_help.render("F6 | Background color [Not yet]", self.cfg["aa"], self.col_help)
        self.label7 = self.font_help.render("F7 | wpms [Not yet]", self.cfg["aa"], self.col_help)
        self.label8 = self.font_help.render("F8", self.cfg["aa"], self.col_help)

        self.label12 = self.font_help.render("F12 | Save settings", self.cfg["aa"], self.col_help)

        f = self.cfg["fonts"]
        self.value1 = self.font_help.render(
            f"{f["text"]["font"]} | {f["text"]["size"]}pt | ", self.cfg["aa"], f["help"]["color"])
        self.hex1 = self.font_help.render(f"{f["text"]["color"]}", self.cfg["aa"], f["text"]["color"])
        self.value2 = self.font_help.render(
            f"{f["notif"]["font"]} | {f["notif"]["size"]}pt | ", self.cfg["aa"], f["help"]["color"])
        self.hex2 = self.font_help.render(f"{f["notif"]["color"]}", self.cfg["aa"], f["notif"]["color"]) 
        self.value3 = self.font_help.render(
            f"{f["help"]["font"]} | {f["help"]["size"]}pt | ", self.cfg["aa"], f["help"]["color"])
        self.hex3 = self.font_help.render(f"{f["help"]["color"]}", self.cfg["aa"], f["help"]["color"])
        self.value4 = self.font_help.render(str(self.cfg["aa"]), self.cfg["aa"], "#00FF00" if self.cfg["aa"] else "#FF0000")

        self.value5 = self.font_help.render(str(self.cfg["floats"]), self.cfg["aa"], "#00FF00" if self.cfg["floats"] else "#FF0000")
        self.value6 = self.font_help.render(self.cfg["bg_color"], self.cfg["aa"], self.col_help)
        self.value7 = self.font_help.render(str(self.cfg["wpms"]), self.cfg["aa"], self.col_help)

    def handleKey(self, key):
        match key:
            case pygame.K_F4:
                self.cfg["aa"] = not self.cfg["aa"]
                self.txts()
            case pygame.K_F5:
                self.cfg["floats"] = not self.cfg["floats"]
                self.txts()
            case pygame.K_F12:
                self.cm.save(self.cfg)
                self.callback.txts()
                self.change_state(self.callback)

    def render(self, window, w, h):
        offset = self.label1.get_height()
        window.blit(self.label1, (100, 100))        
        window.blit(self.label2, (100, 100+offset))        
        window.blit(self.label3, (100, 100+offset*2))  
        window.blit(self.label4, (100, 100+offset*3))
        window.blit(self.label5, (100, 100+offset*5))        #blocks of 4
        window.blit(self.label6, (100, 100+offset*6))        
        window.blit(self.label7, (100, 100+offset*7))  
        window.blit(self.label8, (100, 100+offset*8))       
        window.blit(self.label12, (100, 100+offset*13))

        window.blit(self.value1, (600, 100))
        window.blit(self.hex1, (600+self.value1.get_width(), 100))
        window.blit(self.value2, (600, 100+offset))
        window.blit(self.hex2, (600+self.value2.get_width(), 100+offset))
        window.blit(self.value3, (600, 100+offset*2))
        window.blit(self.hex3, (600+self.value3.get_width(), 100+offset*2))
        window.blit(self.value4, (600, 100+offset*3))

        window.blit(self.value5, (600, 100+offset*5))
        window.blit(self.value6, (600, 100+offset*6))
        window.blit(self.value7, (600, 100+offset*7))