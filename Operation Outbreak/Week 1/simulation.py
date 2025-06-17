import pygame
import random
import math
from collections import defaultdict


WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
SCREEN_WIDTH = WIDTH + 400
SCREEN_HEIGHT = HEIGHT + 60
clock = pygame.time.Clock()
PERSON_RADIUS = 5

class State:
    def __init__(self, name, color, number=0):
        self.color = color
        self.name = name
        self.number = number

class Transition:
    def __init__(self, from_state, to_state, probability, requires_proximity=False, contact_with=None, effect_radius=5):
        self.from_state = from_state
        self.to_state = to_state
        self.probability = probability
        self.requires_proximity = requires_proximity
        self.contact_with = contact_with
        self.effect_radius = effect_radius

    def attempt(self, person, neighbors):
        if person.state != self.from_state:
            return

        if self.requires_proximity:
            for other in neighbors:
                if other is person:
                    continue
                if other.state == self.contact_with:
                    dx = person.x - other.x
                    dy = person.y - other.y
                    if dx*dx + dy*dy <= self.effect_radius**2:
                        if random.random() <= self.probability:
                            person.state = self.to_state
                            break
        else:
            if random.random() <= self.probability:
                person.state = self.to_state

class Model:
    def __init__(self, name="Generic Model"):
        self.name = name
        self.states = []
        self.transitions = []

    def add_state(self, name, color, number=0):
        state = State(name, color, number)
        self.states.append(state)
        return state

    def add_transition(self, from_state, to_state, probability, requires_proximity=False, contact_with=None, effect_radius=5):
        t = Transition(from_state, to_state, probability, requires_proximity, contact_with, effect_radius)
        self.transitions.append(t)

    def apply_transitions(self, person, neighbors):
        for t in self.transitions:
            t.attempt(person, neighbors)

    def count_states(self, people):
        counts = {state: 0 for state in self.states}
        for person in people:
            counts[person.state] += 1
        return counts
    
    def generate_people(self, width=600, height=600):
        people = []
        for state in self.states:
            for _ in range(state.number):
                person = Person(state)
                person.x = random.randint(25, width)
                person.y = random.randint(25, height)
                person.change_direction()
                people.append(person)
        random.shuffle(people)
        return people

class Person:
    def __init__(self, state):
        self.state = state
        self.x = random.randint(25, WIDTH)
        self.y = random.randint(25, HEIGHT)

        self.tmin = 30
        self.tmax = 60
        self.change_direction()

        self.close_infected = []

    def move(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        if (self.x >= WIDTH) or (self.x <= 28):
            self.vx = -1 * self.vx

        if (self.y >= HEIGHT) or (self.y <= 28):
            self.vy = -1 * self.vy

    def change_direction(self):
        v_mag = 0.4 * random.random() + 0.8
        theta = random.uniform(0, 2 * math.pi)
        self.vx = v_mag * math.cos(theta)
        self.vy = v_mag * math.sin(theta)
        self.change_direction_counter = random.randint(self.tmin, self.tmax);

    def set_state(self, state):
        self.state = state

    def get_color(self):
        return self.state.color
    
    def get_state(self):
        return self.state

    def update(self):
        self.change_direction_counter -= 1
        if self.change_direction_counter <= 0:
            self.change_direction()

    def draw(self, screen):
        pygame.draw.circle(screen, color=self.get_color(),
                               center=(self.x, self.y), radius=PERSON_RADIUS, width=0)

def partition_people(people):
    """Partition people into grid cells for spatial partitioning."""
    grid = defaultdict(list)
    for person in people:
        grid_x = int(person.x // GRID_SIZE)
        grid_y = int(person.y // GRID_SIZE)
        grid[(grid_x, grid_y)].append(person)
    return grid

def get_neighbors(grid, person):
    """Get neighbors of a person from the same and adjacent grid cells."""
    grid_x = int(person.x // GRID_SIZE)
    grid_y = int(person.y // GRID_SIZE)
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighbors.extend(grid.get((grid_x + dx, grid_y + dy), []))
    return neighbors

def run_simulation(model):
    pygame.init()
    pygame.font.init()
    my_font = pygame.font.SysFont('Sitka Banner', 35)
    frames = 0
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(model.name)
    running = True

    people = model.generate_people(WIDTH, HEIGHT)

    WHITE = (255, 255, 255)


    while running:
        frames += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        grid = partition_people(people)

        pygame.draw.rect(screen, color=WHITE,
                         rect=(10, 10, WIDTH + 5, HEIGHT + 5),
                         width=5)
        
        text_surface = my_font.render(f"Frames: {frames}", True, WHITE)
        screen.blit(text_surface, (10, HEIGHT + 20))

        for person in people:
            person.draw(screen)
            person.update()
            person.move()

            neighbors = get_neighbors(grid, person)
            model.apply_transitions(person, neighbors)

        counts = model.count_states(people)

        top_y = 50
        spacing = 80

        for i, state in enumerate(model.states):
            y_base = top_y + i * spacing

            center_y = y_base

            pygame.draw.circle(screen, color=state.color,
                            center=(WIDTH + 50, center_y),
                            radius=PERSON_RADIUS)

            label = my_font.render(state.name, True, WHITE)
            screen.blit(label, (WIDTH + 45, center_y - 45))

            count_text = my_font.render(f"{counts[state]}", True, WHITE)
            count_width = count_text.get_width()
            screen.blit(count_text, (SCREEN_WIDTH - 30 - count_width, center_y - 45))

            rect_x = WIDTH + 75
            rect_width = 300
            rect_height = 10
            top_of_bar = center_y - rect_height // 2
            perc_fill = counts[state] / len(people)

            pygame.draw.rect(screen, color=state.color,
                            rect=(rect_x, top_of_bar, rect_width, rect_height), width=2)

            pygame.draw.rect(screen, color=state.color,
                            rect=(rect_x, top_of_bar, rect_width * perc_fill, rect_height))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()