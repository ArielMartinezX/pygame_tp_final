import pygame
from pygame.locals import *

from UI.GUI_button_image import *
from UI.GUI_form import *
from UI.GUI_label import *

from db_score.db import *

class FormRanking(Form):
    def __init__(self, screen, x,y,w,h, color_background, color_border, active,
                path_image, score, margen_y, margen_x, espacio):
        super().__init__(screen, x,y,w,h,color_background, color_border,active)
        aux_imagen = pygame.image.load(path_image)
        aux_imagen = pygame.transform.scale(aux_imagen,(w,h))
        
        self._slave = aux_imagen
        self._score = score
        
        self._margen_y = margen_y
        
        self.lbl_jugador = Label(self._slave, x=margen_x + 10, y=20, w=w/2-margen_x-10,
                    h=50, text="PLAYER",font="Comic Sans",
                    font_size=30, font_color=(255,255,255),
                    path_image="./UI/Recursos/bar.png")
        self.lbl_puntaje = Label(self._slave, x=margen_x + 10+w/2-margen_x-10, y=20, w=w/2-margen_x-10,
                    h=50, text="SCORE",font="Comic Sans",
                    font_size=30, font_color=(255,255,255),
                    path_image="./UI/Recursos/bar.png")
        self.btn_back = Button(self._slave,x,y,500,450,50,50,(30,30,30),(35,35,35),
                            self.btn_back_click,None,"<-",
                            font="Comic Sans",font_size=30,font_color=(255,255,255))
        
        self.lista_widgets.append(self.lbl_jugador)
        self.lista_widgets.append(self.lbl_puntaje)
        self.lista_widgets.append(self.btn_back)
        
        pos_inicial_y = margen_y
        
        for j in self._score:
            pos_inicial_x = margen_x
            for n,s in j.items():
                cadena = ""
                cadena = f"{s}"
                jugador = Label(self._slave, pos_inicial_x, pos_inicial_y, w/2-margen_x,
                            100, cadena.upper(), font="Comic Sans", font_size=30,font_color=(255,255,255),
                            path_image="./UI/Recursos/Table.png")
                self.lista_widgets.append(jugador)
                pos_inicial_x += w/2-margen_x
            pos_inicial_y += espacio
            
    def btn_back_click(self,texto):
        #self.end_dialog()
        self.go_back()
        
    def update(self, lista_eventos):
        if self.active:
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
    
    # def get_data(self):
    #     filas = get_lista()
    #     resultado_diccionario = []
    #     for fila in filas:
    #         fila_diccionario = {}
    #         for i in range(len(fila)):
    #             columna_nombre = filas[0][i]  # Supongo que la primera fila contiene los nombres de las columnas
    #             valor = fila[i]
    #             fila_diccionario[columna_nombre] = valor
    #         resultado_diccionario.append(fila_diccionario)
    #     return resultado_diccionario