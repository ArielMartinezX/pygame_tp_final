import pygame, sys
from pygame.locals import *

from UI.GUI_button import *
from UI.GUI_slider import *
from UI.GUI_textbox import *
from UI.GUI_label import *
from UI.GUI_form import *
from UI.GUI_button_image import *
from UI.GUI_form_menu_score import *
from form_options_menu import *
from UI.gui_form_levels import *

class FormPause(Form):
    
    def __init__(self, screen:pygame.Surface, x:int, y:int, w:int, h:int, color_background, color_border: (0,0,0),
                border_size: int = -1, active = True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)
        
        self.volumen = 0.2
        self.flag_play = True

        pygame.mixer.init()
        
        ####CONTROLES
        self.lbl_title = Label(self._slave, 100, 50, 400, 50,
                            "GAME PAUSED", "Comic Sans",30,
                            (255,255,255),"./UI/Recursos/Table.png")
        
        self.label_volumen = Label(self._slave, 330, 130, 50, 50,
                                "20%", "Comic Sans",15,
                                (255,255,255),"./UI/Recursos/Table.png")
        self.slider_volumen = Slider(self._slave, x,y,
                                    150,200,300,15,self.volumen,
                                    (0,0,255),(255,255,255))
        self.btn_music_state = Button(self._slave, x,y,220,130,
                            100,45,(30,30,30),(35,35,35),
                            self.btn_music_state_click,None,"PAUSE",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        self.btn_quit = Button(self._slave,x,y,500,330,50,50,(30,30,30),(35,35,35),
                            self.btn_quit_click,None,"X",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
    
        self.lista_widgets.append(self.lbl_title)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_music_state)
        self.lista_widgets.append(self.btn_quit)

        # pygame.mixer.music.load("./UI/Recursos/main_music.mp3")
        # pygame.mixer.music.set_volume(self.volumen)
        # pygame.mixer.music.play(-1)
        self.render()
        
    def update_volumen(self, lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)
        
    def btn_music_state_click(self, texto):
        if self.flag_play:
            pygame.mixer.music.pause()
            self.btn_music_state._color_background = (30,30,30)
            self.btn_music_state._font_color = (255,255,255)
            self.btn_music_state.set_text("PLAY")
        else:
            pygame.mixer.music.unpause()
            self.btn_music_state._color_background = (35,35,35)
            self.btn_music_state._font_color = (255,255,255)
            self.btn_music_state.set_text("PAUSE")
        self.flag_play = not self.flag_play
    
    def btn_quit_click(self,texto):
        if self.flag_play:
            pygame.quit()
            sys.exit()
            
    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)
            
    def render(self): 
        self._slave.fill(self._color_background)
    

