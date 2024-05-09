'''HUMAN PLAYER WUMPUS WORLD GAME'''

"""
Copyright © 2024 Gabaon, Deniece Winslhet A.

This code is protected by copyright law. Unauthorized reproduction, distribution,
or modification is prohibited.
"""

from time import sleep
import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
ALMOND = (193, 154, 107)
GREEN = (19, 194, 89)
DGREEN = (13, 165, 71)
CREAM = (242, 201, 121)
RED = (255, 0, 0)
BROWN = (43, 21, 17)
DDGREEN = (0, 46, 14)
LGREEN = (97, 149, 90)
# Define constants
CELL_SIZE = 100
WORLD_SIZE = 4
PIT_PROBABILITY = 0.2

GOLD_REWARD = 1000
DEATH_PENALTY = -1000
ACTION_PENALTY = -1
ARROW_PENALTY = -10

# Initialize score and game state variables
score = 0




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
pygame.display.set_caption("Wumpus World Human")

# Load images
agent_img = pygame.image.load("assets/img/player.png")
agent_img = pygame.transform.scale(agent_img, (70, CELL_SIZE))
wumpus_img = pygame.image.load("assets/img/wumpus.png")
wumpus_img = pygame.transform.scale(wumpus_img, (CELL_SIZE, CELL_SIZE))
pit_img = pygame.image.load("assets/img/pit.png")
pit_img = pygame.transform.scale(pit_img, (CELL_SIZE, CELL_SIZE))
gold_img = pygame.image.load("assets/img/gold.png")
gold_img = pygame.transform.scale(gold_img, (CELL_SIZE, CELL_SIZE))
bg_img = pygame.image.load("assets/img/bg.jpg")
bg_img = pygame.transform.scale(bg_img, (400, 400))

shoot_right = pygame.image.load("assets/img/shoot - right.jpg")
shoot_right = pygame.transform.scale(shoot_right, (70, 70))
shoot_left = pygame.image.load("assets/img/shoot - left.jpg")
shoot_left = pygame.transform.scale(shoot_left, (70, 70))
shoot_up = pygame.image.load("assets/img/shoot - up.jpg")
shoot_up = pygame.transform.scale(shoot_up, (70, 70))
shoot_down = pygame.image.load("assets/img/shoot - down.jpg")
shoot_down = pygame.transform.scale(shoot_down, (70, 70))
top_wall = pygame.image.load("assets/img/top_wall.png")
top_wall = pygame.transform.scale(top_wall, (CELL_SIZE, CELL_SIZE))


# Before the game loop, load the breeze sound
pygame.mixer.init()
breeze_sound = pygame.mixer.Sound("assets/sounds/wind2.wav")  # Replace "breeze_sound.wav" with your actual breeze sound file
stench_sound = pygame.mixer.Sound("assets/sounds/flies.wav")  # Replace "stench_sound.wav" with your actual stench sound file
scream_sound = pygame.mixer.Sound("assets/sounds/scream.mp3")  # Replace "scream_sound.wav" with your actual scream sound file
glitter_sound = pygame.mixer.Sound("assets/sounds/chimes.mp3")  # Replace "gold_sound.wav" with your actual gold sound file
victory_sound = pygame.mixer.Sound("assets/sounds/victory.wav")  # Replace "victory_sound.wav" with your actual victory sound file
lose_sound = pygame.mixer.Sound("assets/sounds/lose.wav")  # Replace "lose_sound.wav" with your actual lose sound file
gameloop = pygame.mixer.Sound("assets/sounds/gameloop.mp3")  # Replace "breeze_sound.wav" with your actual breeze sound file

channel1 = gameloop.play(-1)  # Play the gameloop sound on loop
channel1.set_volume(0.5)  # Set the volume to 10%

instruction_font = pygame.font.SysFont(None, 22)
state = instruction_font.render("empty room", True, BROWN)



