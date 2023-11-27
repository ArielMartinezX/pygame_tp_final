import pygame, random
from auxiliar.constantes import *
from models.player_1 import Player
from models.enemy import Enemy
from models.objetos import Objetos
from models.plataformas import Platform
from models.trampas import Trampas
from models.lifes import Life

class Stage:
    def __init__(self, screen: pygame.surface.Surface, limit_h, limit_w, stage_name:str):
        self.__configs = open_configs().get(stage_name)
        self.__player_configs = self.__configs.get('player')
        self.__player_sprite = Player((limit_w / 2, limit_h),limit_w, GROUND,#limite pantalla
                                    self.__player_configs.get('walk_speed'),
                                    self.__player_configs.get('run_speed'),
                                    self.__player_configs.get('jump_power'),
                                    self.__player_configs.get('gravity'),
                                    self.__player_configs.get('aspect_ratio'),
                                    self.__player_configs.get('frame_rate'),
                                    self.__player_configs.get('lifes'),
                                    self.__player_configs.get('fire_cooldown'),
                                    self.__player_configs.get('player_idle_animation'),
                                    self.__player_configs.get('idle_cols'),
                                    self.__player_configs.get('idle_rows'),
                                    self.__player_configs.get('player_walk_animation'),
                                    self.__player_configs.get('walk_cols'),
                                    self.__player_configs.get('walk_rows'),
                                    self.__player_configs.get('player_jump_animation'),
                                    self.__player_configs.get('jump_cols'),
                                    self.__player_configs.get('jump_rows'),
                                    self.__player_configs.get('player_attack_animation'),
                                    self.__player_configs.get('attack_cols'),
                                    self.__player_configs.get('attack_rows'),
                                    self.__player_configs.get('player_death_animation'),
                                    self.__player_configs.get('death_cols'),
                                    self.__player_configs.get('death_rows'))
        #configuraciones de stage
        self.__stage_configs = self.__configs.get('stage')
        #configuraciones de enemigos
        self.__enemy_configs = self.__configs.get('enemy')
        #configuraciones de frutas
        self.__object_configs = self.__configs.get('objetos')
        #configuraciones de vidas
        self.__lifes_configs = self.__configs.get('vidas')
        
        #creo grupo jugador y enemigos
        self.player = pygame.sprite.GroupSingle(self.__player_sprite)
        self.enemies = pygame.sprite.Group()
        self.objets = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.lifes = pygame.sprite.Group()
        
        self.create_enemies()
        
        #del json obtengo configuraciones del stage
        self.__stage_image = self.__stage_configs.get('stage_background')
        self.__background_image = pygame.image.load(self.__stage_image)
        self.__background_image = pygame.transform.scale(self.__background_image, (SCR_WIDTH, SCR_HEIGHT))
        self.__stage_music = self.__stage_configs.get('stage_music')
        self.__stage_win_sound = pygame.mixer.Sound(self.__stage_configs.get('stage_win'))
        #pantalla principal
        self.__main_screen = screen
        self.__tiempo_transcurrido = 0
        #score
        
        #game over
        self.game_over_sound = False
        #game win
        self.game_win_sound = False
        
        #plataformas
        self.__platform_configs = self.__configs.get('platforms')
        self.__lista_plataformas = []
        self.crear_plataformas()
        
        #spikes
        self.__spikes_configs = self.__configs.get('spikes')
        
        #objetos
        self.__pick_up_sound = pygame.mixer.Sound('assets/sounds/fruit_swallow.mp3') #MUDAR AL JSON
        self.create_objets()
        self.create_spikes()
        self.create_lifes()
        
    @property
    def stage_image(self):
        return self.__background_image
    @property
    def stage_music(self):
        return self.__stage_music
    @property
    def player_lifes(self):
        return self.player.sprite.life
    
    def stage_cleared(self):
        if not self.enemies and not self.objets:
            return True
        return False
    
    def game_over(self):
        return not self.player.sprite.is_alive()

    def get_player_score(self):
        return self.player.sprite.score
    
    def crear_plataformas(self):
        for p in self.__platform_configs:
            self.__lista_plataformas.append(Platform(p.get('x'),p.get('y'),p.get('width'),
                p.get('height'),self.__stage_configs.get('platform_floor')))
        
    def plataformas(self):
        for platform in self.__lista_plataformas:
            platform.draw(self.__main_screen)
            
    def enemigos(self):
        for enemy in self.enemies:
            enemy.draw(self.__main_screen)
    
    def create_spikes(self):
        for s in self.__spikes_configs:
            self.spikes.add(Trampas(s.get('x'), s.get('y')))
            
    def create_objets(self):
        for o in self.__object_configs.get('coords'):
            coord_x = o.get('x')
            coords_y = o.get('y')
            self.objets.add(Objetos(coord_x,coords_y,self.__object_configs.get('aspect_ratio'),
                                self.__object_configs.get('frame_rate'),
                                self.__object_configs.get('puntaje'),
                                self.__object_configs.get('apple_animation'),
                                self.__object_configs.get('animation_cols'),
                                self.__object_configs.get('animation_rows')))

    def create_lifes(self):
        self.lifes.add(Life(400,100,2,1)) #PASAR AL JSON
        
    def create_enemies(self):
        for _ in range(self.__stage_configs.get('max_enemies_amount')):
            walk_speed = random.randint(self.__enemy_configs.get('enemy_min_speed'),
                                self.__enemy_configs.get('enemy_max_speed'))
            coord_x = random.randint(50,750) #PASAR EL JSON (RANDOM COORDENADAS DE CAIDA)
            new_enemy = Enemy((coord_x,SPAWN_Y), SCR_WIDTH,GROUND, walk_speed,
                            self.__enemy_configs.get('gravity'),
                            self.__enemy_configs.get('aspect_ratio'),
                            self.__enemy_configs.get('shoot_percentage'),
                            self.__enemy_configs.get('frame_rate'),
                            self.__enemy_configs.get('puntaje'),
                            self.__enemy_configs.get('enemy_walk_animation'),
                            self.__enemy_configs.get('walk_cols'),
                            self.__enemy_configs.get('walk_rows'),
                            self.__enemy_configs.get('enemy_fall_animation'),
                            self.__enemy_configs.get('fall_cols'),
                            self.__enemy_configs.get('fall_rows'))
            self.enemies.add(new_enemy)
    
    def trampas(self):
        for spike in self.spikes:
            spike.draw(self.__main_screen)
    
    def objetos(self):
        for objeto in self.objets:
            objeto.draw(self.__main_screen)
    
    def vidas(self):
        for life in self.lifes:
            life.draw(self.__main_screen)
    
    def shoot_collisions(self):
        for fireball in self.player.sprite.fireball_group:
            hits = pygame.sprite.spritecollide(fireball, self.enemies, True)
            if hits:
                self.player.sprite.new_score += sum(enemy.score for enemy in hits)
                self.player.sprite.hit.play()
                self.player.sprite.remove_fireball(fireball)  
            if not self.enemies and not self.game_win_sound:
                self.__stage_win_sound.play()
                self.game_win_sound = True
                
        for enemy in self.enemies:
            for fireball in enemy.fireball_group:
                hits = pygame.sprite.spritecollide(fireball, self.player, False)
                if hits:
                    if self.player.sprite.lifes > 0:
                        self.player.sprite.hit.play()
                    self.player.sprite.restar_vida()
                    enemy.fireball_group.remove(fireball)
                    if self.player.sprite.lifes == 0 and not self.game_over_sound:
                        self.game_over_sound = True
                        self.player.sprite.death.play() 
                        
    def spikes_collitions(self):
        return pygame.sprite.spritecollide(self.player.sprite, self.spikes, False)
    
    def enemy_body_collitions(self):
        return pygame.sprite.spritecollide(self.player.sprite, self.enemies,False) 
    
    def objets_collitions(self):
        for objeto in pygame.sprite.spritecollide(self.player.sprite, self.objets, True):
            self.player.sprite.new_score += objeto.score
            self.__pick_up_sound.play()
    
    def lifes_collitions(self):
        if self.player.sprite.life > 2:
            pygame.sprite.spritecollide(self.player.sprite, self.lifes, False)
        else:
            for life in pygame.sprite.spritecollide(self.player.sprite, self.lifes, True):
                self.player.sprite.life_counter += life.life_restore
                self.player.sprite.life_up.play()
            
    
    def run(self, delta_ms, lista_eventos):
        self.__tiempo_transcurrido += delta_ms
        if self.__tiempo_transcurrido >= 17:
            self.plataformas()
            self.enemigos()
            self.objetos()
            self.objets_collitions()
            self.trampas()
            self.vidas()
            self.lifes_collitions()
            self.objets.update(self.__main_screen, delta_ms)
            self.enemies.update(self.__main_screen, delta_ms, self.__lista_plataformas)
            self.player.update(self.__main_screen, delta_ms, self.__lista_plataformas, lista_eventos,
                            self.spikes_collitions(), self.enemy_body_collitions())
            self.player.sprite.draw(self.__main_screen)
            self.shoot_collisions()
            #print(self.player.sprite.score)
        else:
            self.__tiempo_transcurrido = 0