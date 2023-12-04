# import pygame
# from pygame.locals import *

# from UI.GUI_button import *
# from UI.GUI_slider import *
# from UI.GUI_textbox import *
# from UI.GUI_label import *
# from UI.GUI_form import *
# from UI.GUI_button_image import *
# from UI.GUI_form_menu_score import *

# class FormMain(Form):
    
#     def __init__(self, screen:pygame.Surface, x:int, y:int, w:int, h:int, color_background, color_border: (0,0,0),
#                 border_size: int = -1, active = True):
#         super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)
        
#         self.volumen = 0.2
#         self.flag_play = True

#         pygame.mixer.init()
        
#         ####CONTROLES
        
#         self.txtbox = TextBox(self._slave,x,y, 50,50, 150,30,
#                             (220,220,220),(255,255,255),(255,255,255),(255,0,0),
#                             2,font="Comic Sans", font_size=15, font_color=(0,0,0))
        
#         self.btn_play = Button(self._slave, x,y,100,100,
#                             100,50,(255,0,0),(0,0,255),
#                             self.btn_play_click,"nombre","pause",
#                             font="Verdana",font_size=15,font_color=(255,255,255))

#         # D
        
#         self.label_volumen = Label(self._slave, 200, 190, 50, 50,
#                                 "20%", "Comic Sans",15,
#                                 (255,0,0),"./UI/Recursos/Table.png")
#         self.slider_volumen = Slider(self._slave, x,y,
#                                     100,200,300,15,self.volumen,
#                                     (0,0,255),(255,255,255))
#         self.btn_tabla = Button_Image(self._slave,x,y,255,100,50,50,
#                                     "./UI/Recursos/Menu_BTN.png",self.btn_tabla_click,"lalala"
#                                     )
#         ####
        
#         #AGREGARLOS A LA LISTA  
#         self.lista_widgets.append(self.txtbox)
#         self.lista_widgets.append(self.btn_play)
#         self.lista_widgets.append(self.label_volumen)
#         self.lista_widgets.append(self.slider_volumen)
#         self.lista_widgets.append(self.btn_tabla)
#         # self.lista_widgets.append(self.btn_start)
#         ######################################
#         pygame.mixer.music.load("halloween.wav")
        
#         pygame.mixer.music.set_volume(self.volumen)
#         pygame.mixer.music.play(-1)
        
#         self.render()
    
#     def update(self, lista_eventos):
#         if self.verificar_dialog_result():
#             if self.active:
#                 self.draw()
#                 self.render()
#                 for widget in self.lista_widgets:
#                     widget.update(lista_eventos)
#                 self.update_volumen(lista_eventos)
#         else:
#             self.hijo.update(lista_eventos)
            
#     def render(self): 
#         self._slave.fill(self._color_background)
    
#     def btn_play_click(self, texto):
#         if self.flag_play:
#             pygame.mixer.music.pause()
#             self.btn_play._color_background = (0,255,255)
#             self.btn_play._font_color = (255,0,0)
#             self.btn_play.set_text("Play")
#         else:
#             pygame.mixer.music.unpause()
#             self.btn_play._color_background = (255,0,0)
#             self.btn_play._font_color = (255,255,255)
#             self.btn_play.set_text("Pause")
#         self.flag_play = not self.flag_play
        
#     def update_volumen(self, lista_eventos):
#         self.volumen = self.slider_volumen.value
#         self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
#         pygame.mixer.music.set_volume(self.volumen)
    
#     def btn_tabla_click(self,texto):
#         print("hola")
#         dic_score = [{"jugador": "gio"},{"score": 1000},
#                     {"jugador": "fausto"},{"score": 900},
#                     {"jugador": "gonza"},{"score": 750}
#                     ]

#         form_puntaje = FormMenuScore(self._master, 100, 25, 600,550,(220,0,220),
#                                     (255,255,255),True,"./UI/Recursos/Window.png",
#                                     dic_score,100,10,10)

#         self.show_dialog(form_puntaje)