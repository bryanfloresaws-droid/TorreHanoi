import pygame
import os
import math

# =====================================================================================
#                              CLASE PRINCIPAL DEL JUEGO
# =====================================================================================

class HanoiGame:
    def __init__(self, screen):
        # Pantalla donde se dibuja todo el juego
        self.screen = screen
        
        # Carpeta donde se encuentran los recursos del juego (imágenes)
        self.assets = os.path.join("game", "assets")

        # -------------------------------------------------------------------------
        #                               FONDO DEL JUEGO
        # -------------------------------------------------------------------------
        self.bg = pygame.image.load(os.path.join(self.assets, "juego fondo.png"))
        # Se escala el fondo al tamaño exacto de la ventana
        self.bg = pygame.transform.scale(self.bg, (900, 500))

        # -------------------------------------------------------------------------
        #                       BASE Y POSTES DE LAS TORRES
        # -------------------------------------------------------------------------
        self.base = pygame.image.load(os.path.join(self.assets, "base.png"))
        self.base = pygame.transform.scale(self.base, (200, 50))

        self.tower = pygame.image.load(os.path.join(self.assets, "torre.png"))
        self.tower = pygame.transform.scale(self.tower, (25, 180))

        # -------------------------------------------------------------------------
        #                               SISTEMA DE NIVELES
        # -------------------------------------------------------------------------
        self.level = 1             # Nivel inicial del jugador
        self.max_level = 7         # Último nivel disponible
        self.load_level_discs()    # Cargar discos según el nivel

        # Cada poste contiene:
        #   - su coordenada X
        #   - una pila con índices de discos (0 = disco más grande)
        self.posts = [
            {"x": 200, "stack": list(range(self.n_discs))},  # Torre A (inicio)
            {"x": 450, "stack": []},                        # Torre B
            {"x": 700, "stack": []},                        # Torre C
        ]

        # -------------------------------------------------------------------------
        #                           SISTEMA DE ARRASTRAR DISCOS
        # -------------------------------------------------------------------------
        self.dragging = False      # Indica si un disco está siendo arrastrado
        self.drag_disc = None      # Índice del disco arrastrado
        self.offset_x = 0          # Diferencia entre clic y posición del disco
        self.offset_y = 0
        self.original_post = None  # Torre desde donde se tomó el disco

        # -------------------------------------------------------------------------
        #                             ESTADÍSTICAS DEL JUEGO
        # -------------------------------------------------------------------------
        self.moves = 0             # Número de movimientos realizados
        self.time_start = pygame.time.get_ticks()  # Tiempo al iniciar nivel
        self.score = 0             # Puntaje actual (acumula durante el nivel)
        self.total_score = 0       # Puntaje acumulado de niveles pasados

        # -------------------------------------------------------------------------
        #                                PAUSA
        # -------------------------------------------------------------------------
        self.paused = False
        self.music_on = True

        # -------------------------------------------------------------------------
        #                   BOTONES SUPERIORES UNIFORMES DEL HUD
        # -------------------------------------------------------------------------
        BUTTON_WIDTH = 120   # Bastante ancho para que quepa el texto
        BUTTON_HEIGHT = 50   # Altura cómoda
        BUTTON_SPACING = 20  # Espacio entre botones
        BUTTON_Y = 15
        
        # --- 1. Botón de Reinicio ---
        self.reset_btn = pygame.image.load(os.path.join(self.assets, "reiniciar boton.png"))
        self.reset_btn = pygame.transform.scale(self.reset_btn, (BUTTON_WIDTH, BUTTON_HEIGHT))
        self.reset_rect = self.reset_btn.get_rect(topleft=(20, BUTTON_Y))

        # --- 2. Botones de Sonido (ON / OFF) ---
        self.sound_on_btn = pygame.image.load(os.path.join(self.assets, "musica on boton.png"))
        # CORRECCIÓN 1: Usar (WIDTH, HEIGHT) para redimensionar
        self.sound_on_btn = pygame.transform.scale(self.sound_on_btn, (BUTTON_WIDTH, BUTTON_HEIGHT)) 

        self.sound_off_btn = pygame.image.load(os.path.join(self.assets, "musica off boton.png"))
        # CORRECCIÓN 2: Usar (WIDTH, HEIGHT) para redimensionar
        self.sound_off_btn = pygame.transform.scale(self.sound_off_btn, (BUTTON_WIDTH, BUTTON_HEIGHT)) 

        # CORRECCIÓN 3: Usar (WIDTH, HEIGHT) y basar la posición X en WIDTH
        self.sound_rect = pygame.Rect(20 + BUTTON_WIDTH + BUTTON_SPACING, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # --- 3. Botón de Pausa ---
        self.pause_btn = pygame.image.load(os.path.join(self.assets, "pausa boton.png"))
        # CORRECCIÓN 4: Usar (WIDTH, HEIGHT) para redimensionar
        self.pause_btn = pygame.transform.scale(self.pause_btn, (BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # CORRECCIÓN 5: Basar la posición X en WIDTH para el cálculo del desplazamiento
        self.pause_rect = self.pause_btn.get_rect(topleft=(20 + (BUTTON_WIDTH + BUTTON_SPACING) * 2, BUTTON_Y))

        # -------------------------------------------------------------------------
        #                  BOTONES DEL MENÚ DE PAUSA Y VICTORIA
        # -------------------------------------------------------------------------
        self.resume_btn = pygame.image.load(os.path.join(self.assets, "reanudar boton.png"))
        self.resume_btn = pygame.transform.scale(self.resume_btn, (150, 60))
        self.resume_rect = self.resume_btn.get_rect(center=(450, 300))

        self.exit_btn = pygame.image.load(os.path.join(self.assets, "salir boton.png"))
        self.exit_btn = pygame.transform.scale(self.exit_btn, (150, 60))
        self.exit_rect = self.exit_btn.get_rect(center=(450, 380))

        # -------------------------------------------------------------------------
        #                     VARIABLES DEL NIVEL COMPLETADO
        # -------------------------------------------------------------------------
        self.level_complete = False
        self.level_score = 0
        self.completed_time = 0
        self.completed_min_moves = 0
        self.fade_alpha = 0

        # Botones de la pantalla final
        self.next_btn = pygame.Rect(325, 380, 250, 60)
        self.victory_exit_btn = pygame.Rect(325, 450, 250, 60)

    # =====================================================================================
    #                               FUNCIONES DE UTILIDAD
    # =====================================================================================

    def draw_star(self, x, y, size, color):
        """
        Dibuja una estrella de 5 puntas usando un cálculo matemático.
        Se generan 10 puntos alternando radios para formar la estrella.
        """
        points = []
        for i in range(10):
            angle = math.pi / 2 + (2 * math.pi * i / 10)
            radius = size if i % 2 == 0 else size * 0.4
            px = x + radius * math.cos(angle)
            py = y - radius * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(self.screen, color, points)

    # -------------------------------------------------------------------------
    #                         CARGAR DISCOS SEGÚN EL NIVEL
    # -------------------------------------------------------------------------
    def load_level_discs(self):
        # Cada nivel añade 1 disco más → dificultad creciente
        self.n_discs = self.level + 2
        self.discs = []

        # Se cargan imágenes de disco 1,2,3... y se escalan
        for i in range(1, self.n_discs + 1):
            img = pygame.image.load(os.path.join(self.assets, f"disco {i} hanoi.png"))
            img = pygame.transform.scale(img, (80 + i * 20, 22))
            self.discs.append(img)

    # -------------------------------------------------------------------------
    #                 OBTENER DISCO SUPERIOR DE UN POSTE
    # -------------------------------------------------------------------------
    def get_top_disc_at(self, x, y):
        """
        Dado un clic (x,y), revisa si está sobre la parte útil del poste.
        Si hay discos disponibles, devuelve el índice del disco superior.
        """
        for i, post in enumerate(self.posts):
            # 80px de margen para considerar la zona del poste
            if abs(x - post["x"]) < 80:
                if len(post["stack"]) > 0:
                    return post["stack"][0], i
        return None, None

    # -------------------------------------------------------------------------
    #                                 PAUSA
    # -------------------------------------------------------------------------
    def toggle_pause(self):
        if not self.paused:
            self.paused = True
            self.pause_start = pygame.time.get_ticks()
        else:
            self.paused = False
            # Ajusta el tiempo total restando el tiempo en pausa
            pause_duration = pygame.time.get_ticks() - self.pause_start
            self.time_start += pause_duration

    # -------------------------------------------------------------------------
    #                           REINICIAR NIVEL
    # -------------------------------------------------------------------------
    def reset_level(self):
        # Reestablece todas las torres
        self.posts = [
            {"x": 200, "stack": list(range(self.n_discs))},
            {"x": 450, "stack": []},
            {"x": 700, "stack": []},
        ]
        self.moves = 0
        self.score = 0
        self.time_start = pygame.time.get_ticks()
        self.level_complete = False

    # -------------------------------------------------------------------------
    #                           SIGUIENTE NIVEL
    # -------------------------------------------------------------------------
    def next_level(self):
        if self.level < self.max_level:
            # Acumula el puntaje ganado
            self.total_score += self.level_score

            self.level += 1
            self.load_level_discs()

            # Reiniciar posiciones y estadísticas
            self.posts = [
                {"x": 200, "stack": list(range(self.n_discs))},
                {"x": 450, "stack": []},
                {"x": 700, "stack": []},
            ]
            self.moves = 0
            self.score = 0
            self.time_start = pygame.time.get_ticks()
            self.level_complete = False
            self.fade_alpha = 0

    # -------------------------------------------------------------------------
    #         VERIFICAR SI EL NIVEL FUE COMPLETADO (TORRE C COMPLETA)
    # -------------------------------------------------------------------------
    def check_victory(self):
        return len(self.posts[2]["stack"]) == self.n_discs

    # -------------------------------------------------------------------------
    #                   PUNTAJE TEMPORAL MIENTRAS JUEGA
    # -------------------------------------------------------------------------
    def calculate_current_score(self):
        """
        Calcula puntos por discos ya en la torre final.
        Cada disco vale 100 puntos multiplicados por el nivel.
        """
        discs_in_final = len(self.posts[2]["stack"])
        points_per_disc = 100 * self.level
        return discs_in_final * points_per_disc

    # -------------------------------------------------------------------------
    #                   PUNTAJE FINAL AL TERMINAR EL NIVEL
    # -------------------------------------------------------------------------
    def calculate_final_score(self):
        """
        Calcula:
        - puntaje base
        - bonus por eficiencia (comparado con movimientos mínimos)
        - bonus por tiempo
        """
        min_moves = (2 ** self.n_discs) - 1
        time_elapsed = (pygame.time.get_ticks() - self.time_start) // 1000

        base_points = 1000 * self.level

        # Ratio de eficiencia (1.0 = perfecto)
        efficiency_ratio = min_moves / max(1, self.moves)
        efficiency_bonus = int(500 * efficiency_ratio)

        # Bonus por velocidad (más puntos si se hace rápido)
        time_bonus = max(0, 300 - (time_elapsed - 30) * 5) if time_elapsed > 30 else 300

        total = base_points + efficiency_bonus + time_bonus
        return total, min_moves, time_elapsed

    # -------------------------------------------------------------------------
    #                          CÁLCULO DE ESTRELLAS
    # -------------------------------------------------------------------------
    def calculate_stars(self):
        """
        Devuelve estrellas de 1 a 5 según cuán cerca estuvo de los
        movimientos óptimos.
        """
        min_moves = (2 ** self.n_discs) - 1
        ratio = min_moves / max(1, self.moves)

        if ratio >= 1.0: return 5
        if ratio >= 0.85: return 4
        if ratio >= 0.70: return 3
        if ratio >= 0.50: return 2
        return 1

    # =====================================================================================
    #                              CONTROL DE MOUSE
    # =====================================================================================

    def handle_mouse_down(self, pos):
        """Se ejecuta cuando se presiona el mouse."""
        if self.paused or self.level_complete:
            return

        x, y = pos

        # Revisa si el clic fue sobre el disco superior de un poste
        disc_index, post_index = self.get_top_disc_at(x, y)
        if disc_index is None:
            return

        # Empieza el arrastre
        self.dragging = True
        self.drag_disc = disc_index
        self.original_post = post_index

        disc_img = self.discs[disc_index]

        BASE_Y = 400
        DISC_H = 22
        DISC_SPACING = 26

        # Calcula posición exacta del disco antes de moverlo
        start_y = BASE_Y - DISC_H - ((len(self.posts[post_index]["stack"]) - 1) * DISC_SPACING)
        start_x = self.posts[post_index]["x"] - disc_img.get_width() // 2

        # Guarda offset para que el disco no salte al cursor
        self.offset_x = x - start_x
        self.offset_y = y - start_y

        # Quita el disco del poste
        self.posts[post_index]["stack"].pop(0)

    def handle_mouse_up(self, pos):
        """Se ejecuta cuando se suelta el mouse."""
        if not self.dragging or self.paused or self.level_complete:
            return

        self.dragging = False
        x, y = pos
        target = None

        # Detecta si se soltó sobre un poste
        for i, post in enumerate(self.posts):
            if abs(x - post["x"]) < 80:
                target = i

        # Si no se soltó sobre ningún poste → regresar al original
        if target is None:
            self.posts[self.original_post]["stack"].insert(0, self.drag_disc)
            self.drag_disc = None
            return

        # Verificar reglas del juego: no disco grande sobre pequeño
        if len(self.posts[target]["stack"]) > 0:
            if self.drag_disc > self.posts[target]["stack"][0]:
                self.posts[self.original_post]["stack"].insert(0, self.drag_disc)
                self.drag_disc = None
                return

        # Movimiento válido → colocar disco
        self.posts[target]["stack"].insert(0, self.drag_disc)
        self.moves += 1
        self.drag_disc = None

    # =====================================================================================
    #                                   HUD DEL JUEGO
    # =====================================================================================

    def draw_hud(self):
        """
        Dibuja información del jugador:
        - Puntaje actual
        - Puntaje total
        - Movimientos
        - Tiempo
        - Nivel
        - Movimientos óptimos
        """

        self.score = self.calculate_current_score()

        # Panel semitransparente del HUD
        hud = pygame.Surface((200, 180))
        hud.set_alpha(140)
        hud.fill((10, 10, 30))
        self.screen.blit(hud, (685, 15))

        pygame.draw.rect(self.screen, (0, 180, 255), (685, 15, 200, 180), 3)

        font = pygame.font.SysFont("Arial", 19, bold=True)

        score_text = font.render(f"Puntos: {self.score}", True, (255, 255, 100))
        total_text = font.render(f"Total: {self.total_score}", True, (150, 255, 150))
        moves = font.render(f"Movimientos: {self.moves}", True, (255, 255, 255))
        time = font.render(f"Tiempo: {(pygame.time.get_ticks() - self.time_start) // 1000}s", True, (255, 255, 255))
        lvl = font.render(f"Nivel: {self.level}", True, (100, 255, 255))

        min_moves = (2 ** self.n_discs) - 1
        optimal = font.render(f"Óptimo: {min_moves}", True, (255, 150, 150))

        y = 28
        for item in (score_text, total_text, moves, optimal, time, lvl):
            self.screen.blit(item, (695, y))
            y += 26

    # =====================================================================================
    #                           PANTALLA DE NIVEL COMPLETADO
    # =====================================================================================

    def draw_level_complete(self):
        """Dibuja pantalla de victoria con estrellas y estadísticas."""

        # Fondo oscuro
        overlay = pygame.Surface((900, 500))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        self.screen.blit(overlay, (0, 0))

        # Título principal
        title_font = pygame.font.SysFont("Arial", 55, bold=True)
        title = title_font.render("¡NIVEL COMPLETADO!", True, (0, 200, 255))
        title_rect = title.get_rect(center=(450, 60))
        self.screen.blit(title, title_rect)

        # --------------------- DIBUJAR ESTRELLAS ---------------------
        stars = self.calculate_stars()
        star_y = 130
        star_spacing = 65
        total_width = 5 * star_spacing
        star_x_start = (900 - total_width) // 2 + 32

        for i in range(5):
            x = star_x_start + i * star_spacing
            if i < stars:
                # Estrella brillante
                self.draw_star(x, star_y, 18, (255, 215, 0))
                self.draw_star(x, star_y, 15, (255, 255, 100))
            else:
                # Estrella gris (no obtenida)
                self.draw_star(x, star_y, 18, (80, 80, 80))

        # --------------------- INFORMACIÓN DEL NIVEL ---------------------
        font = pygame.font.SysFont("Arial", 26)
        info_y = 190
        line_spacing = 35

        puntaje = font.render(f"Puntaje: +{self.level_score}", True, (255, 255, 150))
        self.screen.blit(puntaje, puntaje.get_rect(center=(450, info_y)))

        total = font.render(f"Total Acumulado: {self.total_score + self.level_score}", True, (150, 255, 150))
        self.screen.blit(total, total.get_rect(center=(450, info_y + line_spacing)))

        movimientos = font.render(f"Movimientos: {self.moves} / {self.completed_min_moves}", True, (255, 255, 255))
        self.screen.blit(movimientos, movimientos.get_rect(center=(450, info_y + line_spacing * 2)))

        tiempo = font.render(f"Tiempo: {self.completed_time}s", True, (255, 255, 255))
        self.screen.blit(tiempo, tiempo.get_rect(center=(450, info_y + line_spacing * 3)))

        # --------------------- BOTÓN SIGUIENTE NIVEL ---------------------
        button_font = pygame.font.SysFont("Arial", 24, bold=True)

        pygame.draw.rect(self.screen, (0, 200, 255), self.next_btn, border_radius=10)
        pygame.draw.rect(self.screen, (100, 220, 255), self.next_btn, 3, border_radius=10)

        siguiente_text = button_font.render("SIGUIENTE NIVEL", True, (255, 255, 255))
        self.screen.blit(siguiente_text, siguiente_text.get_rect(center=self.next_btn.center))

        # --------------------- BOTÓN VOLVER AL MENÚ ---------------------
        pygame.draw.rect(self.screen, (255, 60, 60), self.victory_exit_btn, border_radius=10)
        pygame.draw.rect(self.screen, (255, 120, 120), self.victory_exit_btn, 3, border_radius=10)

        menu_text = button_font.render("VOLVER AL MENÚ", True, (255, 255, 255))
        self.screen.blit(menu_text, menu_text.get_rect(center=self.victory_exit_btn.center))

    # =====================================================================================
    #                               FUNCIÓN PRINCIPAL DRAW()
    # =====================================================================================

    def draw(self):
        """Dibuja absolutamente todo el juego en pantalla"""

        # ---------------------------- FONDO ----------------------------
        self.screen.blit(self.bg, (0, 0))

        BASE_Y = 400
        DISC_H = 22
        DISC_SPACING = 26

        # ---------------------- BASES Y TORRES -------------------------
        for post in self.posts:

            # Dibuja la base de madera
            bx = post["x"] - self.base.get_width() // 2
            self.screen.blit(self.base, (bx, BASE_Y))

            # Dibuja la torre vertical
            tx = post["x"] - self.tower.get_width() // 2
            ty = BASE_Y - self.tower.get_height() + 5
            self.screen.blit(self.tower, (tx, ty))

        # ---------------------- DISCOS FIJOS ---------------------------
        for post in self.posts:
            for level, disc_index in enumerate(reversed(post["stack"])):

                disc = self.discs[disc_index]
                x = post["x"] - disc.get_width() // 2
                y = BASE_Y - DISC_H - (level * DISC_SPACING)

                self.screen.blit(disc, (x, y))

        # ----------------------- DISCO ARRASTRADO ----------------------
        if self.dragging and self.drag_disc is not None:
            mx, my = pygame.mouse.get_pos()
            disc = self.discs[self.drag_disc]
            # El disco sigue al mouse con su offset original
            self.screen.blit(disc, (mx - self.offset_x, my - self.offset_y))

        # ---------------------------- HUD ------------------------------
        if not self.level_complete:
            self.draw_hud()

        # ------------------------- BOTONES -----------------------------
        self.screen.blit(self.reset_btn, self.reset_rect)
        self.screen.blit(self.sound_on_btn if self.music_on else self.sound_off_btn, self.sound_rect)
        self.screen.blit(self.pause_btn, self.pause_rect)

        # -------------------------- PAUSA ------------------------------
        if self.paused:
            overlay = pygame.Surface((900, 500))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(180)
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.SysFont("Arial", 50)
            text = font.render("PAUSA", True, (255, 255, 255))
            self.screen.blit(text, (360, 150))

            # Botones de pausa
            self.screen.blit(self.resume_btn, self.resume_rect)
            self.screen.blit(self.exit_btn, self.exit_rect)

        # --------------------- NIVEL COMPLETADO ------------------------
        if self.check_victory() and not self.level_complete:
            # Calcula score del nivel UNA SOLA VEZ
            self.level_score, self.completed_min_moves, self.completed_time = self.calculate_final_score()
            self.level_complete = True

        if self.level_complete:
            self.draw_level_complete()
