import pygame
from pygame.locals import *
from models.game import Game

from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *
from UI.GUI_slider import *
from UI.GUI_textbox import *

class FormLevels(Form):
    def __init__(self, screen, x,y,w,h, color_background, color_border, active):
        super().__init__(screen, x,y,w,h,color_background, color_border,active)
        self.volumen = 0.2
        self.flag_play = True
        pygame.mixer.init()
        
        self.__player_name = None
        
        self.lbl_options_title = Label(self._slave, 100, 50, 400, 50,
                            "SELECT LEVEL", "Comic Sans",30,
                            (255,255,255),"./UI/Recursos/Table.png")
        
        self.btn_back = Button(self._slave,x,y,500,330,50,50,(30,30,30),(35,35,35),
                            self.btn_back_click,None,"<-",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        self.btn_lvl_1 = Button(self._slave,x,y,100,150,100,100,(40,40,40),(35,35,35),
                            self.btn_lvl_1_click,None,"1",
                            font="Comic Sans",font_size=30,font_color=(255,255,255))
        self.btn_lvl_2 = Button(self._slave,x,y,250,150,100,100,(40,40,40),(35,35,35),
                            self.btn_lvl_2_click,None,"2",
                            font="Comic Sans",font_size=30,font_color=(255,255,255))
        self.btn_lvl_3 = Button(self._slave,x,y,400,150,100,100,(40,40,40),(35,35,35),
                            self.btn_lvl_3_click,None,"3",
                            font="Comic Sans",font_size=30,font_color=(255,255,255))
        self.lbl_name_info = Label(self._slave, 100, 260, 400, 40,
                            "WRITE YOUR NAME, PRESS ENTER", "Comic Sans",15,
                            (255,255,255),"./UI/Recursos/Table.png")
        
        self.txtbox_player_name = TextBox(self._slave,x,y,200,300, 200,50,
                            (220,220,220),(255,255,255),(255,255,255),(255,0,0),
                            2,font="Comic Sans", font_size=30, font_color=(0,0,0))
        
        self.lista_widgets.append(self.lbl_options_title)
        self.lista_widgets.append(self.btn_back)
        self.lista_widgets.append(self.btn_lvl_1)
        self.lista_widgets.append(self.btn_lvl_2)
        self.lista_widgets.append(self.btn_lvl_3)
        self.lista_widgets.append(self.txtbox_player_name)
        self.lista_widgets.append(self.lbl_name_info)
        
        self.__game = Game()
        
        self.name = "levels"
        self.__player_name = None
        self.__player_changed = False
    
        
    def render(self): 
        self._slave.fill(self._color_background)
    
    def btn_back_click(self,texto):
        #self.end_dialog()
        self.go_back()
    
    def btn_lvl_1_click(self,texto):
        if self.__player_name:
            self.__game.run_game("stage_1", self.__player_name)

    def btn_lvl_2_click(self,texto): 
        if self.__game.stage_1_passed and not self.__player_changed:      
            self.__game.run_game("stage_2", self.__player_name)
        
    def btn_lvl_3_click(self,texto):
        if self.__game.stage_2_passed and not self.__player_changed:
            self.__game.run_game("stage_3", self.__player_name)
    
    def txtbox_player_name_input(self):
        self.check_game_values_if_player_change(self.txtbox_player_name.get_text())
        self.__player_name = self.txtbox_player_name.get_text()
        print(self.__player_name)
    
    def check_game_values_if_player_change(self, text_input):
        if self.__player_name != text_input:
            self.__player_changed = True
            
    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                for evento in lista_eventos:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN:
                            self.txtbox_player_name_input()
        else:
            self.hijo.update(lista_eventos)