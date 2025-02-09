import pygame
import math
import pickle
import neat
import sys

# Constants
WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 188.2 / 3  # Car width
CAR_SIZE_Y = 230 / 3    # Car length

target_x = 1600  # X-coordinate of the target
target_y = 500   # Y-coordinate of the target

stat_x = 250     # Initial X position of the car
stat_y = 100     # Initial Y position of the car

BORDER_COLOR = (255, 255, 255, 255)  # Color of obstacles for collision detection

class Car:
    def __init__(self):
        # Istniejąca inicjalizacja samochodu
        self.sprite = pygame.image.load('car.png').convert()
        self.sprite = pygame.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite

        self.distance_to_target = 9999
        self.previous_distance_to_target = 9999
        self.position = [stat_x, stat_y]
        self.angle = 0
        self.speed = 20
        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2]

        self.radars = []
        self.alive = True
        self.collision_penalized = False
        self.angle_history = []  # Track angle changes
        self.spinning_penalized = False  # Track if already penalized for spinning

        self.path = []

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position)
        self.draw_radar(screen)
        self.draw_path(screen)

    def draw_path(self, screen):
        # Rysowanie śladu przejazdu
        if len(self.path) > 1:
            pygame.draw.lines(screen, (255, 0, 0), False, self.path, 3)  # Ślad w kolorze czerwonym

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        extra_points = []
        for i in range(1, 5):
            ratio = i / 5.0
            extra_points.extend([  # Początkowe punkty pomocnicze
                [
                    self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * CAR_SIZE_X * ratio,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * CAR_SIZE_Y * ratio
                ],
                [
                    self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * CAR_SIZE_X * ratio,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * CAR_SIZE_Y * ratio
                ],
                [
                    self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * CAR_SIZE_X * ratio,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * CAR_SIZE_Y * ratio
                ],
                [
                    self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * CAR_SIZE_X * ratio,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * CAR_SIZE_Y * ratio
                ]
            ])
        for point in self.corners + extra_points:
            x, y = int(point[0]), int(point[1])
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                if game_map.get_at((x, y)) == BORDER_COLOR:
                    self.alive = False
                    break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        if length < 300:
            dist = int(math.sqrt((x - self.center[0]) ** 2 + (y - self.center[1]) ** 2))
            self.radars.append([(x, y), dist])


    def get_data(self):
        return_values = [0] * 6
        for i, radar in enumerate(self.radars):
            if i < 5:
                return_values[i] = int(radar[1] / 30)

        self.previous_distance_to_target = self.distance_to_target
        self.distance_to_target = int(math.sqrt((target_x - self.center[0]) ** 2 + (target_y - self.center[1]) ** 2))
        return_values[5] = self.distance_to_target

        return return_values


    def update(self, game_map):
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], HEIGHT - 120)

        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length,
                    self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length,
                     self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length,
                       self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length,
                        self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.check_collision(game_map)
        self.path.append((int(self.center[0]), int(self.center[1])))
        self.radars.clear()

        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def is_alive(self):
        return self.alive

    def rotate_center(self, image, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rotated_image.get_rect(center=image.get_rect().center)
        return rotated_image


def run_simulation(genome):
    net = neat.nn.FeedForwardNetwork.create(genome, config)

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_map = pygame.image.load('map4.jpg').convert()

    car = Car()
    car.alive = True

    clock = pygame.time.Clock()

    while car.is_alive():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        output = net.activate(car.get_data())
        choice = output.index(max(output))
        if choice == 0:
            car.angle += 10
        elif choice == 1:
            car.angle -= 10
        elif choice == 2 and car.speed - 2 >= 12:
            car.speed -= 2
        else:
            car.speed += 2

        car.update(game_map)

        distance_to_target = car.distance_to_target
        if distance_to_target < 50:  # You can adjust the threshold as needed
            print("Car reached the target!")
            car.speed = 0
            #wstrzymaj symulację do czasu naciesniecia esc
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit(0)
                pygame.display.flip()
                clock.tick(60)





        screen.blit(game_map, (0, 0))
        pygame.draw.circle(screen, (0, 0, 255, 255), (target_x, target_y), 20)
        car.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    # Load the saved best genome
    with open("best_genome2.pkl", "rb") as f:
        best_genome = pickle.load(f)

    config_path = "config2.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    run_simulation(best_genome)
