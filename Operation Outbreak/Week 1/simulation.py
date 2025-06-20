import pygame
import random
import math
from collections import defaultdict


WIDTH = 600
HEIGHT = 600
GRID_SIZE = 20
SCREEN_WIDTH = WIDTH + 400
SCREEN_HEIGHT = HEIGHT + 60
PERSON_RADIUS = 5

clock = pygame.time.Clock()

class State:
    def __init__(self, name, color, number=0, moving=True, effect_radius=PERSON_RADIUS, show_cloud=False, isolated=False):
        self.color = color
        self.name = name
        self.number = number
        self.moving = moving
        self.effect_radius = effect_radius
        self.show_cloud = show_cloud
        self.isolated = isolated

class Transition:
    def __init__(self, from_state, to_state, probability, requires_proximity=False, contact_with=None, effect_radius=5, min_required=0):
        self.from_state = from_state
        self.to_state = to_state
        self.probability = probability
        self.requires_proximity = requires_proximity
        self.contact_with = contact_with
        self.effect_radius = self.to_state.effect_radius
        self.min_infected = min_required
        self.min_reached = False

    def attempt(self, person, neighbors, people):
        
        if person.state != self.from_state:
            return
        
        if self.min_infected > 0:
            num_infected = sum(1 for p in people if p.state == self.contact_with)
            if num_infected < self.min_infected:
                if not self.min_reached:
                    return
            self.min_reached = True

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

    def add_state(self, name, color, number=0, moving=True, show_cloud=False, effect_radius=5, isolated=False):
        state = State(name, color, number, moving, effect_radius, show_cloud, isolated)
        self.states.append(state)
        return state

    def add_transition(self, from_state, to_state, probability, requires_proximity=False, contact_with=None, effect_radius=5, min_required=0):
        t = Transition(from_state, to_state, probability, requires_proximity, contact_with, effect_radius, min_required)
        self.transitions.append(t)

    def apply_transitions(self, person, neighbors, people):
        for t in self.transitions:
            t.attempt(person, neighbors, people)

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
        self.has_moved_to_isolation = False
        self.was_isolated = False

        self.tmin = 30
        self.tmax = 60
        self.change_direction()

        self.close_infected = []

    def move(self):
        if not self.state.moving:
            return
        self.x = self.x + self.vx
        self.y = self.y + self.vy

        if not self.state.isolated:
            if self.was_isolated:
                self.x = random.randint(25, WIDTH)
                self.y = random.randint(25, HEIGHT)
                self.was_isolated = False
                
            if (self.x >= WIDTH) or (self.x <= 30):
                self.vx = -self.vx
                if self.x >= WIDTH:
                    self.x = self.x - PERSON_RADIUS
                if self.x <= 30:
                    self.x = self.x + PERSON_RADIUS

            if (self.y >= HEIGHT) or (self.y <= 30):
                self.vy = -self.vy
                if self.y >= HEIGHT:
                    self.y = self.y - PERSON_RADIUS
                if self.y <= 30:
                    self.y = self.y + PERSON_RADIUS
            
        if self.state.isolated:
            if (self.x <= WIDTH + 50) or (self.x >= (WIDTH / 3) + WIDTH + 50):
                self.vx = -self.vx
                if self.x >= (WIDTH / 3) + WIDTH + 50:
                    self.x = self.x - PERSON_RADIUS
                if self.x <= WIDTH + 50:
                    self.x = self.x + PERSON_RADIUS

            if (self.y <= HEIGHT - (HEIGHT / 3) + 30) or (self.y >= (HEIGHT / 3) + HEIGHT - (HEIGHT / 3)):
                self.vy = -self.vy
                if self.y >= (HEIGHT / 3) + HEIGHT - (HEIGHT / 3) + 30:
                    self.y = self.y - PERSON_RADIUS
                if self.y <= HEIGHT - (HEIGHT / 3):
                    self.y = self.y + PERSON_RADIUS

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
        
        if self.state.show_cloud:
            pygame.draw.circle(screen, color=self.get_color(),
                               center=(self.x, self.y), radius=self.state.effect_radius, width=1)

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
    
    exist_isolated = False
    for s in model.states:
        if s.isolated:
            exist_isolated = True

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
            
            if person.state.isolated:
                if not person.has_moved_to_isolation:
                    person.was_isolated = True
                    person.x = random.randint(WIDTH + 60, int((WIDTH / 3) + WIDTH + 20))
                    person.y = random.randint(int(HEIGHT - (HEIGHT / 3) + 15), int((HEIGHT / 3) + HEIGHT - (HEIGHT / 3)))
                    person.has_moved_to_isolation = True
            else:
                person.has_moved_to_isolation = False

            neighbors = get_neighbors(grid, person)
            model.apply_transitions(person, neighbors, people)
            
        if exist_isolated:
            pygame.draw.rect(screen, color=WHITE, rect=(WIDTH + 40, HEIGHT - (HEIGHT / 3), WIDTH / 3 + 15, HEIGHT / 3 + 15), width=5)

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