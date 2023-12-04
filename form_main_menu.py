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

class FormMain(Form):
    
    def __init__(self, screen:pygame.Surface, x:int, y:int, w:int, h:int, color_background, color_border: (0,0,0),
                border_size: int = -1, active = True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)
        
        self.volumen = 0.2
        self.flag_play = True

        pygame.mixer.init()
        
        ####CONTROLES
        self.lbl_title = Label(self._slave, 100, 50, 400, 50,
                            "OWLET MONSTER", "Comic Sans",30,
                            (255,255,255),"./UI/Recursos/Table.png")
        
        self.btn_start_game = Button(self._slave,x,y,180,150,250,50,(30,30,30),(35,35,35),
                            self.btn_start_click,"nombre","START GAME",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        self.btn_options = Button(self._slave,x,y,180,210,250,50,(30,30,30),(35,35,35),
                            self.btn_options_click,"nombre","OPTIONS",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        self.btn_quit = Button(self._slave,x,y,500,330,50,50,(30,30,30),(35,35,35),
                            self.btn_quit_click,None,"X",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        self.btn_ranking = Button(self._slave,x,y,180,270,250,50,(30,30,30),(35,35,35),
                            self.btn_ranking_click,"nombre","RANKING",
                            font="Comic Sans",font_size=15,font_color=(255,255,255))
        
        #AGREGARLOS A LA LISTA  

        self.lista_widgets.append(self.btn_start_game)
        self.lista_widgets.append(self.btn_options)
        self.lista_widgets.append(self.lbl_title)
        self.lista_widgets.append(self.btn_quit)
        self.lista_widgets.append(self.btn_ranking)
        ######################################
        
        pygame.mixer.music.load("./UI/Recursos/main_music.mp3")
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play(-1)
        
        self.__form_levels = FormLevels(self._master,100,100,600,400,(20, 20, 20),(10, 10, 10),True)
        self.name = "main"
        self.render()
    
    def update(self, lista_eventos):
        if self.verificar_dialog_result(): 
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                # self.update_volumen(lista_eventos)      
        else:
            self.hijo.update(lista_eventos)
            
    def render(self): 
        self._slave.fill(self._color_background)
    
    def btn_quit_click(self,texto):
        if self.flag_play:
            # for event in lista_eventos:
            #     print(event)
            #     if event.type == pygame.QUIT:
            #         pygame.quit()
            #         sys.exit()
            pygame.quit()
            sys.exit()
                    
    def btn_start_click(self, texto):
        print(self.flag_play)
        if self.flag_play:
            self.__form_levels.active = True
            self.show_dialog(self.__form_levels)

    def btn_options_click(self,texto):
        if self.flag_play:
            form_options = FormMenuOptions(self._master,100,100,600,400,(20, 20, 20),(10, 10, 10),
                    True)
            self.show_dialog(form_options)
    
    def btn_ranking_click(self,texto):
        if self.flag_play:
            dic_score = self.get_data()
            print(dic_score)
            form_puntaje = FormRanking(self._master, 100, 25, 600,550,(220,0,220),
                                     (255,255,255),True,"./UI/Recursos/Window.png",
                                     dic_score,100,10,10)
            self.show_dialog(form_puntaje)
    
    # def btn_tabla_click(self,texto):
    #     print("hola")
    #     dic_score = [{"jugador": "gio"},{"score": 1000},
    #                 {"jugador": "fausto"},{"score": 900},
    #                 {"jugador": "gonza"},{"score": 750}
    #                 ]

    #     form_puntaje = FormMenuScore(self._master, 100, 25, 600,550,(220,0,220),
    #                                 (255,255,255),True,"./UI/Recursos/Window.png",
    #                                 dic_score,100,10,10)

    #     self.show_dialog(form_puntaje)
    
    def get_data(self):
        filas = get_lista()
        print(filas)
        resultado_diccionario = []
        for fila in filas:
            fila_diccionario = {}
            for i in range(len(fila)):
                columna_nombre = filas[0][i]  # Suponemos que la primera fila contiene los nombres de las columnas
                valor = fila[i]
                fila_diccionario[columna_nombre] = valor
            resultado_diccionario.append(fila_diccionario)
        return resultado_diccionario
    