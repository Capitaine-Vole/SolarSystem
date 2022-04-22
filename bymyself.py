import pygame
import math

pygame.init()

WIDTH, HEIGHT = 600, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet simulation - BY MYSELF TRYING TO UNDERSTAND PHYSIC !!!!!!!")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

class Planet:
    AU = 149.6e6 * 1000 #distance between sun and earth
    G = 6.67428e-11 # constant idk what is the utility but real numbers
    SCALE = 190 / AU # 1 AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
        
            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x = other.x
        other_y = other.y
        dx = other_x - self.x
        dy = other_y - self.y
        r = math.sqrt(dx**2 + dy**2)

        if other.sun:
            self.distance_to_sun = r

        f = self.G * self.mass * other.mass / r**2
        theta = math.atan2(dy, dx)
        Fx = math.cos(theta) * f
        Fy = math.sin(theta) * f
        return Fx, Fy

    def update_position(self, planets):
        Tfx = 0
        Tfy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            Tfx += fx
            Tfy += fy

        self.x_vel = self.x_vel + Tfx / self.mass * self.TIMESTEP
        self.y_vel = self.y_vel + Tfy / self.mass * self.TIMESTEP

        self.x = self.x + self.x_vel * self.TIMESTEP
        self.y = self.x + self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = -29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, earth, mars]


    clock = pygame.time.Clock()
    run = True

    while run:

        clock.tick(60)
        win.fill((0, 0, 0))

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(win)

        pygame.display.update()

    pygame.quit()

main()