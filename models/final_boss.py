# from models.enemy import *

# class FinalBoss(Enemy):
#     def __init__(self, pos, constraint_w, constraint_h, walk_speed, gravity, aspect_ratio, fire_percentage, frame_rate, puntaje,
#                  walk_path, walk_cols, walk_rows, fall_path, fall_cols, fall_rows, special_attack_power):
#         # Llama al constructor de la clase padre (Enemy)
#         super().__init__(pos, constraint_w, constraint_h, walk_speed, gravity, aspect_ratio, fire_percentage, frame_rate, puntaje,
#                          walk_path, walk_cols, walk_rows, fall_path, fall_cols, fall_rows)
        
#         # Nuevas propiedades específicas del jefe final
#         self.__special_attack_power = special_attack_power
#         self.__special_attack_cooldown = 5000  # Tiempo en milisegundos entre ataques especiales
#         self.__original_player_position = pos

#     def special_attack(self):
#         current_time = pygame.time.get_ticks()

#         if current_time - self.__special_attack_cooldown >= self.__special_attack_cooldown:
#             # Reinicia el contador de cooldown
#             self.__special_attack_cooldown = current_time

#             # Lanza un relámpago a la posición original del jugador
#             self.launch_lightning(self.__original_player_position)

#     def launch_lightning(self, target_position):
#         # Logica para lanzar un relámpago a la posición del player
#         # crear instancias de relámpagos o realizar otras acciones necesarias
#         pass

#     def update(self, screen: pygame.surface.Surface, delta_ms, lista_plataformas):
#         # Agregar comportamientos específicos del jefe final en la actualización
#         super().update(screen, delta_ms, lista_plataformas)
        
#         # Lógica adicional específica del jefe final
#         self.special_attack()