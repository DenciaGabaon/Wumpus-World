from time import sleep

import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (19, 194, 89)
DGREEN = (13, 165, 71)
CREAM = (242, 201, 121)
RED = (255, 0, 0)
BROWN = (43, 21, 17)
# Define constants
CELL_SIZE = 100
WORLD_SIZE = 4
PIT_PROBABILITY = 0.2
MAX_MOVES_PER_GAME = 1000

# Define actions
GOFORWARD = "GOFORWARD"
TURNLEFT = "TURNLEFT"
TURNRIGHT = "TURNRIGHT"
SHOOT = "SHOOT"
GRAB = "GRAB"
CLIMB = "CLIMB"

# Initialize Pygame
pygame.init()


# Set up the display
WINDOW_SIZE = (WORLD_SIZE * CELL_SIZE, WORLD_SIZE * CELL_SIZE)
window = pygame.display.set_mode((650, 400))  # Adjust the size as needed
pygame.display.set_caption("Wumpus World")

# Load images
agent_img = pygame.image.load("player.png")
agent_img = pygame.transform.scale(agent_img, (70, CELL_SIZE))
wumpus_img = pygame.image.load("wumpus.png")
wumpus_img = pygame.transform.scale(wumpus_img, (CELL_SIZE, CELL_SIZE))
pit_img = pygame.image.load("pit.png")
pit_img = pygame.transform.scale(pit_img, (CELL_SIZE, CELL_SIZE))
gold_img = pygame.image.load("gold.png")
gold_img = pygame.transform.scale(gold_img, (CELL_SIZE, CELL_SIZE))
bg_img = pygame.image.load("bg.jpg")
bg_img = pygame.transform.scale(bg_img, (400, 400))


instruction_font = pygame.font.SysFont(None, 22)
state = instruction_font.render("empty room", True, BLACK)


# Define fonts
font = pygame.font.Font(None, 24)

# Define classes
class Agent:
    def __init__(self):
        self.x = 3
        self.y = 0
        self.orientation = "RIGHT"
        self.has_gold = False
        self.has_arrow = True
        self.bump = False

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
            self.x = new_x
            self.y = new_y
            self.bump = False  # Reset bump to False if move is successful
        else:
            self.bump = True

    def turn_left(self):
        if self.orientation == "RIGHT":
            self.orientation = "UP"
        elif self.orientation == "UP":
            self.orientation = "LEFT"
        elif self.orientation == "LEFT":
            self.orientation = "DOWN"
        elif self.orientation == "DOWN":
            self.orientation = "RIGHT"

    def turn_right(self):
        if self.orientation == "RIGHT":
            self.orientation = "DOWN"
        elif self.orientation == "DOWN":
            self.orientation = "LEFT"
        elif self.orientation == "LEFT":
            self.orientation = "UP"
        elif self.orientation == "UP":
            self.orientation = "RIGHT"

    def grab(self):
        self.has_gold = True

    def climb(self):
        pass

    def shoot(self):
        pass

class WumpusWorld:
    def __init__(self):
        self.agent = Agent()
        self.grid = [[Cell() for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
        self.generate_world()

    def generate_world(self):
        occupied_cells = set()  # Keep track of occupied cells

        # Randomly place pits with a probability of 0.2 in each cell except [0, 3]
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                if (row, col) == (3, 0):
                    continue  # Skip [0, 3]
                if random.random() < PIT_PROBABILITY:
                    self.grid[row][col].has_pit = True
                    occupied_cells.add((row, col))  # Mark cell as occupied

        # Randomly place wumpus
        while True:
            wumpus_row, wumpus_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (wumpus_row, wumpus_col) in occupied_cells or (wumpus_row, wumpus_col) == (3, 0):
                continue  # Skip occupied cells and [0, 3]
            self.grid[wumpus_row][wumpus_col].has_wumpus = True
            occupied_cells.add((wumpus_row, wumpus_col))  # Mark cell as occupied
            break

        # Randomly place gold
        while True:
            gold_row, gold_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (gold_row, gold_col) in occupied_cells or (gold_row, gold_col) == (3, 0):
                continue  # Skip occupied cells and [0, 3]
            self.grid[gold_row][gold_col].has_gold = True
            occupied_cells.add((gold_row, gold_col))  # Mark cell as occupied
            break

    '''def generate_world(self):
        occupied_cells = set()  # Keep track of occupied cells
        occupied_cells.add((0, 3))  # Mark initial cell as occupied
        occupied_cells.add((1, 3))  # Mark the adjacent cell as occupied

        # Randomly place pits
        num_pits = random.randint(1, 3)  # Generate a random number of pits between 1 and 3
        for _ in range(num_pits):
            while True:
                row, col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
                if (row, col) in occupied_cells or random.random() >= PIT_PROBABILITY:
                    continue  # Skip occupied cells and cells that don't meet the pit probability
                self.grid[row][col].has_pit = True
                occupied_cells.add((row, col))  # Mark cell as occupied
                break

        # Randomly place wumpus
        while True:
            wumpus_row, wumpus_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (wumpus_row, wumpus_col) in occupied_cells:
                continue  # Skip occupied cells
            self.grid[wumpus_row][wumpus_col].has_wumpus = True
            occupied_cells.add((wumpus_row, wumpus_col))  # Mark cell as occupied
            break

        # Randomly place gold
        while True:
            gold_row, gold_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (gold_row, gold_col) in occupied_cells:
                continue  # Skip occupied cells
            self.grid[gold_row][gold_col].has_gold = True
            occupied_cells.add((gold_row, gold_col))  # Mark cell as occupied
            break
'''

    def draw(self):
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                cell = self.grid[row][col]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell.has_pit:
                    window.blit(pit_img, rect)
                    print(f"Cell [{row},{col}]: Pit")
                elif cell.has_wumpus:
                    window.blit(wumpus_img, rect)
                    print(f"Cell [{row},{col}]: Wumpus")
                elif cell.has_gold:
                    window.blit(gold_img, rect)
                    print(f"Cell [{row},{col}]: Gold")
                else:
                    print(f"Cell [{row},{col}]: Empty")




# Define classes


class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)  # The position and size of the button
        self.text = text  # The text on the button
        self.color = GREEN  # The color of the button
        self.text_color = (43, 21, 17)  # The color of the text
        self.font = pygame.font.Font(None, 24)  # The font of the text

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect, border_radius=20)  # Draw the button
        text_surface = self.font.render(self.text, True, self.text_color)  # Render the text
        text_rect = text_surface.get_rect(center=self.rect.center)  # Center the text on the button
        window.blit(text_surface, text_rect)  # Draw the text

