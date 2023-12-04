import pygame,sys
from pygame.locals import *
# from form_test import *
from form_main_menu import *
from db_score.db import *

pygame.init()
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
form_test = FormMain(screen, 100,100,600,400,(20, 20, 20),(10, 10, 10),
                    5, True)

crear_tabla()

while True:
    clock.tick(60)
    mouse_pos = pygame.mouse.get_pos()
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # print(event)
    # print(mouse_pos)
    screen.fill((0,0,0))
    
    form_test.update(eventos)
    
    pygame.display.update()
