import pygame
from auxiliar.utils import SurfaceManager as sf
from models.fireball import Fireball
from models.explotion import Explotion
from auxiliar.constantes import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w,constraint_h, walk_speed,run_speed, jump_power, gravity, aspect_ratio, frame_rate, lifes, fire_cooldown,
                idle_path,idle_cols,idle_rows, walk_path, walk_cols, walk_rows, jump_path, jump_cols, jump_rows, attack_path, attack_cols, attack_rows,
                death_path, death_cols, death_rows):
        super().__init__()

        self.__iddle_r = sf.get_surface_from_spritesheet(idle_path, idle_cols, idle_rows)
        self.__iddle_l = sf.get_surface_from_spritesheet(idle_path, idle_cols, idle_rows, flip=True)
        self.__iddle_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__iddle_r]
        self.__iddle_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__iddle_l]
        self.__walk_r = sf.get_surface_from_spritesheet(walk_path,walk_cols,walk_rows)
        self.__walk_l = sf.get_surface_from_spritesheet(walk_path,walk_cols,walk_rows,flip=True)
        self.__walk_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_r]
        self.__walk_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__walk_l]
        self.__jump_r = sf.get_surface_from_spritesheet(jump_path,jump_cols,jump_rows)
        self.__jump_l = sf.get_surface_from_spritesheet(jump_path,jump_cols,jump_rows,flip=True)
        self.__jump_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__jump_r]
        self.__jump_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__jump_l]
        self.__attack_r = sf.get_surface_from_spritesheet(attack_path, attack_cols, attack_rows)
        self.__attack_l = sf.get_surface_from_spritesheet(attack_path, attack_cols, attack_rows,flip=True)
        self.__attack_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__attack_r]
        self.__attack_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__attack_l]
        self.__death_r = sf.get_surface_from_spritesheet(death_path, death_cols, death_rows)
        self.__death_l = sf.get_surface_from_spritesheet(death_path, death_cols, death_rows, flip=True)
        self.__death_r = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__death_r]
        self.__death_l = [pygame.transform.scale(image,(image.get_width() * aspect_ratio, image.get_height() * aspect_ratio)) for image in self.__death_l]
        
        self.__frame_rate = frame_rate
        self.__frame_rate_stay = 200 #PASAR AL JSON
        self.__frame_rate_walk = 200 #PASAR AL JSON
        self.__frame_rate_shoot = 500 #PASAR AL JSON
        self.__frame_rate_death = 500 #PASAR AL JSON
        self.__player_animation_time = 0
        self.__initial_frame = 0
        self.__actual_animation = self.__iddle_r
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        self.__rect = self.__actual_img_animation.get_rect(midbottom=pos)
        #vidas
        self.__lifes = lifes
        self.__life_sound = pygame.mixer.Sound('assets/sounds/life_sound.mp3') #PASAR AL JSON
        #animacion muerte
        self.__death_animation_times = False
        #sonido muerte
        self.__game_over_sound = pygame.mixer.Sound('assets/sounds/game_over.wav') #PASAR AL JSON
        self.__game_over = False
        #donde esta mirando
        self.__is_looking_right = True
        
        #disparos
        self.__fireball_group = pygame.sprite.Group()
        self.__fire_cooldown = fire_cooldown
        self.__fire_ready = True
        self.__shoot_time = 0
        self.__shoot_sound = pygame.mixer.Sound('assets/sounds/fire_shoot.mp3') #PASAR AL JSON
        self.__damage_sound = pygame.mixer.Sound('assets/sounds/hit_sound.wav') #PASAR AL JSON
        # #HITBOX
        self.__ground_collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 + 6, (self.__rect.y + self.__rect.height), self.__rect.w//2 - 6, 6)
        self.__collition_rect = pygame.Rect(self.__rect.x + self.__rect.w//4 + 6, (self.__rect.y + self.__rect.height), self.__rect.w//2 - 6, 50)
        
        #Atributos de movimiento
        self.__walk_speed = walk_speed
        self.__run_speed = run_speed
        self.__max_constraint_w = constraint_w
        self.__max_constraint_h = constraint_h
        
        #salto
        self.__jump_power = jump_power
        self.__gravity = gravity
        self.__salto = jump_power
        self.__jump_sound = pygame.mixer.Sound('assets/sounds/jump_sound.mp3') #PASAR AL JSON
        self.__total_jump_movents = 21
        
        #plataformas
        self.__retorno = False
        
        #test salto
        self.__is_jumping = False
        
        #puntaje
        self.__puntaje = 0
    #propiedad del grupo disparo
    @property   
    def fireball_group(self):        
        return self.__fireball_group
    @property
    def rect(self):
        return self.__collition_rect
    @property
    def lifes(self):
        return self.__lifes
    @property
    def rect_ground(self):
        return self.__ground_collition_rect
    @property
    def hit(self):
        return self.__damage_sound
    @property
    def death(self):
        return self.__game_over_sound
    @property
    def life_up(self):
        return self.__life_sound
    @property
    def score(self):
        return self.__puntaje
    @score.setter
    def new_score(self, value):
        self.__puntaje = value
        
    @property
    def life(self):
        return self.__lifes
    @life.setter
    def life_counter(self, value):
        self.__lifes = value
    
    def restar_vida(self):
        if self.__lifes > 0:
            self.__lifes -= 1
        else:
            self.__lifes = 0

    def explotion(self):
        return pygame.sprite.GroupSingle(Explotion(self.__rect.center,(30,30)))
    
    def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
        self.__rect.x += move_x
        self.__actual_animation = animation_list
        self.__is_looking_right = look_r
    
    def __set_y_animations_preset(self,move_y, frame: int):
        self.__rect.y -= move_y
        self.__actual_animation = [self.__jump_r[frame]] if self.__is_looking_right else [self.__jump_l[frame]]
        self.__initial_frame = 0
        self.__is_jumping = True 
    
    def do_animation(self, delta_ms):
        self.__player_animation_time += delta_ms   
        if self.__player_animation_time >= self.__frame_rate:
            self.__player_animation_time = 0
            if self.__initial_frame < len(self.__actual_animation) - 1:
                self.__initial_frame += 1
            else:
                self.__initial_frame = 0

    
    def on_platform(self, lista_plataformas):
        self.__retorno = False
        if self.__ground_collition_rect.y >= GROUND: # aplica gravedad. 
            self.__retorno = True
            return self.__retorno
        else:
            for plataform in lista_plataformas:
                if self.__ground_collition_rect.colliderect(plataform.ground_collition_rect):
                    self.__retorno = True
                    break
        return self.__retorno
    
    def get_inputs(self, lista_eventos, lista_plataformas):
        
        if self.__lifes > 0:    
            
            for event in lista_eventos:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not self.__is_jumping and self.on_platform(lista_plataformas):
                        self.__is_jumping = True
                        self.__jump_sound.play()
                
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.__is_right = False
                self.walk(self.__is_right)
            if keys[pygame.K_d]:
                self.__is_right = True
                self.walk(self.__is_right)
            if not keys[pygame.K_a] and not keys[pygame.K_d]:
                self.stay()
            if keys[pygame.K_k] and self.__fire_ready:
                self.shoot_fireball()
                self.__shoot_sound.play()
                self.__fire_ready = False
                self.__shoot_time = pygame.time.get_ticks()
        else:
            if not self.__death_animation_times: 
                self.is_dead()
                self.__death_animation_times = True

            else:
                if self.__death_animation_times and self.__initial_frame == 7:
                    self.__actual_animation = [self.__death_r[3]] if self.__is_looking_right else [self.__death_l[3]]
                    self.__initial_frame = 0    

    def is_alive(self):
        if self.__lifes > 0:
            return True
        return False

    def check_traps(self, trampas):
        if trampas:
            if self.__is_looking_right:
                self.__rect.x -= 25 #PASAR AL JSON
            else:
                self.__rect.x += 25 #PASAR AL JSON
            self.__rect.y -= 12 #PASAR AL JSON
                
            self.__damage_sound.play()
            self.restar_vida()
            
            if self.__lifes == 0 and not self.__game_over:
                self.__game_over_sound.play()
                self.__game_over = True
    
    def check_body_to_body_collitions(self,cuerpo_a_cuerpo):
        if cuerpo_a_cuerpo and self.__lifes > 0:
            self.restar_vida()
            self.__damage_sound.play()
            if self.__is_looking_right:
                self.__rect.x -= 70 #PASAR AL JSON
            else:
                self.__rect.x += 70 #PASAR AL JSON
            self.__rect.y -= 5 #PASAR AL JSON
            
    # def saltar(self, lista_plataformas):
    #     if self.__is_jumping:
    #         if self.__salto >= -self.__jump_power:
    #             self.__rect.y -= self.__salto + 10
    #             keys = pygame.key.get_pressed()
    #             if keys[pygame.K_a]:
    #                 self.__rect.x -= self.__run_speed
    #             if keys[pygame.K_d]:
    #                 self.__rect.x += self.__run_speed
    #             self.__salto -= 0.5
    #         elif self.on_platform(lista_plataformas):
    #             self.__is_jumping = False
    #             self.__salto = self.__jump_power
                
    def saltar(self, lista_plataformas):
        if self.__is_jumping:
            if self.__salto >= -self.__jump_power:
                self.__set_y_animations_preset( self.__salto + 10, self.handle_jump_animation())
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    self.__rect.x -= self.__run_speed
                if keys[pygame.K_d]:
                    self.__rect.x += self.__run_speed
                self.__salto -= 0.5
                self.__total_jump_movents -=1
            elif self.on_platform(lista_plataformas):
                self.__is_jumping = False
                self.__total_jump_movents = 21
                self.__salto = self.__jump_power  
                
    def handle_jump_animation(self):
        if self.__total_jump_movents == 21: 
            return 0
        if self.__total_jump_movents <= 20 and self.__total_jump_movents >= 19:
            return 1
        if self.__total_jump_movents <= 18 and self.__total_jump_movents >= 17:
            return 2
        if self.__total_jump_movents <= 18 and self.__total_jump_movents >= 11:
            return 3
        if self.__total_jump_movents <= 10 and self.__total_jump_movents >= 7:
            return 4
        if self.__total_jump_movents <= 6 and self.__total_jump_movents >= 3:
            return 5
        if self.__total_jump_movents <= 2 and self.__total_jump_movents >= 1:
            return 6
        return 7                

    def is_dead(self):
        self.__frame_rate = self.__frame_rate_death
        self.__actual_animation = self.__death_r if self.__is_looking_right else self.__death_l

    def stay(self):
        self.__frame_rate = self.__frame_rate_stay
        if self.__actual_animation != self.__iddle_l and self.__actual_animation != self.__iddle_r:
            self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
            self.__initial_frame = 0
    
    def walk(self, look_right=True):
        self.__frame_rate = self.__frame_rate_walk
        if look_right:
            self.__set_x_animations_preset(self.__walk_speed, self.__walk_r, look_r=look_right)
        else:
            self.__set_x_animations_preset(-self.__walk_speed, self.__walk_l, look_r=look_right)


    def constraint(self):
        if self.__rect.left  <= 0 -16:
            self.__rect.left = 0 -16
        if self.__rect.right >= self.__max_constraint_w+16:
            self.__rect.right = self.__max_constraint_w+16

        if self.__rect.top <= 0:
            self.__rect.top = 0
        if self.__rect.bottom >= self.__max_constraint_h+1:
            self.__rect.bottom = self.__max_constraint_h+1
    
    def gravedad(self, lista_plataformas):
        if not self.on_platform(lista_plataformas):
            self.__rect.y += self.__gravity

    def create_fireball(self, direction):
        if direction:
            return Fireball(self.__rect.right, self.__rect.y+42, self.__is_looking_right)
        else:
            return Fireball(self.__rect.left, self.__rect.y+42, self.__is_looking_right)
            
    def shoot_fireball(self):
        self.__frame_rate = self.__frame_rate_shoot
        self.__fireball_group.add(self.create_fireball(self.__is_looking_right))
        self.__actual_animation = [self.__attack_r[2]] if self.__is_looking_right else [self.__attack_l[2]]
        self.__initial_frame = 0

    def remove_fireball(self, fireball):
        self.__fireball_group.remove(fireball)
    
    def fire_cooldown(self):
        if not self.__fire_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.__shoot_time >= self.__fire_cooldown:
                self.__fire_ready = True
                
    def draw(self, screen):
        self.__actual_img_animation = self.__actual_animation[self.__initial_frame]
        screen.blit(self.__actual_img_animation, self.__rect)
        if DEBUG:
            self.__ground_collition_rect.midbottom = self.__rect.midbottom
            self.__collition_rect.midbottom = self.__rect.midbottom
            pygame.draw.rect(screen,((0,0,255)),self.__collition_rect)
        self.__ground_collition_rect.midbottom = self.__rect.midbottom
        self.__collition_rect.midbottom = self.__rect.midbottom

    def update(self, screen: pygame.surface.Surface, delta_ms, lista_plataformas, lista_eventos, trampas, cuerpo_a_cuerpo):
        self.get_inputs(lista_eventos, lista_plataformas)
        self.constraint()
        self.do_animation(delta_ms)
        self.gravedad(lista_plataformas)
        self.fire_cooldown()
        self.saltar(lista_plataformas)
        self.check_traps(trampas)
        self.check_body_to_body_collitions(cuerpo_a_cuerpo)
        self.__fireball_group.draw(screen)
        self.__fireball_group.update()