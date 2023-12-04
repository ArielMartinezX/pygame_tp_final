import pygame
from auxiliar.utils import SurfaceManager as sf
from auxiliar.constantes import DEBUG

class Explotion(pygame.sprite.Sprite):
    def __init__(self, center, dimentions: tuple):
        super().__init__()

        self.__actual_frame = 0
        self.__actual_animation = sf.get_surface_from_spritesheet('./assets/graphics/explotion.png',5,2)
        self.image = self.__actual_animation[self.__actual_frame]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.__frame_rate = 35
        self.__update_time = pygame.time.get_ticks()
        self.__animation_done = False
    
    def update(self, screen: pygame.surface.Surface):
        current_time = pygame.time.get_ticks()
        if not self.__animation_done and current_time - self.__update_time > self.__frame_rate:
            self.__update_time = current_time
            center = self.rect.center
            if self.__actual_frame < len(self.__actual_animation):
                self.image = self.__actual_animation[self.__actual_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.__actual_frame += 1
                self.draw(screen)
            else:
                self.__animation_done = True
                self.kill()


    def draw(self, screen: pygame.surface.Surface):
        screen.blit(self.image, self.rect)