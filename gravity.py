import pygame
import math

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation with Ball Collision and Friction")

# Definición de colores
WHITE = (255, 255, 255)
FPS = 60
# Constantes
GRAVITY = 9.8 / FPS  # Dividimos por 60 porque el juego corre a 60 FPS
BALL_RADIUS = 10
FRICTION = 0.98  # Coeficiente de fricción para el suelo
BALL_CREATION_DELAY = 500  # Tiempo mínimo entre bolas en milisegundos (0.5 segundos)

# Clase Ball
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0

    def update(self):
        # Aumentar la velocidad vertical por la gravedad
        self.y_vel += GRAVITY

        # Actualizar la posición usando la velocidad
        self.x += self.x_vel
        self.y += self.y_vel

        # Colisionar con el suelo para que la bola no atraviese el fondo
        if self.y >= HEIGHT - BALL_RADIUS:
            self.y = HEIGHT - BALL_RADIUS
            self.y_vel = -self.y_vel * 0.8  # Rebote con una pérdida de energía (damping)

            # Aplicar fricción al suelo
            self.x_vel *= FRICTION
            # Aplicar un poco de fricción a la velocidad vertical también (disminuye el rebote)
            self.y_vel *= FRICTION

            # Si la velocidad es muy pequeña, detenerla para evitar movimientos infinitesimales
            if abs(self.y_vel) < 0.1:
                self.y_vel = 0
            if abs(self.x_vel) < 0.1:
                self.x_vel = 0

        # Colisionar con las paredes para mantener las bolas en pantalla
        if self.x <= BALL_RADIUS or self.x >= WIDTH - BALL_RADIUS:
            self.x_vel = -self.x_vel

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)

# Función para detectar y manejar colisiones entre bolas
def handle_collisions(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball1 = balls[i]
            ball2 = balls[j]

            # Calcular la distancia entre los centros de las dos bolas
            dx = ball1.x - ball2.x
            dy = ball1.y - ball2.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= 2 * BALL_RADIUS:
                # Las bolas están colisionando
                # Normalizar la distancia
                nx = dx / distance
                ny = dy / distance

                # Velocidades relativas
                dvx = ball1.x_vel - ball2.x_vel
                dvy = ball1.y_vel - ball2.y_vel

                # Producto punto de las velocidades relativas y el vector normal
                dot_product = dvx * nx + dvy * ny

                # Evitar el cálculo si las bolas ya se están separando
                if dot_product > 0:
                    continue

                # Intercambiar la velocidad a lo largo de la dirección normal
                ball1.x_vel -= dot_product * nx
                ball1.y_vel -= dot_product * ny
                ball2.x_vel += dot_product * nx
                ball2.y_vel += dot_product * ny

# Función principal
def main():
    run = True
    clock = pygame.time.Clock()
    balls = []  # Lista para almacenar todas las bolas creadas
    last_ball_creation_time = 0  # Tiempo de creación de la última bola

    while run:
        clock.tick(FPS)  # Control de FPS

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                # Crear una nueva bola si ha pasado suficiente tiempo desde la última
                if current_time - last_ball_creation_time >= BALL_CREATION_DELAY:
                    mouse_pos = pygame.mouse.get_pos()
                    new_ball = Ball(mouse_pos[0], mouse_pos[1])
                    balls.append(new_ball)
                    last_ball_creation_time = current_time

        # Actualizar bolas
        for ball in balls:
            ball.update()

        # Manejar colisiones entre bolas
        handle_collisions(balls)

        # Dibujar en pantalla
        WIN.fill((0, 0, 0))  # Rellenar la pantalla con negro
        for ball in balls:
            ball.draw(WIN)  # Dibujar todas las bolas
        pygame.display.update()  # Actualizar la pantalla

    pygame.quit()  # Cerrar Pygame

# Ejecutar la función principal
if __name__ == "__main__":
    main()
