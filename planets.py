import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1900, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar system")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (0, 150, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)
ORANGE = (255, 128, 0)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67e-11
    SCALE = 180 / AU # scale factor 100 PIXELS = 1 AU
    TIMESTEP = 3600*24 # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.color = color

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win, scale, offset_x, offset_y):
        x = (self.x * scale) + WIDTH / 2 + offset_x
        y = (self.y * scale) + HEIGHT / 2 + offset_y
        adjusted_radius = max(1, round(self.radius * scale / Planet.SCALE))
        if adjusted_radius > 0 and 0 <= x <= WIDTH and 0 <= y <= HEIGHT:  # Only draw if within screen bounds
            pygame.draw.circle(win, self.color, (int(x), int(y)), adjusted_radius)

def main():
    run = True
    clock = pygame.time.Clock()
    scale = Planet.SCALE
    offset_x, offset_y = 0, 0
    min_scale = 0.1
    dragging = False
    last_mouse_pos = None

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    mercury = Planet(0.38 * Planet.AU, 0, 2, GREY, 3.302 * 10**23)
    venus = Planet(0.72 * Planet.AU, 0, 9, ORANGE, 4.867 * 10**24)
    earth = Planet(Planet.AU, 0, 10, LIGHT_BLUE, 5.972 * 10**24)
    mars = Planet(1.52 * Planet.AU, 0, 5, RED, 6.39 * 10**23)
    jupiter = Planet(5.20 * Planet.AU, 0, 21, RED, 1.898 * 10**27)
    saturn = Planet(9.58 * Planet.AU, 0, 19, RED, 5.68 * 10**26)
    uranus = Planet(19.14 * Planet.AU, 0, 14, RED, 8.68 * 10**25)
    neptune = Planet(30.20 * Planet.AU, 0, 13, RED, 1.02 * 10**26)
    sun.sun = True
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up to zoom in
                    scale *= 1.1
                elif event.button == 5:  # Scroll down to zoom out
                    scale /= 1.1
                    if scale < min_scale:  # Prevent scale from becoming too small
                        scale = min_scale
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if last_mouse_pos is not None:
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    offset_x += dx
                    offset_y += dy
                last_mouse_pos = (mouse_x, mouse_y)
        
        for planet in planets:
            planet.draw(WIN, scale, offset_x, offset_y)
        
        pygame.display.update()
    pygame.quit()

main()