import pygame, sys
from models.stage import Stage
from auxiliar.constantes import * 


class Game:
    
    def __init__(self) -> None:
        self.__timer = 10
    
    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    
    def run_stage(self, stage_name:str):
        pygame.init()
        
        screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        title = pygame.display.set_caption("PROTOTIPO")
        game = Stage(screen, SCR_HEIGHT, SCR_WIDTH, stage_name)
        back = game.stage_image
        # back = game._Stage__stage_image
        background_music = game.stage_music
        background = pygame.image.load(back)
        background = pygame.transform.scale(background, (SCR_WIDTH, SCR_HEIGHT))
        # Reproducir la música en bucle (loop)
        pygame.mixer.music.set_volume(0.05)
        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1)
        
        while True:
            lista_eventos = []
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    self.__timer -= 1
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                lista_eventos.append(event)
            # pygame.mixer.music.set_volume(0.05)
            # print("Current volume:", pygame.mixer.music.get_volume())

            if game.stage_cleared():
                print("ganaste")
            
            
            screen.blit(background,(0,0))
            delta_ms = clock.tick(FPS)
            game.run(delta_ms, lista_eventos)
            
            pygame.display.update()
            if self.__timer < 0:
                print("Perdiste boludoooooooo")
                # reiniciar si paso de nivel
            else:
                print(f"Timer: {self.format_time(self.__timer)}")