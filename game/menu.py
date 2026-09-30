import pygame
import os

class Menu:

    def __init__(self, screen):
        # Guardamos la pantalla donde vamos a dibujar el menú
        self.screen = screen
        
        # Fuente principal del menú (tamaño 40)
        self.font = pygame.font.SysFont("Arial", 40)

        # Carpeta donde están los recursos (imágenes del menú)
        assets = os.path.join("game", "assets")

        # -------------------------------
        # CARGA DEL FONDO
        # -------------------------------
        # Cargamos la imagen del fondo del menú
        self.bg = pygame.image.load(os.path.join(assets, "menu fondo.png"))
        # La ajustamos al tamaño de la ventana (900x500)
        self.bg = pygame.transform.scale(self.bg, (900, 500))

        # -------------------------------
        # CARGA Y ESCALADO DE BOTÓN "JUGAR"
        # -------------------------------
        # Se carga la imagen del botón
        self.btn_play = pygame.image.load(os.path.join(assets, "jugar boton.png"))
        # Se ajusta su tamaño a 200x80 px
        self.btn_play = pygame.transform.scale(self.btn_play, (200, 80))

        # -------------------------------
        # CARGA Y ESCALADO DE BOTÓN "SALIR"
        # -------------------------------
        self.btn_exit = pygame.image.load(os.path.join(assets, "salir boton.png"))
        self.btn_exit = pygame.transform.scale(self.btn_exit, (200, 80))

        # -------------------------------
        # RECTÁNGULOS DE COLISIÓN (HITBOX)
        # -------------------------------
        # Creamos rectángulos centrados para detectar clics
        self.play_rect = self.btn_play.get_rect(center=(450, 260))  # Botón jugar
        self.exit_rect = self.btn_exit.get_rect(center=(450, 360))  # Botón salir

    # -----------------------------------------------------------------------
    # MÉTODO: handle_click(pos)
    # Este método recibe la posición del clic y determina qué botón se tocó.
    # -----------------------------------------------------------------------
    def handle_click(self, pos):
        # Si se hace clic sobre el botón de "Jugar"
        if self.play_rect.collidepoint(pos):
            # Retornamos la acción que debe ejecutarse (cambiar a pantalla de juego)
            return "game"

        # Si se hace clic sobre el botón de "Salir"
        if self.exit_rect.collidepoint(pos):
            # Retornar acción para cerrar la aplicación
            return "exit"

    # -----------------------------------------------------------------------
    # MÉTODO: draw()
    # Dibuja todo el menú en pantalla
    # -----------------------------------------------------------------------
    def draw(self):
        # Dibujar fondo del menú
        self.screen.blit(self.bg, (0, 0))

        # Dibujar botones "Jugar" y "Salir"
        self.screen.blit(self.btn_play, self.play_rect)
        self.screen.blit(self.btn_exit, self.exit_rect)

        # -------------------------------
        # TITULO DEL JUEGO
        # -------------------------------
        # Se crea el texto "TORRE DE HANOI" con una fuente más grande y negrita
        title = pygame.font.SysFont("Arial", 55, bold=True).render(
            "TORRE DE HANOI", 
            True, 
            (255, 255, 0)  # Color amarillo
        )

        # Centramos el título arriba de la pantalla
        rect = title.get_rect(center=(450, 100))

        # Dibujamos el título en pantalla
        self.screen.blit(title, rect)
