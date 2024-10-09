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
FPS = 60
FONT = pygame.font.SysFont("Arial", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67e-11
    SCALE = 200 / AU  # scale factor 100 PIXELS = 1 AU   
    TIMESTEP = 3600 * 24 # 1 day in seconds

    def __init__(self, x, y, radius, color, mass, name):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0
        self.orbit_count = 0  # Contador de vueltas al sol
        self.previous_y = y  # Para comprobar cuando se completa una vuelta
        self.has_crossed_sun = False  # Flag para verificar si ha cruzado el eje del sol
    
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
        if adjusted_radius > 0 and (
            0 <= x + adjusted_radius <= WIDTH or 0 <= x - adjusted_radius <= WIDTH or
            0 <= y + adjusted_radius <= HEIGHT or 0 <= y - adjusted_radius <= HEIGHT
        ):  # Draw if any part of the planet is within screen bounds
            pygame.draw.circle(win, self.color, (int(x), int(y)), adjusted_radius)
        if not self.sun:
            distance_text = FONT.render(f"{self.name}", 1, WHITE)
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
        if self.sun:
            return  # El sol no debe moverse

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

        # Actualizar el contador de vueltas
        current_distance_to_sun = math.sqrt(self.x ** 2 + self.y ** 2)
        
        # Comprobar si el planeta ha cruzado el eje Y del sol (aproximadamente)
        if self.previous_y < 0 and self.y > 0:
            self.orbit_count += 0.5
        elif self.previous_y > 0 and self.y < 0:
            self.orbit_count += 0.5

        self.previous_y = self.y


def draw_distance_table(win, planets, mouse_pos, selected_planet, click_processed):
    title_text = FONT.render("Planet Distances to the Sun:", 1, WHITE)
    win.blit(title_text, (10, HEIGHT - 180))

    for i, planet in enumerate(planets):
        if planet.sun:
            continue  # No mostrar el sol en la tabla
        if planet == selected_planet:
            color = (255, 0, 0)  # Rojo para el planeta seleccionado
        else:
            color = WHITE

        distance_text = FONT.render(f"{planet.name} : {format(round(planet.distance_to_sun / 1000), ',')} km | Orbits: {planet.orbit_count}", 1, color)
        text_rect = distance_text.get_rect(topleft=(10, HEIGHT - 160 + i * 20))
        
        # Dibuja el texto en la tabla
        win.blit(distance_text, text_rect.topleft)

        # Detectar clic
        if pygame.mouse.get_pressed()[0] and not click_processed:  # Si se ha hecho clic (botón izquierdo del mouse)
            if text_rect.collidepoint(mouse_pos):  # Si el clic está sobre este texto
                return planet, True  # Retorna el planeta seleccionado y marca el clic como procesado

    return selected_planet, click_processed

def move_camera_to_planet(selected_planet, scale, offset_x, offset_y):
    # Recalcular la posición del planeta en pantalla
    target_x = (selected_planet.x * scale) + WIDTH / 2
    target_y = (selected_planet.y * scale) + HEIGHT / 2

    # Mover la cámara directamente hacia el planeta seleccionado
    offset_x = WIDTH / 2 - target_x  # Recalcula la diferencia del centro de la pantalla
    offset_y = HEIGHT / 2 - target_y

    return offset_x, offset_y

def zoom_to_planet(selected_planet, scale):
    target_zoom = max(300 / selected_planet.radius, 0.05)  # Ajustar el zoom según el radio del planeta
    scale += (target_zoom - scale) * 0.1  # Zoom progresivo

    # Limitar el zoom
    if scale > 1.2:
        scale = 1.2
    elif scale < 0.005:
        scale = 0.005

    return scale

def main():
    run = True
    clock = pygame.time.Clock()
    scale = Planet.SCALE
    offset_x, offset_y = 0, 0
    dragging = False
    last_mouse_pos = None
    selected_planet = None
    click_processed = False

    # Inicialización de planetas
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "Sun")
    mercury = Planet(0.38 * Planet.AU, 0, 2, GREY, 3.302 * 10**23, "Mercury")
    mercury.y_vel = 47.9 * 1000
    venus = Planet(0.72 * Planet.AU, 0, 9, ORANGE, 4.867 * 10**24, "Venus")
    venus.y_vel = 35 * 1000
    earth = Planet(Planet.AU, 0, 10, LIGHT_BLUE, 5.972 * 10**24, "Earth")
    earth.y_vel = 29.8 * 1000
    mars = Planet(1.52 * Planet.AU, 0, 5, RED, 6.39 * 10**23, "Mars")
    mars.y_vel = 24.1 * 1000
    jupiter = Planet(5.20 * Planet.AU, 0, 21, RE_BROWN, 1.898 * 10**27, "Jupiter")
    jupiter.y_vel = 13.1 * 1000
    saturn = Planet(9.58 * Planet.AU, 0, 19, BROWN, 5.68 * 10**26, "Saturn")
    saturn.y_vel = 9.7 * 1000
    uranus = Planet(19.14 * Planet.AU, 0, 14, BLUE, 8.68 * 10**25, "Uranus")
    uranus.y_vel = 6.8 * 1000
    neptune = Planet(30.20 * Planet.AU, 0, 13, VIOLET, 1.02 * 10**26, "Neptune")
    neptune.y_vel = 5.4 * 1000
    sun.sun = True
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while run:
        clock.tick(FPS)
        WIN.fill((0, 0, 0))  # Limpiar la pantalla
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.button == 1:
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button in [4, 5]:  # Scroll para zoom in/out
                    old_scale = scale
                    if event.button == 4:
                        scale *= 1.1
                    else:
                        scale /= 1.1
                    offset_x -= (mouse_x - WIDTH / 2 - offset_x) * (scale / old_scale - 1)
                    offset_y -= (mouse_y - HEIGHT / 2 - offset_y) * (scale / old_scale - 1)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    click_processed = False  # Permitir procesar el siguiente clic
                elif event.button == 3 and selected_planet:  # Deseleccionar planeta con botón derecho del mouse
                    selected_planet = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - last_mouse_pos[0]
                    dy = mouse_y - last_mouse_pos[1]
                    offset_x += dx
                    offset_y += dy
                    last_mouse_pos = (mouse_x, mouse_y)

        # Actualizar el planeta seleccionado desde la tabla
        selected_planet, click_processed = draw_distance_table(WIN, planets, mouse_pos, selected_planet, click_processed)

        # Si hay un planeta seleccionado, mover la cámara hacia él y hacer zoom
        if selected_planet:
            offset_x, offset_y = move_camera_to_planet(selected_planet, scale, offset_x, offset_y)
            zoom_to_planet(selected_planet, scale)

        # Dibujar los planetas y actualizarlos
        for planet in planets:
            planet.update_positions(planets)
            planet.draw(WIN, scale, offset_x, offset_y)

        # Dibujar el sol si no está en pantalla
        sun_x = (sun.x * scale) + WIDTH / 2 + offset_x
        sun_y = (sun.y * scale) + HEIGHT / 2 + offset_y
        if not (0 <= sun_x + sun.radius * scale <= WIDTH and 0 <= sun_y + sun.radius * scale <= HEIGHT):
            pygame.draw.circle(WIN, YELLOW, (50, HEIGHT - 50), 20)  # Dibuja el sol en la esquina inferior izquierda

        pygame.display.update()  # Actualizar la pantalla
    pygame.quit()

main()