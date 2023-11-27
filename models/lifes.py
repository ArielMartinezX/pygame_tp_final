import pygame
from auxiliar.utils import SurfaceManager as sf
from auxiliar.constantes import DEBUG

class Life(pygame.sprite.Sprite):
    def __init__(self, x,y, aspect_ratio,life_increase):
        super().__init__()

        self.__image = pygame.image.load("assets\graphics\Sprite_heart.png") #PASAR AL JSON
        self.__image = pygame.transform.scale(self.__image, (self.__image.get_width() * aspect_ratio,
                        self.__image.get_height() * aspect_ratio))
        self.__rect = self.__image.get_rect(midbottom=(x,y))
        self.__collition_rect = pygame.Rect(self.__rect.x+17, self.__rect.y+20, self.__rect.w//2 -3, self.__rect.h-43)
        self.__life_increase = life_increase
        
    @property
    def rect(self):
        return self.__collition_rect   
    @property
    def life_restore(self):
        return self.__life_increase

    
    def draw(self, screen):
        if DEBUG:
            # pygame.draw.rect(screen, ((255,0,0)), self.__rect)
            pygame.draw.rect(screen, ((0,255,0)), self.__collition_rect)
                # pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
        screen.blit(self.__image,self.__rect)