class Cell:
    def __init__(self):
        self.has_pit = False
        self.has_wumpus = False
        self.has_gold = False

# Create the Wumpus World
world = WumpusWorld()
restart_button = Button((410, 317, 230, 70), "Restart")


# Game loop
running = True
while running:

    #window.fill(BLACK, (0, 600, 100, 100))
    # Blit the instructions onto the surface

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for a mouse button down event
            if restart_button.rect.collidepoint(event.pos):  # Check if the click was within the button's rect
                world = WumpusWorld()  # Restart the game
                sleep(0.1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                world.agent.move(-1, 0)
            elif event.key == pygame.K_DOWN:
                world.agent.move(1, 0)
            elif event.key == pygame.K_LEFT:
                world.agent.move(0, -1)
            elif event.key == pygame.K_RIGHT:
                world.agent.move(0, 1)
            elif event.key == pygame.K_SPACE:
                world.agent.grab()
            elif event.key == pygame.K_RETURN:
                world.agent.climb()


    # Fill the backgrounda
    window.fill(DGREEN)
    window.blit(bg_img, (0, 0))

    # Draw the grid lines
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(window, BLACK, (x, 0), (x, WINDOW_SIZE[1]))
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(window, BLACK, (0, y), (WINDOW_SIZE[0], y))

    # Draw the Wumpus World
    world.draw()

    # Draw agent
    agent_rect = pygame.Rect(world.agent.y * CELL_SIZE, world.agent.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    window.blit(agent_img, agent_rect)
    print(f"Agent: [{world.agent.x},{world.agent.y}]")

    restart_button.draw()

    # Display percept status
    adjacent_pit = (
            (world.agent.x > 0 and world.grid[world.agent.x - 1][world.agent.y].has_pit) or  # Check above
            (world.agent.y > 0 and world.grid[world.agent.x][world.agent.y - 1].has_pit) or  # Check left
            (world.agent.x < WORLD_SIZE - 1 and world.grid[world.agent.x + 1][world.agent.y].has_pit) or  # Check below
            (world.agent.y < WORLD_SIZE - 1 and world.grid[world.agent.x][world.agent.y + 1].has_pit)  # Check right
    )

    adjacent_wumpus = (
            (world.agent.y > 0 and world.grid[world.agent.x - 1][world.agent.y].has_wumpus) or  # Check above
            (world.agent.x > 0 and world.grid[world.agent.x][world.agent.y - 1].has_wumpus) or  # Check left
            (world.agent.y < WORLD_SIZE - 1 and world.grid[world.agent.y + 1][
                world.agent.x].has_wumpus) or  # Check below
            (world.agent.x < WORLD_SIZE - 1 and world.grid[world.agent.y][world.agent.x + 1].has_wumpus)  # Check right
    )

    in_gold_cell = world.grid[world.agent.x][world.agent.y].has_gold


    pygame.draw.rect(window, GREEN, (410, 12, 230, 300), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 25, 210, 140), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 170, 210, 55), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 230, 210, 70), border_radius=20)

    # Check if the agent has found the gold
    if world.grid[world.agent.x][world.agent.y].has_gold:
        print("You've found the gold! You win!")
        state_text = "You've found the gold!\n You win!"
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, GREEN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20

    # Check if the agent has fallen into a pit
    elif world.grid[world.agent.x][world.agent.y].has_pit:
        print("You've fallen into a pit! Game over.")
        state_text = "You've fallen into a pit!\n Game over."
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, RED)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20

    # Check if the agent has been eaten by the wumpus
    elif world.grid[world.agent.x][world.agent.y].has_wumpus:
        print("You've been eaten by the wumpus! Game over.")
        state_text = "You've been eaten by\nthe wumpus! Game over."
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, RED)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20

    else:
        print("empty room")
        state_text = "          Empty room"
        # Render the state text
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, BROWN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20  # Adjust this value as needed for spacing


    # Display the state text
    percept_text = f"Stench: {adjacent_wumpus}\nBreeze: {adjacent_pit}\nGlitter: {in_gold_cell}\nBump: {world.agent.bump}\nScream: None"
    percept_lines = percept_text.splitlines()
    y_offset = 50
    for line in percept_lines:
        percept_surface = font.render(line, True, BROWN)
        window.blit(percept_surface, (440, y_offset))
        y_offset += 20  # Adjust this value as needed for spacing



    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
