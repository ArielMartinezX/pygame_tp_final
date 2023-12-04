import pygame, sys
from models.stage import Stage
from auxiliar.constantes import * 
from UI.GUI_form_pause import FormPause

from db_score.db import *

class Game:
    
    def __init__(self) -> None:
        self.__stage_duration = open_configs().get("stage_duration")
        self.__timer = self.__stage_duration
        self.__waiting_time = 7
        self.__is_current_level_ended = False
        
        self.__game_win = False
        self.__score = 0
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsans", 30)
        self.__music_loaded = False
        
        self.__current_stage = None
        self.__stage = None
        
        self.__stage_1_passed = False
        self.__stage_2_passed = False
        self.__stage_3_passed = False
        
        self.__score_to_show = 0
        self.__running = True
        self.__pause = False
        #--------------------------------------------------------
        self.__player_name_previo = None
        self.__player_name = None    
        #--------------------------------------------------------
    @property
    def stage_1_passed(self):
        return self.__stage_1_passed
    
    @property
    def stage_2_passed(self):
        return self.__stage_2_passed
    
    @property
    def stage_3_passed(self):
        return self.__stage_3_passed
    
    def restart_main_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./UI/Recursos/main_music.mp3")
        pygame.mixer.music.play(-1)

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    
    def init_stage(self, screen, stage_name:str):
        self.__stage = Stage(screen, SCR_HEIGHT, SCR_WIDTH, stage_name)
        self.__current_stage = stage_name
        
        
    def reset_level_values(self):
        self.__is_current_level_ended = False
        self.__waiting_time = 7
        self.__timer = self.__stage_duration
        
    def reset_levels_and_score(self):
        self.__score_to_show = 0
        self.__score = 0
        self.__game_win = False
        self.__stage_1_passed = False
        self.__stage_2_passed = False
        self.__stage_3_passed = False        
    
    def pause(self,screen):
        self.__pause = True
        form_pause = FormPause(screen,100,100,600,400,(20, 20, 20),(10, 10, 10),
                    True)
        while self.__pause:
            lista_eventos = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__pause = False
                    self.__running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.__pause = False
                lista_eventos.append(event)
            screen.fill((0,0,0))
            form_pause.update(lista_eventos)
            pygame.display.update()
            
    
    def run_game(self, stage, player_name):
        pygame.init()
        screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        title = pygame.display.set_caption("OWLET MONSTER")
        
        self.__stage = None
        self.__player_name = player_name
        
        if not self.__player_name_previo:
            self.__player_name_previo = self.__player_name
            
        if self.__player_name != self.__player_name_previo:
            insertar_campos(self.__player_name_previo, self.__score)
            self.reset_levels_and_score()
            
        while self.__running:
            lista_eventos = []
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.__timer -= 1
                    if self.__is_current_level_ended:
                        self.__waiting_time -=1
                        print(f"Tiempo de espera {self.__waiting_time}")
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.pause(screen)

                lista_eventos.append(event)
            
            if not self.__stage:
                self.__stage = Stage(screen, SCR_HEIGHT, SCR_WIDTH, stage)
                self.__current_stage = stage
                
            if not self.__game_win:  
                if not self.__music_loaded:
                    pygame.mixer.music.load(self.__stage.stage_music)
                    # pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    self.__music_loaded = True
                self.__score_to_show = self.__score + self.__stage.get_player_score()     
                match self.__current_stage:
                    case "stage_1":
                        if self.__stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += self.__stage.get_player_score()
                                self.init_stage(screen,"stage_2")
                                self.reset_level_values()
                                self.__music_loaded = False
                                self.__stage_1_passed = True
                        elif self.__stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.init_stage(screen,"stage_1")
                                self.reset_level_values()
                    case "stage_2":
                        if self.__stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += self.__stage.get_player_score()
                                self.init_stage(screen,"stage_3")
                                self.__music_loaded = False
                                self.reset_level_values()
                                self.__stage_2_passed = True
                        elif self.__stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.init_stage(screen,"stage_2") 
                                self.reset_level_values()
                    case "stage_3":
                        if self.__stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += self.__stage.get_player_score()
                                self.__game_win = True 
                                self.__music_loaded = False
                                self.__stage_3_passed = True
                                self.reset_level_values()
                                insertar_campos(player_name, self.__score)
                                self.restart_main_music()
                                return True
                        elif self.__stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.init_stage(screen,"stage_3") 
                                self.reset_level_values()
            else:
                self.__score = 0
                self.__score_to_show = 0
                self.__game_win = False

            if self.__stage.return_to_menu:
                return True
            
            screen.blit(self.__stage.stage_image,(0,0))
            score_text = self.font.render(f"SCORE: {self.__score_to_show}", True, (255, 255, 255)) 
            time_text = self.font.render(f"TIME: {self.format_time(self.__timer)}",True, (255, 255, 255))
            life_text = self.font.render(f"LIFES: {self.__stage.player_lifes}",True, (255, 255, 255)) 
            screen.blit(score_text, (80,20))
            screen.blit(time_text, (500,20))
            screen.blit(life_text, (300,20))
            delta_ms = clock.tick(FPS)
            self.__stage.run(delta_ms, lista_eventos)
            
            pygame.display.update()
