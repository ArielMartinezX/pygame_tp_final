import pygame, sys
from models.stage import Stage
from auxiliar.constantes import * 


class Game:
    
    def __init__(self) -> None:
        self.__stage_duration = open_configs().get("stage_duration")
        self.__timer = self.__stage_duration
        self.__waiting_time = 7
        self.__is_current_level_ended = False
        
        #para nivel 3, no buclea el 3er nivel si gane.
        self.__game_win = False
        self.__score = 0
        pygame.font.init()
        self.font = pygame.font.SysFont("comicsans", 30)
        self.__music_loaded = False
        
        self.__stage_list = ["stage_1", "stage_2", "stage_3"]
        self.__current_stage = None
        self.__next_stage = None

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    
    def init_stage(self, screen, stage_name:str):
        stage = Stage(screen, SCR_HEIGHT, SCR_WIDTH, stage_name)
        self.__current_stage = stage_name
        self.__timer = self.__stage_duration
        return stage
    
    
    def run_game(self):
        pygame.init()
        screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        title = pygame.display.set_caption("PROTOTIPO")
        stage = None
        
        while True:
            lista_eventos = []
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.__timer -= 1
                    if self.__is_current_level_ended:
                        self.__waiting_time -=1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                lista_eventos.append(event)
            
            if not stage and not self.__current_stage:
                stage = Stage(screen, SCR_HEIGHT, SCR_WIDTH, "stage_1")
                self.__current_stage = "stage_1"
                

            if not self.__game_win:  
                if not self.__music_loaded:
                    pygame.mixer.music.load(stage.stage_music)
                    pygame.mixer.music.set_volume(0.2)
                    pygame.mixer.music.play(-1)
                    self.__music_loaded = True
                puntaje = self.__score + stage.get_player_score()      
                match self.__current_stage:
                    case "stage_1":
                        if stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += stage.get_player_score()
                                stage = self.init_stage(screen,"stage_2")
                                self.__music_loaded = False
                                self.__waiting_time = 7
                        elif stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                stage = self.init_stage(screen,"stage_1") 
                                self.__waiting_time = 7
                    case "stage_2":
                        if stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += stage.get_player_score()
                                stage = self.init_stage(screen,"stage_3")
                                self.__music_loaded = False
                                self.__waiting_time = 7
                        elif stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                stage = self.init_stage(screen,"stage_2") 
                                self.__waiting_time = 7
                    case "stage_3":
                        if stage.stage_cleared() and self.__timer > 0 :
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                self.__score += stage.get_player_score()
                                self.__game_win = True 
                                self.__music_loaded = False
                                self.__waiting_time = 7
                        elif stage.game_over() or self.__timer <= 0:
                            self.__is_current_level_ended = True
                            if  self.__waiting_time <= 0:
                                stage = self.init_stage(screen,"stage_3") 
                                self.__waiting_time = 7

            screen.blit(stage.stage_image,(0,0))
            score_text = self.font.render(f"SCORE: {puntaje}", True, (255, 255, 255))
            time_text = self.font.render(f"TIME: {self.format_time(self.__timer)}",True, (255, 255, 255))
            life_text = self.font.render(f"LIFES: {stage.player_lifes}",True, (255, 255, 255))
            screen.blit(score_text, (80, 50))
            screen.blit(time_text, (500,50))
            screen.blit(life_text, (300,50))
            delta_ms = clock.tick(FPS)
            stage.run(delta_ms, lista_eventos)
            
            pygame.display.update()
