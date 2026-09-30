import pygame
from game.menu import Menu            # Importa la clase del menú principal
from game.hanoi_game import HanoiGame # Importa la clase del juego Torre de Hanoi

# -------------------------------------------------------------------
# INICIALIZACIÓN DE PYGAME Y VENTANA PRINCIPAL
# -------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((900, 500))   # Crea una ventana de 900x500
pygame.display.set_caption("Torre de Hanoi Retro")  # Título de la ventana

clock = pygame.time.Clock()  # Controlador de FPS
running = True               # Controla si el juego sigue activo

# -------------------------------------------------------------------
# ESTADO ACTUAL DE LA APLICACIÓN
# Puede ser:
#   "menu"  -> estás en el menú principal
#   "game"  -> estás dentro del juego
# -------------------------------------------------------------------
state = "menu"

# Crear instancias del menú y del juego
menu = Menu(screen)
game = HanoiGame(screen)

# -------------------------------------------------------------------
# MÚSICA DE FONDO DEL JUEGO
# Se intenta cargar un archivo MP3 desde assets
# Si falla, simplemente imprime el error pero no detiene el juego
# -------------------------------------------------------------------
try:
    pygame.mixer.music.load("game/assets/juego sonido.mp3")
    pygame.mixer.music.play(-1)          # -1 significa "se repite infinito"
    pygame.mixer.music.set_volume(0.45)  # Volumen de música
except Exception as e:
    print("Error cargando música:", e)

# -------------------------------------------------------------------
# BUCLE PRINCIPAL DEL JUEGO
# Aquí se procesan:
#  - eventos (clics, teclado, cerrar ventana)
#  - lógica de menú o juego
#  - dibujado de pantalla
# -------------------------------------------------------------------
while running:

    # --- PROCESAMIENTO DE EVENTOS ---
    for event in pygame.event.get():

        # Si el usuario cierra la ventana
        if event.type == pygame.QUIT:
            running = False

        # =============================================================
        #                      ESTADO: MENU
        # =============================================================
        if state == "menu":

            # Se detectan clics de mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                # El menú devuelve "game", "exit" o None
                option = menu.handle_click(event.pos)

                if option == "game":
                    # Cambiar a pantalla de juego
                    state = "game"

                elif option == "exit":
                    # Cerrar juego
                    running = False

        # =============================================================
        #                      ESTADO: JUEGO
        # =============================================================
        elif state == "game":

            # -------------------------
            # CUANDO PRESIONAS EL MOUSE
            # -------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:

                # --- SI EL NIVEL FUE COMPLETADO ---
                if game.level_complete:

                    # Botón "Siguiente Nivel"
                    if game.next_btn.collidepoint(event.pos):
                        game.next_level()
                        continue  # Evita que toque discos durante transición

                    # Botón "Salir al menú" desde pantalla de victoria
                    if game.victory_exit_btn.collidepoint(event.pos):
                        state = "menu"           # Volver al menú
                        game.level_complete = False  # Reset bandera
                        continue

                # --- BOTÓN DE REINICIAR NIVEL ---
                if game.reset_rect.collidepoint(event.pos):
                    game.reset_level()
                    continue  # Importantísimo para evitar agarrar un disco accidentalmente

                # --- ACTIVAR/DESACTIVAR SONIDO ---
                if game.sound_rect.collidepoint(event.pos):
                    game.music_on = not game.music_on

                    if game.music_on:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()
                    continue

                # --- BOTÓN DE PAUSA ---
                if game.pause_rect.collidepoint(event.pos):
                    game.toggle_pause()
                    continue

                # --- REANUDAR DESDE PAUSA ---
                if game.paused and game.resume_rect.collidepoint(event.pos):
                    game.toggle_pause()
                    continue

                # --- SALIR AL MENÚ DESDE PAUSA ---
                if game.paused and game.exit_rect.collidepoint(event.pos):
                    state = "menu"
                    continue

                # --- ARRASTRAR DISCO (solo si no está en pausa ni en victoria) ---
                if not game.paused and not game.level_complete:
                    game.handle_mouse_down(event.pos)

            # -------------------------
            # CUANDO SUELTAS EL MOUSE
            # -------------------------
            if event.type == pygame.MOUSEBUTTONUP:
                # Soltar disco si se estaba arrastrando
                if not game.paused and not game.level_complete:
                    game.handle_mouse_up(event.pos)

    # --------------------------------------------------------
    # DIBUJO DE PANTALLA (SE EJECUTA CADA FRAME)
    # --------------------------------------------------------
    screen.fill((0, 0, 0))  # Limpia pantalla

    # Mostrar menú o juego según estado actual
    if state == "menu":
        menu.draw()

    elif state == "game":
        game.draw()

    # Actualizar ventana
    pygame.display.flip()

    # Limitar a 60 FPS
    clock.tick(60)

# Cuando se sale del bucle, cerrar pygame
pygame.quit()
