import pygame
import sys

# Definir colores y dimensiones
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (200, 200, 200)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
BLOCKSIZE = 20  # Tamaño de cada bloque del grid

# Inicializar Pygame
pygame.init()

# Crear pantalla y reloj
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

def main():
    SCREEN.fill(BLACK)  # Llenar la pantalla con color negro inicialmente
    filled_cells = []  # Lista para almacenar las celdas que deben llenarse

    while True:
        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Evento de clic del mouse
                mouse_pos = pygame.mouse.get_pos()  # Obtener la posición del mouse
                grid_pos = (mouse_pos[0] // BLOCKSIZE, mouse_pos[1] // BLOCKSIZE)  # Calcular la celda del grid
                if grid_pos not in filled_cells:
                    filled_cells.append(grid_pos)  # Agregar la celda a la lista de celdas llenas
                print(f"Clic en la celda: {grid_pos}")  # Imprimir la posición de la celda

        # Aplicar gravedad gradual
        filled_cells = applyGravity(filled_cells)

        # Dibujar el grid y las celdas llenas
        SCREEN.fill(BLACK)  # Limpiar la pantalla
        drawGrid(filled_cells)  # Dibujar las celdas llenas y el grid

        pygame.display.update()  # Actualizar la pantalla
        CLOCK.tick(10)  # Controlar la velocidad del bucle a 10 FPS para un efecto más visible


def applyGravity(filled_cells):
    # Aplicar la gravedad de forma gradual
    new_filled_cells = set()  # Usar un set para almacenar las nuevas posiciones

    # Mover bloques solo una celda hacia abajo si es posible
    for cell in filled_cells:
        # Verificar si la celda debajo está vacía
        if (cell[0], cell[1] + 1) not in filled_cells and cell[1] + 1 < WINDOW_HEIGHT // BLOCKSIZE:
            # Mover el bloque una celda hacia abajo
            new_cell = (cell[0], cell[1] + 1)
            new_filled_cells.add(new_cell)
        else:
            # Si no puede moverse hacia abajo, mantener la posición actual
            new_filled_cells.add(cell)

    return list(new_filled_cells)  # Retornar las celdas como lista


def drawGrid(filled_cells):
    # Dibujar las celdas llenas
    for cell in filled_cells:
        x = cell[0] * BLOCKSIZE
        y = cell[1] * BLOCKSIZE
        rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
        pygame.draw.rect(SCREEN, WHITE, rect)  # Dibujar el rectángulo lleno

    # Dibujar el grid
    for x in range(0, WINDOW_WIDTH, BLOCKSIZE):
        for y in range(0, WINDOW_HEIGHT, BLOCKSIZE):
            rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            pygame.draw.rect(SCREEN, GRID_COLOR, rect, 1)


# Llamar a la función principal
if __name__ == "__main__":
    main()
