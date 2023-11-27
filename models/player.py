import pygame,sys


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint_w,constraint_h, walk_speed,run_speed, jump_power, gravity, aspect_ratio, jump_limit):
        super().__init__()
        
        #Mostrar sprite del player
        self.image = pygame.image.load(r'assets\graphics\stand_test.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * aspect_ratio
                        ,self.image.get_height() * aspect_ratio))
        self.rect = self.image.get_rect(midbottom=pos)
        
        #HITBOX
        self.__hitbox = pygame.Rect(self.rect.x , self.rect.y, self.rect.width, self.rect.height)
        self.debug = True
        #Atributos de movimiento
        self.__walk_speed = walk_speed
        self.__run_speed = run_speed
        self.__max_constraint_w = constraint_w
        self.__max_constraint_h = constraint_h
        
        #salto
        self.__space_pressed= False
        self.__is_jumping = False
        self.__jump_power = jump_power
        self.__salto_anterior = jump_power
        self.__jump_energy = jump_limit
        
        #testeo salto v.2
        self.__jump_velocity = self.__jump_power
        #gravedad
        self.__gravity = gravity
        
        #donde esta mirando
        self.__is_right = True
        
    # def __set_x_animations_preset(self, move_x, animation_list: list[pygame.surface.Surface], look_r: bool):
    #     self.rect.x = move_x
    #     self.__actual_animation = animation_list
    #     self.__is_looking_right = look_r
        
    
    # def __set_y_animations_preset(self,move_y, animation_list: list[pygame.surface.Surface], look_r: bool):
    #     self.rect.y = -self.__jump
    #     self.rect.x = self.__speed_run if self.__is_looking_right else -self.__speed_run
    #     self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
    #     self.__initial_frame = 0
    #     self.__is_jumping = True 

    def update_hitbox(self):
        self.__hitbox.topleft = (self.rect.x, self.rect.y)
        
    def get_inputs(self):

        # for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.quit()
        #             sys.exit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.jump()
                    self.update_hitbox()

            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_SPACE:
                    # self.__space_pressed = False
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.__is_right = False
            self.walk(self.__is_right)
        if keys[pygame.K_d]:
            self.__is_right = True
            self.walk(self.__is_right)
        if keys[pygame.K_a] and keys[pygame.K_LSHIFT]:
            self.__is_right = False
            self.run(self.__is_right)
        if keys[pygame.K_d] and keys[pygame.K_LSHIFT]:
            self.__is_right = True
            self.run(self.__is_right)
        # if keys[pygame.K_SPACE]and self.__space_pressed == False:
        #     print("toque espacio")
        #     self.jump()
        #     self.update_hitbox()
        
    
    def walk(self, look_right=True):
        if look_right:
            self.rect.x += self.__walk_speed
        else:
            self.rect.x += -self.__walk_speed
        self.update_hitbox()
        
    def run(self, look_right=True):
        if look_right:
            self.rect.x += self.__run_speed
        else:
            self.rect.x += -self.__run_speed
        self.update_hitbox()
    
    def jump(self):
        if not self.__space_pressed and not self.__is_jumping:
            self.__space_pressed = True
            self.__is_jumping = True
            if self.__is_jumping:
                self.rect.y -= self.__jump_power
        
        if self.rect.bottom >= self.__max_constraint_h:
            self.rect.bottom = self.__max_constraint_h
            self.__is_jumping = False
            self.__space_pressed = False
        
        # if not self.__space_pressed and not self.__is_jumping:
        #     self.__space_pressed = True
        #     self.__is_jumping = True
        #     self.rect.y -= self.__jump_velocity
        #     self.rect.x += -self.__walk_speed
        #     self.__jump_velocity -= self.__gravity
        #     if self.__jump_velocity < -self.__jump_power:
        #         self.__jump_velocity = self.__jump_power
        # if self.rect.bottom >= self.__max_constraint_h:
        #     self.__is_jumping = False
        #     self.__space_pressed = False
        #     self.rect.bottom = self.__max_constraint_h
        
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.__max_constraint_w:
            self.rect.right = self.__max_constraint_w

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.__max_constraint_h:
            self.rect.bottom = self.__max_constraint_h
    
    def gravedad(self):
        if self.rect.bottom >= 0:
            self.rect.y += self.__gravity

    def draw(self, screen):
        if self.debug:
            pygame.draw.rect(screen,((255,0,0)),self.rect)
    
    def update(self, screen: pygame.surface.Surface):
        self.get_inputs()
        self.constraint()
        self.gravedad()        
        self.draw(screen)
        pygame.draw.rect(screen, (255, 0, 0), self.__hitbox, 2)