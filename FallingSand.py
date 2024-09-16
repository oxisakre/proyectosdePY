import pygame
import sys
import time

# tamaño de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CELL_SIZE = 10  # Tamaño de cada celda

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
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, (255, 255, 255), rect, 1)
            if grid[col][row] == 1:
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(SCREEN, (255, 255, 255), rect)

def gravity():
    for col in range(cols):
        for row in range(rows - 2, -1, -1):
            if grid[col][row] == 1 and grid[col][row + 1] == 0:
                grid[col][row + 1] = 1
                grid[col][row] = 0
# Bucle principal del juego
def main():
    clock = pygame.time.Clock()
    gravity_timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # click del mouse
                mouse_pos = pygame.mouse.get_pos()  # posicion del mouse
                columna = mouse_pos[0] // CELL_SIZE
                fila =  mouse_pos[1] // CELL_SIZE
                print((mouse_pos[1] // CELL_SIZE))
                grid[columna][fila] = 1
        
        # timer de la gravedad
        gravity_timer += clock.get_time()
        if gravity_timer > 40:  # hacer que vaya cayendo con lentitud
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