shooting_instructions_displayed = False
wumpus_shot = False
gold_retrieved = False
shot_missed = False
no_arrow_state = False



# Define fonts
font = pygame.font.Font(None, 24)
instruction = pygame.font.Font(None, 16)
bold_font = pygame.font.Font(None, 16)
bold_font.set_bold(True)


# Initialize grid covers
grid_covers = [[True for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
grid_covers[3][0] = False  # Remove cover for grid (3, 0)

# Display Grid Covers
def draw_grid_covers():
    for row in range(WORLD_SIZE):
        for col in range(WORLD_SIZE):
            if grid_covers[row][col]:
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                window.blit(top_wall, rect)

# Remove Grid Covers
def uncover_grid(x, y):
    if 0 <= x < WORLD_SIZE and 0 <= y < WORLD_SIZE:
        grid_covers[x][y] = False

# Define classes
class Agent:
    def __init__(self):
        self.x = 3
        self.y = 0
        self.orientation = "RIGHT"
        self.has_gold = False
        self.has_arrow = True
        self.bump = False
        self.has_pit = False
        self.has_wumpus = False

    def move(self, dx, dy):
        global score  # Add global score variable

        new_x = self.x + dx
        new_y = self.y + dy

        # Check if the new position has a pit or wumpus
        if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
            if world.grid[new_x][new_y].has_pit or world.grid[new_x][new_y].has_wumpus:
                score += DEATH_PENALTY  # Increment score by death penalty
                if world.grid[new_x][new_y].has_pit:
                    print("You've fallen into a pit! Game over.")
                    self.has_pit = True
                elif world.grid[new_x][new_y].has_wumpus:
                    print("You've been eaten by the wumpus! Game over.")
                    self.has_wumpus = True
            '''elif world.grid[new_x][new_y].has_gold:
                self.has_gold = True'''
        else:
            self.bump = True  # Reset bump to False if move is successful

        # Update agent's position
        if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
            self.x = new_x
            self.y = new_y
            score += ACTION_PENALTY


    def grab(self):
        global gold_retrieved, score

        if world.grid[world.agent.x][world.agent.y].has_gold:
            world.grid[self.x][self.y].has_gold = False
            score += GOLD_REWARD
            gold_retrieved = True
            print("You've found the gold! You win!")


    def shoot(self):
        global no_arrow_state, shooting_instructions_displayed, wumpus_shot, score, shot_missed

        if self.has_arrow:
            if pygame.key.get_pressed()[pygame.K_UP]:
                for x in range(self.x - 1, -1, -1):
                    if world.grid[x][self.y].has_wumpus:
                        world.grid[x][self.y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        score += ARROW_PENALTY
                        score += GOLD_REWARD
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_up, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
                    else:
                        score += ARROW_PENALTY
                        shot_missed = True
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_up, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)

            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                for x in range(self.x + 1, WORLD_SIZE):
                    if world.grid[x][self.y].has_wumpus:
                        world.grid[x][self.y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        score = ARROW_PENALTY
                        score += GOLD_REWARD
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_down, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
                    else:
                        score += ARROW_PENALTY
                        shot_missed = True
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_down, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                for y in range(self.y - 1, -1, -1):
                    if world.grid[self.x][y].has_wumpus:
                        world.grid[self.x][y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        score += ARROW_PENALTY
                        score += GOLD_REWARD
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_left, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
                    else:
                        score += ARROW_PENALTY
                        shot_missed = True
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_left, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                for y in range(self.y + 1, WORLD_SIZE):
                    if world.grid[self.x][y].has_wumpus:
                        world.grid[self.x][y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        score += ARROW_PENALTY
                        score += GOLD_REWARD
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_right, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
                    else:
                        score += ARROW_PENALTY
                        shot_missed = True
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_right, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)

        else:
            no_arrow_state = True
            print("No arrows left.")



class WumpusWorld:
    def __init__(self):
        self.agent = Agent()
        self.grid = [[Cell() for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
        self.generate_world()

    def generate_world(self):
        occupied_cells = set()  # Keep track of occupied cells

        # Randomly decide the number of pits (between 1 and 4)
        num_pits = random.randint(1, 4)

        # Randomly place the decided number of pits in the grid
        for _ in range(num_pits):
            while True:
                pit_row, pit_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
                if (pit_row, pit_col) in occupied_cells or (pit_row, pit_col) == (3, 0):
                    continue  # Skip occupied cells and [0, 3]
                # Add a probability check here
                if random.random() < PIT_PROBABILITY:
                    self.grid[pit_row][pit_col].has_pit = True
                    occupied_cells.add((pit_row, pit_col))  # Mark cell as occupied
                    break


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


    def draw(self):
        for row in range(WORLD_SIZE):
            for col in range(WORLD_SIZE):
                cell = self.grid[row][col]
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if cell.has_pit:
                    window.blit(pit_img, rect)
                    #print(f"Cell [{row},{col}]: Pit")
                elif cell.has_wumpus:
                    window.blit(wumpus_img, rect)
                    #print(f"Cell [{row},{col}]: Wumpus")
                elif cell.has_gold:
                    window.blit(gold_img, rect)
                    #print(f"Cell [{row},{col}]: Gold")
                else:
                    pass
                #print(f"Cell [{row},{col}]: Empty")





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


# Define the class for the circular button
class CircleButton(Button):
    def __init__(self, center, radius, text):
        self.radius = radius  # The radius of the button
        # Calculate the position and size of the button based on the center and radius
        x = center[0] - radius
        y = center[1] - radius
        width = 2 * radius
        height = 2 * radius
        super().__init__((x, y, width, height), text)  # Call the superclass initialization with the corrected parameters

    def draw(self):
        # Draw the button
        pygame.draw.circle(window, GREEN, self.rect.center, self.radius)
        # Render the text
        text_surface = self.font.render(self.text, True, self.text_color)
        # Center the text on the button
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Draw the text
        window.blit(text_surface, text_rect)



class Cell:
    def __init__(self):
        self.has_pit = False
        self.has_wumpus = False
        self.has_gold = False



instruction_text = [
    "Movement:",
    "Use arrow keys to move the agent.",
    "",
    "Actions:",
    "Spacebar: Grab gold on agent's cell.",
    "Enter/Return key: Shoot in agent's",
    "direction.",
    "Note: Agent has 1 arrow per game.",
    "",
    "Percepts:",
    "Stench: Wumpus nearby.",
    "Breeze: Pit nearby.",
    "Glitter: Gold present.",
    "Bump: Agent hit wall.",
    "Scream: Wumpus killed.",
    "",
    "Game Over Conditions:",
    "Falling into pit.",
    "Eaten by Wumpus.",
    "Shooting Wumpus.",
    "Grabbing gold and escaping.",
    "",
    "Scoring:",
    "Reward for gold.",
    "Penalty for pit, Wumpus, or arrow.",
    "Final score based on rewards and",
    " penalties.",
    "",
    "Restart:",
    "Click restart button to restart game."
]

def display_instructions():
    # Create a new surface for the instructions
    instruction_surface = pygame.Surface((460, 350), pygame.SRCALPHA)  # Adjust the size as needed

    # Draw the instructions on the surface
    pygame.draw.rect(instruction_surface, DDGREEN, pygame.Rect(0, 0, 460, 350), border_radius=20)
    pygame.draw.rect(instruction_surface, ALMOND, pygame.Rect(10, 35, 440, 300), border_radius=20)  # Adjust the width for columns

    column1 = instruction_text[:len(instruction_text)//2]
    column2 = instruction_text[len(instruction_text)//2:]

    y_offset = 80
    for line in column1:
        if line.strip() in ["Movement:", "Actions:", "Percepts:", "Game Over Conditions:", "Scoring:", "Restart:"]:
            text_surface = bold_font.render(line, True, BROWN)
        else:
            text_surface = instruction.render(line, True, BROWN)
        instruction_surface.blit(text_surface, (30, y_offset))
        y_offset += 15  # Adjust this value as needed for spacing

    y_offset = 80
    for line in column2:
        if line.strip() in ["Movement:", "Actions:", "Game Over Conditions:", "Scoring:", "Restart:"]:
            text_surface = bold_font.render(line, True, BROWN)
        else:
            text_surface = instruction.render(line, True, BROWN)
        instruction_surface.blit(text_surface, (240, y_offset))  # Adjust x position for second column
        y_offset += 15  # Adjust this value as needed for spacing

    # Create the "X" button
    x_button = Button((500, 25, 50, 50), "X")  # Adjust the position and size as needed
    x_button.color = LGREEN  # Change the color of the button

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if x_button.rect.collidepoint(event.pos):  # Check if the "X" button was clicked
                    return  # Return to the game

        # Draw the instruction surface and the "X" button
        window.blit(instruction_surface, (100, 12))  # Adjust the position as needed
        x_button.draw()

        pygame.display.flip()



# Create the Wumpus World
world = WumpusWorld()
restart_button = Button((410, 317, 160, 70), "Restart")
instruction_button = CircleButton((605, 352), 25, "?")





# Game loop
running = True
while running:
    print(shooting_instructions_displayed)
    #window.fill(BLACK, (0, 600, 100, 100))
    # Blit the instructions onto the surface


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for a mouse button down event
            if restart_button.rect.collidepoint(event.pos):  # Check if the click was within the button's rect
                world = WumpusWorld()  # Restart the game
                wumpus_shot = False
                gold_retrieved = False
                shot_missed = False
                no_arrow_state = False
                grid_covers = [[True for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
                grid_covers[3][0] = False  # Remove cover for grid (3, 0)
                sleep(0.1)
            elif instruction_button.rect.collidepoint(event.pos):
                display_instructions()
        elif event.type == pygame.KEYDOWN and shooting_instructions_displayed == False and gold_retrieved == False and wumpus_shot == False \
                and world.agent.has_gold == False and world.agent.has_pit == False and world.agent.has_wumpus == False:
            shot_missed = False
            no_arrow_state = False
            if event.key == pygame.K_UP:
                world.agent.move(-1, 0)
                uncover_grid(world.agent.x, world.agent.y)
            elif event.key == pygame.K_DOWN:
                world.agent.move(1, 0)
                uncover_grid(world.agent.x, world.agent.y)
            elif event.key == pygame.K_LEFT:
                world.agent.move(0, -1)
                uncover_grid(world.agent.x, world.agent.y)
            elif event.key == pygame.K_RIGHT:
                world.agent.move(0, 1)
                uncover_grid(world.agent.x, world.agent.y)
            elif event.key == pygame.K_SPACE:
                world.agent.grab()
                victory_sound.play()
            elif event.key == pygame.K_RETURN:
                if world.agent.has_arrow:
                    shooting_instructions_displayed = True
                    print("Shooting instructions displayed")
                else:
                    no_arrow_state = True
                    print("No arrows left.")



    # Fill the backgrounda
    window.fill(DGREEN)
    window.blit(bg_img, (0, 0))

    # Draw the grid lines
    for x in range(0, WINDOW_SIZE[0], CELL_SIZE):
        pygame.draw.line(window, ALMOND, (x, 0), (x, WINDOW_SIZE[1]))
    for y in range(0, WINDOW_SIZE[1], CELL_SIZE):
        pygame.draw.line(window, ALMOND, (0, y), (WINDOW_SIZE[0], y))

    # Draw the Wumpus World
    world.draw()
    draw_grid_covers()


    # Draw agent
    agent_rect = pygame.Rect(world.agent.y * CELL_SIZE, world.agent.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    window.blit(agent_img, agent_rect)
    print(f"Agent: [{world.agent.x},{world.agent.y}]")

    restart_button.draw()
    instruction_button.draw()
    # Display percept status


    adjacent_pit = (
        (world.agent.x > 0 and world.grid[world.agent.x - 1][world.agent.y].has_pit) or  # Check above
        (world.agent.x < WORLD_SIZE - 1 and world.grid[world.agent.x + 1][world.agent.y].has_pit) or  # Check below
        (world.agent.y > 0 and world.grid[world.agent.x][world.agent.y - 1].has_pit) or  # Check left
        (world.agent.y < WORLD_SIZE - 1 and world.grid[world.agent.x][world.agent.y + 1].has_pit)  # Check right
    )

    adjacent_wumpus = (
        (world.agent.x > 0 and world.grid[world.agent.x - 1][world.agent.y].has_wumpus) or  # Check above
        (world.agent.x < WORLD_SIZE - 1 and world.grid[world.agent.x + 1][world.agent.y].has_wumpus) or  # Check below
        (world.agent.y > 0 and world.grid[world.agent.x][world.agent.y - 1].has_wumpus) or  # Check left
        (world.agent.y < WORLD_SIZE - 1 and world.grid[world.agent.x][world.agent.y + 1].has_wumpus)  # Check right
    )


    in_gold_cell = world.grid[world.agent.x][world.agent.y].has_gold

    if in_gold_cell:
        glitter_sound.play()
    else:
        glitter_sound.stop()

    if adjacent_pit:
        breeze_sound.play()
    else:
        breeze_sound.stop()

    if adjacent_wumpus:
        stench_sound.play()
    else:
        stench_sound.stop()




    pygame.draw.rect(window, GREEN, (410, 12, 230, 300), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 25, 210, 140), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 170, 210, 55), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 230, 210, 70), border_radius=20)

    # Check if the agent has found the gold
    # After the game loop
    # Determine the color based on game outcome
    if world.grid[world.agent.x][world.agent.y].has_pit or world.grid[world.agent.x][world.agent.y].has_wumpus:
        state_color = RED  # Game over color
    else:
        state_color = BROWN  # Win color

    # Display the appropriate state text based on game outcome
    if world.grid[world.agent.x][world.agent.y].has_pit:
        state_text = "You've fallen into a pit!\n Game over."
        lose_sound.play()
    elif world.grid[world.agent.x][world.agent.y].has_wumpus:
        state_text = "You've been eaten by\nthe wumpus! Game over."
        lose_sound.play()
    elif wumpus_shot:
        state_text = "You've shot the wumpus!\n You win!"
        scream_sound.play()
        victory_sound.play()
    elif gold_retrieved and world.agent.has_gold == False:
        state_text = "You've found the gold!\n You win!"
        victory_sound.play()
    elif shooting_instructions_displayed:
            state_text = "Choose direction to shoot\n using arrow keys."
            world.agent.shoot()
    elif shot_missed == True:
        state_text = "You missed the wumpus!"
    elif no_arrow_state == True:
        state_text = "No arrows left."
    else:
        state_text = "        Empty room"

    # Render the state text with the appropriate color
    state_lines = state_text.splitlines()
    y_coords = 250
    for line in state_lines:
        state_surface = instruction_font.render(line, True, state_color)
        window.blit(state_surface, (440, y_coords))
        y_coords += 20


    # Display the state text
    percept_text = f"Stench: {adjacent_wumpus}\nBreeze: {adjacent_pit}\nGlitter: {in_gold_cell}\nBump: {world.agent.bump}\nScream: {wumpus_shot}"
    percept_lines = percept_text.splitlines()
    y_offset = 50
    for line in percept_lines:
        percept_surface = font.render(line, True, BROWN)
        window.blit(percept_surface, (440, y_offset))
        y_offset += 20  # Adjust this value as needed for spacing

    score_surface = instruction_font.render(f"Final Score: {score}", True, BROWN)
    window.blit(score_surface, (440, 190))




    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
