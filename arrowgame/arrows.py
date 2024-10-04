import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Flechas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imágenes de flechas
arrow_up = pygame.image.load('arrow_up.png').convert_alpha()
arrow_down = pygame.image.load('arrow_down.png').convert_alpha()
arrow_left = pygame.image.load('arrow_left.png').convert_alpha()
arrow_right = pygame.image.load('arrow_right.png').convert_alpha()

# Escalar imágenes
arrow_size = (50, 50)
arrow_up = pygame.transform.scale(arrow_up, arrow_size)
arrow_down = pygame.transform.scale(arrow_down, arrow_size)
arrow_left = pygame.transform.scale(arrow_left, arrow_size)
arrow_right = pygame.transform.scale(arrow_right, arrow_size)

# Lista de flechas
arrows = []
arrow_types = ['up', 'down', 'left', 'right']

# Posiciones de las flechas en el eje X
arrow_positions = {
    'left': WIDTH * 0.25 - 25,
    'down': WIDTH * 0.5 - 25,
    'up': WIDTH * 0.75 - 25,
    'right': WIDTH - 75,
}

# Marca en la parte inferior
target_y = HEIGHT - 150

# Fuente para el puntaje
font = pygame.font.SysFont(None, 36)

# Variables del juego
clock = pygame.time.Clock()
score = 0
running = True
game_over = False

# Variables para aumentar dificultad
arrow_speed = 5  # Velocidad inicial de caída
arrow_frequency = 1000  # Frecuencia inicial de aparición (en milisegundos)
difficulty_increase_interval = 5000  # Cada 5 segundos aumenta la dificultad
last_difficulty_increase = pygame.time.get_ticks()

# Función para mostrar texto en pantalla
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Función para crear una nueva flecha
def create_arrow():
    arrow_type = random.choice(arrow_types)
    x = arrow_positions[arrow_type]
    y = -50  # Comienza fuera de la pantalla
    arrows.append({'type': arrow_type, 'x': x, 'y': y})

# Crear una flecha cada cierto tiempo
ADD_ARROW_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ARROW_EVENT, arrow_frequency)

# Bucle principal del juego
while running:
    clock.tick(60)  # 60 FPS

    current_time = pygame.time.get_ticks()

    # Aumentar dificultad cada cierto tiempo
    if not game_over and current_time - last_difficulty_increase > difficulty_increase_interval:
        arrow_speed += 1  # Incrementar velocidad de caída
        if arrow_frequency > 200:
            arrow_frequency -= 100  # Incrementar frecuencia de aparición
            pygame.time.set_timer(ADD_ARROW_EVENT, arrow_frequency)
        last_difficulty_increase = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == ADD_ARROW_EVENT and not game_over:
            create_arrow()

        if event.type == pygame.KEYDOWN and not game_over:
            for arrow in arrows:
                if abs(arrow['y'] - target_y) < 50:
                    if (event.key == pygame.K_UP and arrow['type'] == 'up') or \
                       (event.key == pygame.K_DOWN and arrow['type'] == 'down') or \
                       (event.key == pygame.K_LEFT and arrow['type'] == 'left') or \
                       (event.key == pygame.K_RIGHT and arrow['type'] == 'right'):
                        arrows.remove(arrow)
                        score += 10
                        break  # Solo una flecha por tecla

    if not game_over:
        # Mover flechas
        for arrow in arrows:
            arrow['y'] += arrow_speed  # Velocidad de caída actualizada

        # Verificar si alguna flecha ha pasado la parte inferior
        for arrow in arrows:
            if arrow['y'] > HEIGHT:
                game_over = True
                break

    # Dibujar todo
    screen.fill(BLACK)

    if not game_over:
        # Dibujar marca
        pygame.draw.rect(screen, WHITE, (0, target_y + 40, WIDTH, 5))

        # Dibujar flechas
        for arrow in arrows:
            if arrow['type'] == 'up':
                screen.blit(arrow_up, (arrow['x'], arrow['y']))
            elif arrow['type'] == 'down':
                screen.blit(arrow_down, (arrow['x'], arrow['y']))
            elif arrow['type'] == 'left':
                screen.blit(arrow_left, (arrow['x'], arrow['y']))
            elif arrow['type'] == 'right':
                screen.blit(arrow_right, (arrow['x'], arrow['y']))

        # Mostrar puntaje
        draw_text(f"Puntaje: {score}", font, WHITE, screen, WIDTH // 2, 30)

    else:
        # Pantalla de Game Over
        draw_text("¡Juego Terminado!", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text(f"Puntaje Final: {score}", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text("Presiona ESC para salir", font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 50)

        # Permitir al jugador salir del juego
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
