'''displaying of text nalang need ayusin
then next is AI'''


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

shoot_right = pygame.image.load("shoot - right.jpg")
shoot_right = pygame.transform.scale(shoot_right, (70, 70))
shoot_left = pygame.image.load("shoot - left.jpg")
shoot_left = pygame.transform.scale(shoot_left, (70, 70))
shoot_up = pygame.image.load("shoot - up.jpg")
shoot_up = pygame.transform.scale(shoot_up, (70, 70))
shoot_down = pygame.image.load("shoot - down.jpg")
shoot_down = pygame.transform.scale(shoot_down, (70, 70))


instruction_font = pygame.font.SysFont(None, 22)
state = instruction_font.render("empty room", True, BROWN)



shooting_instructions_displayed = False
wumpus_shot = False
gold_retrieved = False



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


    def grab(self):
        global gold_retrieved, score
        self.has_gold = True

        if world.grid[world.agent.x][world.agent.y].has_gold:
            world.grid[self.x][self.y].has_gold = False
            score += GOLD_REWARD
            gold_retrieved = True
            print("You've found the gold! You win!")


    def shoot(self):
        global state_state, shooting_instructions_displayed, wumpus_shot

        if self.has_arrow:
            if pygame.key.get_pressed()[pygame.K_UP]:
                for x in range(self.x - 1, -1, -1):
                    if world.grid[x][self.y].has_wumpus:
                        world.grid[x][self.y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_up, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                for x in range(self.x + 1, WORLD_SIZE):
                    if world.grid[x][self.y].has_wumpus:
                        world.grid[x][self.y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(self.y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_down, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                for y in range(self.y - 1, -1, -1):
                    if world.grid[self.x][y].has_wumpus:
                        world.grid[self.x][y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_left, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break
            elif pygame.key.get_pressed()[pygame.K_RIGHT]:
                for y in range(self.y + 1, WORLD_SIZE):
                    if world.grid[self.x][y].has_wumpus:
                        world.grid[self.x][y].has_wumpus = False
                        print("You shot the Wumpus!")
                        self.has_arrow = False
                        shooting_instructions_displayed = False
                        wumpus_shot = True
                        # Blit the shoot image onto the window
                        agent_rect = pygame.Rect(y * CELL_SIZE, self.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                        window.blit(shoot_right, agent_rect)
                        pygame.display.flip()  # Update the display
                        pygame.time.delay(500)  # Delay for 500 milliseconds (0.5 seconds)
                        break

        else:
            print("No arrows left.")


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
                sleep(0.1)
        elif event.type == pygame.KEYDOWN and shooting_instructions_displayed == False and gold_retrieved == False and wumpus_shot == False:
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
                shooting_instructions_displayed = True
                print("Shooting instructions displayed")


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

    # Draw agent
    agent_rect = pygame.Rect(world.agent.y * CELL_SIZE, world.agent.x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    window.blit(agent_img, agent_rect)
    print(f"Agent: [{world.agent.x},{world.agent.y}]")

    restart_button.draw()

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


    pygame.draw.rect(window, GREEN, (410, 12, 230, 300), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 25, 210, 140), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 170, 210, 55), border_radius=20)
    pygame.draw.rect(window, CREAM, (420, 230, 210, 70), border_radius=20)

    # Check if the agent has found the gold


    # Check if the agent has fallen into a pit
    if world.grid[world.agent.x][world.agent.y].has_pit:
        score += DEATH_PENALTY
        game_over = True
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
        score += DEATH_PENALTY
        game_over = True
        print("You've been eaten by the wumpus! Game over.")
        state_text = "You've been eaten by\nthe wumpus! Game over."
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, RED)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20

    elif wumpus_shot == True:
        score += GOLD_REWARD
        game_over = True
        print("You've shot the wumpus! You win!")
        state_text = "You've shot the wumpus!\n You win!"
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, GREEN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20
    elif gold_retrieved == True:
        state_text = "You've found the gold!\n You win!"
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, GREEN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20


    '''else:
        print("empty room")
        state_text = "          Empty room"
        # Render the state text
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, BROWN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20'''  # Adjust this value as needed for spacing
    if shooting_instructions_displayed == True:
        state_text = "Choose direction to shoot\n using arrow keys."
        state_lines = state_text.splitlines()
        y_coords = 250
        for line in state_lines:
            state_surface = instruction_font.render(line, True, BROWN)
            window.blit(state_surface, (440, y_coords))
            y_coords += 20
        world.agent.shoot()

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
