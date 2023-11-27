

import pygame
from auxiliar.utils import SurfaceManager as sf
from auxiliar.constantes import DEBUG

class Trampas(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.__image = pygame.image.load("assets/graphics/spike.png") #PASAR AL JSON
        self.__rect = self.__image.get_rect(midbottom=(x,y))
        self.__ground_collition_rect = pygame.Rect(self.__rect.x, self.__rect.y+6, self.__rect.w-1 , self.__rect.h/2)

    @property
    def rect(self):
        return self.__ground_collition_rect   
    
    def draw(self, screen):
        if DEBUG:
            # pygame.draw.rect(screen, ((255,0,0)), self.__rect)
            pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
                # pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
        screen.blit(self.__image,self.__rect)
        # screen.blit(self.__actual_img_animation, self.__rect)
        
