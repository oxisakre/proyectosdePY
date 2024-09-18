import pygame
import sys
import random

# tamaño de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 5  # Tamaño de cada celda

# numero de columnas y filas divido por el tamaño de cada celula
cols = WINDOW_WIDTH // CELL_SIZE
rows = WINDOW_HEIGHT // CELL_SIZE

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
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect)

def gravity():
    for col in range(cols - 2, -1, -1):
        for row in range(rows - 2, -1, -1):
            state = grid[col][row]
            if state == 1:  # si en la celda hay arena
                below = grid[col][row + 1] if row + 1 < rows else 1  # verificar si hay espacio debajo
                if below == 0:
                    # mover hacia abajo
                    grid[col][row + 1] = 1
                    grid[col][row] = 0
                else:
                    # comprobar las diagonales para hacer efecto de caida
                    direction = random.choice([-1, 1])  # hacer aleatorio el movimiento a la izquierda o derecha
                    if col + direction >= 0 and col + direction < cols:
                        side_below = grid[col + direction][row + 1] if row + 1 < rows else 1
                        if side_below == 0:
                            # mover hacia abajo y a la izquierda o derecha
                            grid[col + direction][row + 1] = 1
                            grid[col][row] = 0

# Bucle principal del juego
def main():
    clock = pygame.time.Clock()
    gravity_timer = 0
    pressed = False
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
            mouse_pos = pygame.mouse.get_pos()  # posicion del mouse
            mouse_col = mouse_pos[0] // CELL_SIZE
            mouse_row =  mouse_pos[1] // CELL_SIZE
            print(f'{mouse_col, mouse_row}')
            grid[mouse_col][mouse_row] = 1

        # timer de la gravedad
        gravity_timer += clock.get_time()
        if gravity_timer > 15:  # velocidad de la arena
            gravity()
            drawGrid()
            pygame.display.update()
            gravity_timer = 0


        # dibujar el grid
        drawGrid()
        # Actualizar la pantalla
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
