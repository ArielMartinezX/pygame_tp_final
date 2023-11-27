import pygame, random
from auxiliar.constantes import *
from models.player_1 import Player
from models.enemy import Enemy

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_h, limit_w, stage_name:str):
        self.__configs = open_configs().get(stage_name)
        self.__player_configs = self.__configs.get('player')
        self.__player_sprite = Player((limit_w / 2, limit_h),limit_w, 500,#limite pantalla
                                    self.__player_configs.get('walk_speed'),
                                    self.__player_configs.get('run_speed'),
                                    self.__player_configs.get('jump_power'),
                                    self.__player_configs.get('gravity'),
                                    self.__player_configs.get('aspect_ratio'),
                                    self.__player_configs.get('jump_limit'),
                                    self.__player_configs.get('frame_rate'))
        #configuraciones de stage
        self.__stage_configs = self.__configs.get('stage')
        #configuraciones de enemigos
        self.__enemy_configs = self.__configs.get('enemy')
        
        #creo grupo jugador y enemigos

        self.enemies = pygame.sprite.Group()
        self.create_enemies()
        #del json obtengo configuraciones del stage
        self.__stage_configs = self.__configs.get('stage')
        self.__stage_image = self.__stage_configs.get('stage_background')
        self.__max_enemies = self.__stage_configs.get('max_enemies_amount')
        self.__coordenadas_enemigos = self.__stage_configs.get('coords_enemies')
        #limites del stage
        self.__limit_w = limit_w
        self.__limit_h = limit_h
        #pantalla principal
        self.__main_screen = screen
        self.__tiempo_transcurrido = 0
    
    def create_enemies(self):
        for _ in range(self.__stage_configs.get('max_enemies_amount')):
            walk_speed = random.randint(self.__enemy_configs.get('enemy_min_speed'),
                                self.__enemy_configs.get('enemy_max_speed'))
            new_enemy = Enemy((200,200), SCR_WIDTH, walk_speed,
                            self.__enemy_configs.get('gravity'),
                            self.__enemy_configs.get('aspect_ratio'),
                            self.__enemy_configs.get('shoot_percentage')
                            )
            self.enemies.add(new_enemy)
    
    def run(self, delta_ms):
        self.__tiempo_transcurrido += delta_ms
        if self.__tiempo_transcurrido >= 17:
            self.__player_sprite.update(self.__main_screen, delta_ms)
            self.__player_sprite.draw(self.__main_screen)
            self.enemies.update(self.__main_screen, delta_ms)
            self.enemies.draw(self.__main_screen)
        else:
            self.__tiempo_transcurrido = 0