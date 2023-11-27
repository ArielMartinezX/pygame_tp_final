import pygame
import random
from models.fireball import Fireball
from auxiliar.utils import SurfaceManager as sf
from auxiliar.constantes import DEBUG,open_configs, GROUND
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w,constraint_h, walk_speed, gravity, aspect_ratio, fire_percentage, frame_rate, puntaje,
                walk_path, walk_cols, walk_rows, fall_path, fall_cols, fall_rows):
        super().__init__()
        self.__walk_r = sf.get_surface_from_spritesheet(walk_path, walk_cols, walk_rows)
        self.__walk_l = sf.get_surface_from_spritesheet(walk_path, walk_cols, walk_rows,flip=True)
        self.__walk_r = [ pygame.transform.scale(image, (image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_r]
        self.__walk_l = [ pygame.transform.scale(image, (image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_l]
        self.__fall_r = sf.get_surface_from_spritesheet(fall_path, fall_cols, fall_rows)
        self.__fall_l = sf.get_surface_from_spritesheet(fall_path, fall_cols, fall_rows,flip=True)
        self.__fall_r = [ pygame.transform.scale(image, (image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__fall_r]
        self.__fall_l = [ pygame.transform.scale(image, (image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__fall_l]
        #animacion
        self.__frame_rate = frame_rate
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__walk_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect(midbottom=pos)
        self.__ground_collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 +6, (self.__rect.y + self.__rect.height), self.__rect.w//2 -6, 6)
        
        #puntaje
        self.__score = puntaje
        #hitbox
        self.__collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 +6, (self.__rect.y + self.__rect.height), self.__rect.w//2 -6, 50)
        

        #Atributos de movimiento
        self.__walk_speed = walk_speed
        self.__max_constraint_w = constraint_w
        self.__max_constraint_h = constraint_h
        self.__gravity = gravity
        
        #donde esta mirando
        self.__is_looking_right = random.choice([True, False])
        
        #grupo tiros
        self.__fireball_group = pygame.sprite.Group()
        self.__fire_probability = fire_percentage
        self.__fire_random = 0
        self.__fire_counting_time = 0
        self.__fire_delay = 2000  #PASAR AL JSON

        #plataforma actual y nuevo constraint
        self.__current_platform = None
        self.__platform_stay = random.choice([True, False])
        
    @property
    def fireball_group(self):
        return self.__fireball_group
    
    @property
    def rect(self):
        return self.__collition_rect
    
    @property
    def score(self):
        return self.__score
    #animacion
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__rect.x += move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r

    def __set_y_animations_preset(self,move_y, animation_list: list[pygame.surface.Surface]):
        self.__rect.y += move_y
        self.__actual_animation = animation_list
        self.__initial_frame = 0
 
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms   
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0
    
    def draw(self, screen):
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)
        self.__ground_collition_rect.midbottom = self.__rect.midbottom
        self.__collition_rect.midbottom = self.__rect.midbottom
        # if DEBUG:
        #     pygame.draw.rect(screen,((255,255,255)),self.__collition_rect)
            
    
    def on_platform(self, lista_plataformas):
        self.__retorno = False
        if self.__ground_collition_rect.y >= GROUND: # aplica gravedad. 
            self.__retorno = True
            return self.__retorno
        else:
            for plataform in lista_plataformas:
                if self.__ground_collition_rect.colliderect(plataform.ground_collition_rect):
                    self.__retorno = True
                    self.__current_platform = plataform
                    break
        return self.__retorno
    
    def platform_constraint(self):
        if self.__current_platform != None:
            if self.__platform_stay:
                if self.__ground_collition_rect.left <= self.__current_platform.rect.left:
                    self.__ground_collition_rect.left = self.__current_platform.rect.left
                    self.__is_looking_right = True
                if self.__ground_collition_rect.right >= self.__current_platform.rect.right:
                    self.__ground_collition_rect.right = self.__current_platform.rect.right
                    self.__is_looking_right = False
                if self.__ground_collition_rect.bottom >= self.__current_platform.rect.top+1:
                    self.__ground_collition_rect.bottom = self.__current_platform.rect.top+1

    def update_player_properties(self):
        self.__rect.midbottom = self.__ground_collition_rect.midbottom
    
    def gravedad(self, lista_plataformas):
        if not self.on_platform(lista_plataformas):
            # self.__rect.y += self.__gravity
            if self.__is_looking_right:
                self.__set_y_animations_preset(self.__gravity, self.__fall_r)
            else:    
                self.__set_y_animations_preset(self.__gravity, self.__fall_l)

    def create_fireball(self, delta_ms):
        self.__fire_random = random.randint(0,6) #PASAR AL JSON
        self.__fire_counting_time += delta_ms
        if self.__fire_random > self.__fire_probability and self.__fire_counting_time > self.__fire_delay:
            self.__fire_counting_time = 0
            if self.__is_looking_right:
                return Fireball(self.__rect.right, self.__rect.y+42, self.__is_looking_right)
            else:
                return Fireball(self.__rect.left, self.__rect.y+42, self.__is_looking_right)
        return None

    
    def constrain(self):
        if not self.__platform_stay:
            if self.__rect.left <= 0:
                self.__rect.left = 0
                self.__is_looking_right = True
            if self.__rect.right >= self.__max_constraint_w:
                self.__rect.right = self.__max_constraint_w
                self.__is_looking_right = False
            
            if self.__rect.top <= 0:
                self.__rect.top = 0
            if self.__rect.bottom >= self.__max_constraint_h+1:
                self.__rect.bottom = self.__max_constraint_h+1
    
    def movement(self, lista_plataformas):
        if self.on_platform(lista_plataformas):
            if not self.__is_looking_right:
                # self.__rect.x += -self.__walk_speed 
                self.__set_x_animations_preset(-self.__walk_speed, self.__walk_l, self.__is_looking_right)
            else:
                self.__set_x_animations_preset(self.__walk_speed, self.__walk_r, self.__is_looking_right)
                # self.__rect.x += self.__walk_speed        
    
    def update(self, screen: pygame.surface.Surface, delta_ms, lista_plataformas):
        self.do_animation(delta_ms)
        new_fireball = self.create_fireball(delta_ms)
        if new_fireball:
            self.__fireball_group.add(new_fireball)
        self.__fireball_group.draw(screen)
        self.__fireball_group.update()
        self.gravedad(lista_plataformas)
        self.movement(lista_plataformas)
        self.constrain()
        self.platform_constraint()