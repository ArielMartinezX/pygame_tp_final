import pygame
from auxiliar.utils import SurfaceManager as sf
from auxiliar.constantes import DEBUG

class Objetos(pygame.sprite.Sprite):
    def __init__(self, x,y, aspect_ratio, frame_rate, puntaje, item_img_path,
            item_cols, item_rows):
        super().__init__()

        self.__image = sf.get_surface_from_spritesheet(item_img_path, item_cols, item_rows)
        self.__image = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__image]
        #atributos animacion
        self.__frame_rate = frame_rate
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__image
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect(midbottom=(x,y))
        self.__ground_collition_rect = pygame.Rect(self.__rect.x+17, self.__rect.y+20, self.__rect.w//2 -3, self.__rect.h-43)
        self.__puntaje = puntaje
    @property
    def rect(self):
        return self.__ground_collition_rect   
    @property
    def score(self):
        return self.__puntaje
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms   
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    
    def draw(self, screen):
        if DEBUG:
            pygame.draw.rect(screen, ((255,0,0)), self.__rect)
            pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
                # pygame.draw.rect(screen, ((0,255,0)), self.__ground_collition_rect)
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation,self.__rect)
        # screen.blit(self.__actual_img_animation, self.__rect)
        
    def update(self,screen: pygame.surface.Surface, delta_ms):
        self.do_animation(delta_ms)