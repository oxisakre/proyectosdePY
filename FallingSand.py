import pygame
import sys
import random

# tamaño de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 4 # Tamaño de cada celda

# numero de columnas y filas divido por el tamaño de cada celula
cols = WINDOW_WIDTH // CELL_SIZE
rows = WINDOW_HEIGHT // CELL_SIZE
color_grid = {}  # diccionario de colores
# inciar el juego
pygame.init()
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Grid en Pygame")


# intento de grid
def make2DArray(cols, rows):
    arr = [[0 for _ in range(rows)] for _ in range(cols)]
    return arr


grid = make2DArray(cols, rows)
# poner valor a cada celda
for col in range(cols):
    for row in range(rows):
        grid[col][row] = 0


# dibujar grid
def drawGrid():
    SCREEN.fill((0, 0, 0))
    for col in range(cols):
        for row in range(rows):
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if grid[col][row] == 1:
                if (col, row) not in color_grid:
                    # genero un color random y lo guardo
                    r = random.randint(200, 255)
                    g = random.randint(190, 215)
                    b = random.randint(150, 180)
                    color_grid[(col, row)] = (r, g, b)

                # dibuja la celda con el color almacenado (esto es para que no para de cambiar de color constantemente)
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, color_grid[(col, row)], rect)


def gravity():
    for col in range(cols - 1, -1, -1):
        for row in range(rows - 2, -1, -1):
            state = grid[col][row]
            if state == 1:  # si en la celda hay arena
                below = (
                    grid[col][row + 1] if row + 1 < rows else 1
                )  # verificar si hay espacio debajo
                if below == 0:
                    # mover hacia abajo
                    grid[col][row + 1] = 1
                    grid[col][row] = 0
                else:
                    # comprobar las diagonales para hacer efecto de caida
                    direction = random.choice(
                        [-1, 1]
                    )  # hacer aleatorio el movimiento a la izquierda o derecha
                    if col + direction >= 0 and col + direction < cols:
                        side_below = (
                            grid[col + direction][row + 1] if row + 1 < rows else 1
                        )
                        if side_below == 0:
                            # mover hacia abajo y a la izquierda o derecha
                            grid[col + direction][row + 1] = 1
                            grid[col][row] = 0


# Bucle principal del juego
def main():
    clock = pygame.time.Clock()
    pressed = False

    # Cantidad de veces que la gravedad se aplica por cada frame
    gravity_steps_per_frame = 5 # Incrementa este valor para hacer que la arena caiga más rápido

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # click del mouse
                pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False

        if pressed:
            mouse_pos = pygame.mouse.get_pos()  # posición del mouse
            mouse_col = mouse_pos[0] // CELL_SIZE
            mouse_row = mouse_pos[1] // CELL_SIZE
            if 0 <= mouse_col < cols and 0 <= mouse_row < rows:
                amount = random.randint(10, 15)
                for _ in range(amount):  # Lanza arena en un área aleatoria alrededor del mouse
                    rand_col = mouse_col + random.randint(-10, 10)
                    rand_row = mouse_row + random.randint(-10, 10)
                    if 0 <= rand_col < cols and 0 <= rand_row < rows:
                        grid[rand_col][rand_row] = 1

        # Aplicar gravedad varias veces por frame
        for _ in range(gravity_steps_per_frame):
            gravity()

        # Dibujar y actualizar la pantalla
        drawGrid()
        pygame.display.update()

        # Limitar la tasa de fotogramas por segundo (FPS)
        clock.tick(60)


if __name__ == "__main__":
    main()
