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
BROWN = (150, 75, 0)
RE_BROWN = (168, 66, 45)
BLUE = (0, 0, 255)
VIOLET = (128, 0, 128)

FONT = pygame.font.SysFont("Arial", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67e-11
    SCALE = 200 /AU # scale factor 100 PIXELS = 1 AU   
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

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                point_x, point_y = point
                updated_x = (point_x * scale) + WIDTH / 2 + offset_x
                updated_y = (point_y * scale) + HEIGHT / 2 + offset_y
                updated_points.append((updated_x, updated_y))
            pygame.draw.lines(win, self.color, False, updated_points, 1)

        adjusted_radius = max(1, round(self.radius * scale / Planet.SCALE))
        if adjusted_radius > 0 and 0 <= x <= WIDTH and 0 <= y <= HEIGHT:  # Only draw if within screen bounds
            pygame.draw.circle(win, self.color, (int(x), int(y)), adjusted_radius)
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * other.mass * self.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y
    
    def update_positions(self, planets):
        total_force_x = total_force_y = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_force_x += fx
            total_force_y += fy
        self.x_vel += total_force_x / self.mass * self.TIMESTEP
        self.y_vel += total_force_y / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
    
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
    mercury.y_vel = 47.9 * 1000
    venus = Planet(0.72 * Planet.AU, 0, 9, ORANGE, 4.867 * 10**24)
    venus.y_vel = 35 * 1000
    earth = Planet(Planet.AU, 0, 10, LIGHT_BLUE, 5.972 * 10**24)
    earth.y_vel = 29.8 * 1000
    mars = Planet(1.52 * Planet.AU, 0, 5, RED, 6.39 * 10**23)
    mars.y_vel = 24.1 * 1000
    jupiter = Planet(5.20 * Planet.AU, 0, 21, RE_BROWN, 1.898 * 10**27)
    jupiter.y_vel = 13.1 * 1000
    saturn = Planet(9.58 * Planet.AU, 0, 19, BROWN, 5.68 * 10**26)
    saturn.y_vel = 9.7 * 1000
    uranus = Planet(19.14 * Planet.AU, 0, 14, BLUE, 8.68 * 10**25)
    uranus.y_vel = 6.8 * 1000
    neptune = Planet(30.20 * Planet.AU, 0, 13, VIOLET, 1.02 * 10**26)
    neptune.y_vel = 5.4 * 1000
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
                        continue
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
            planet.update_positions(planets)
            planet.draw(WIN, scale, offset_x, offset_y)
        
        pygame.display.update()
    pygame.quit()

main()