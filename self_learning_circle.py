import pygame
import random
import numpy as np

# Parámetros de la ventana
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
FPS = 60

# Parámetros del círculo (agente)
CIRCLE_RADIUS = 20
CIRCLE_COLOR = (0, 255, 0)  # Verde
circle_position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]  # Centro inicial

# Parámetros de los cuadrados (enemigos)
SQUARE_SIZE = 20
SQUARE_COLOR = (255, 0, 0)  # Rojo
square_speed = 5
squares = []  # Lista para guardar los cuadrados

# Parámetros del aprendizaje
epsilon = 1.0  # Probabilidad de tomar una acción aleatoria
epsilon_decay = 0.995  # Para reducir epsilon
learning_rate = 0.8
discount_factor = 0.95  # Factor de descuento

# Q-Tabla (estado-acción)
q_table = np.zeros((WINDOW_WIDTH // CIRCLE_RADIUS, WINDOW_HEIGHT // CIRCLE_RADIUS, 4))  # Estados y 4 acciones (arriba, abajo, izquierda, derecha)

# Función para elegir la mejor acción
def choose_action(state):
    if random.uniform(0, 1) < epsilon:  # Exploración
        return random.randint(0, 3)
    else:  # Explotación (mejor acción conocida)
        return np.argmax(q_table[state[0], state[1]])

# Función de actualización de la Q-Tabla
def update_q_table(state, action, reward, next_state):
    best_future_q = np.max(q_table[next_state[0], next_state[1]])
    q_table[state[0], state[1], action] = q_table[state[0], state[1], action] + learning_rate * (reward + discount_factor * best_future_q - q_table[state[0], state[1], action])

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Función para resetear la posición del círculo
def reset_circle():
    global circle_position
    circle_position = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]  # Vuelve al centro

# Bucle principal
running = True
square_spawn_rate = 30  # Cantidad de frames antes de que aparezca un nuevo cuadrado
frames_since_start = 0  # Para controlar el tiempo que pasa

while running:
    screen.fill((0, 0, 0))  # Fondo negro
    frames_since_start += 1

    # Aumentar la dificultad (más cuadrados) con el tiempo
    if frames_since_start % square_spawn_rate == 0:
        squares.append([random.randint(0, WINDOW_WIDTH - SQUARE_SIZE), 0])
        # Reducir el intervalo de generación de cuadrados
        if square_spawn_rate > 5:  # Limitar la velocidad de aparición
            square_spawn_rate -= 1

    # Mover los cuadrados hacia abajo
    for square in squares:
        square[1] += square_speed
        pygame.draw.rect(screen, SQUARE_COLOR, (square[0], square[1], SQUARE_SIZE, SQUARE_SIZE))

    # Eliminar cuadrados fuera de la pantalla
    squares = [square for square in squares if square[1] < WINDOW_HEIGHT]

    # Convertir la posición del círculo en un estado discreto
    state = [circle_position[0] // CIRCLE_RADIUS, circle_position[1] // CIRCLE_RADIUS]

    # Elegir acción (0: arriba, 1: abajo, 2: izquierda, 3: derecha)
    action = choose_action(state)

    # Aplicar la acción
    if action == 0 and circle_position[1] > CIRCLE_RADIUS:  # Arriba
        circle_position[1] -= CIRCLE_RADIUS
    elif action == 1 and circle_position[1] < WINDOW_HEIGHT - CIRCLE_RADIUS:  # Abajo
        circle_position[1] += CIRCLE_RADIUS
    elif action == 2 and circle_position[0] > CIRCLE_RADIUS:  # Izquierda
        circle_position[0] -= CIRCLE_RADIUS
    elif action == 3 and circle_position[0] < WINDOW_WIDTH - CIRCLE_RADIUS:  # Derecha
        circle_position[0] += CIRCLE_RADIUS

    # Dibujar el círculo
    pygame.draw.circle(screen, CIRCLE_COLOR, circle_position, CIRCLE_RADIUS)

    # Verificar colisiones y dar recompensas
    reward = 1  # Recompensa por estar vivo
    for square in squares:
        if pygame.Rect(square[0], square[1], SQUARE_SIZE, SQUARE_SIZE).colliderect(pygame.Rect(circle_position[0] - CIRCLE_RADIUS, circle_position[1] - CIRCLE_RADIUS, CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2)):
            reward = -100  # Penalización grande por chocar
            reset_circle()  # Reaparece en el centro al morir
            squares = []  # Reinicia los cuadrados para mayor claridad

    # Actualizar la Q-Tabla
    next_state = [circle_position[0] // CIRCLE_RADIUS, circle_position[1] // CIRCLE_RADIUS]
    update_q_table(state, action, reward, next_state)

    # Reducir epsilon para disminuir la exploración
    epsilon = max(0.1, epsilon * epsilon_decay)

    # Actualizar la pantalla
    pygame.display.flip()

    # Limitar los frames por segundo
    clock.tick(FPS)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
