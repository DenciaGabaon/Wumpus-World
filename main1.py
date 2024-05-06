'''BACKTRACK USING SAFE CELLS'''


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
shot_missed = False
no_arrow_state = False
marked_pits = []
marked_wumpus = []



# Define fonts
font = pygame.font.Font(None, 24)
clock = pygame.time.Clock()
FPS = 10

# Define classes
'''class Agent:
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
        else:
            self.bump = True  # Reset bump to False if move is successful

        # Update agent's position
        if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
            self.x = new_x
            self.y = new_y
            score += ACTION_PENALTY


    def grab(self):
        global gold_retrieved, score
        self.has_gold = True

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
            print("No arrows left.")'''



class Agent:
    def __init__(self):
        # Initialize agent properties
        self.x = 3
        self.y = 0
        self.has_gold = False
        self.has_arrow = True
        self.bump = False
        self.has_pit = False
        self.has_wumpus = False
        self.safe_cells = {(3, 0)}  # Initialize with the starting cell
        self.visited_cells = {(3, 0)}  # Initialize with the starting cell

    def move(self):
        global score, gold_retrieved, marked_pits, marked_wumpus# Add global score variable
        # Get adjacent cells of the current cell
        print("Marked pits: ", marked_pits)
        print("Marked wumpus: ", marked_wumpus)

        if adjacent_pit == True:
            self.mark_pit(self.x, self.y)
        elif adjacent_wumpus == True:
            self.mark_wumpus(self.x, self.y)

        if marked_pits:
            for pits in marked_pits:
                p = self.wumpit_get_adj(pits[0], pits[1])
                for cell in p:
                    adjacent_x, adjacent_y = cell
                    pp = world.detect_breeze(adjacent_x, adjacent_y)
                    if pp == True:
                        continue
                        # that cell has wumpus
                    else:
                        self.safe_cells.add((adjacent_x, adjacent_y))
                        self.safe_cells.add((pits[0], pits[1]))

                print("p:", p)
            '''for pit in marked_wumpus:
                adjacent_cells = self.wumpit_get_adj(pit[0], pit[1])'''

            marked_pits = []
        elif marked_wumpus:
            for wumpus in marked_wumpus:
                w = self.wumpit_get_adj(wumpus[0], wumpus[1])
                for cell in w:
                    adjacent_x, adjacent_y = cell
                    ww = world.detect_stench(adjacent_x, adjacent_y)
                    if ww == True:
                        continue
                        #that cell has wumpus
                    else:
                        self.safe_cells.add((adjacent_x, adjacent_y))
                        self.safe_cells.add((wumpus[0], wumpus[1]))
                print("w:", w)
            '''for pit in marked_wumpus:
                adjacent_cells = self.wumpit_get_adj(pit[0], pit[1])'''
            marked_wumpus = []
        else:
            adjacent_cells = self.get_adjacent_cells()

        # Randomly choose one adjacent cell to move
        new_x, new_y = random.choice(adjacent_cells)

        # Update agent's position and mark the cell as visited
        self.x, self.y = new_x, new_y
        score += ACTION_PENALTY
        self.visited_cells.add((self.x, self.y))


        # Check for breeze and stench in the new cell

        if world.grid[self.x][self.y].has_gold:
            self.has_gold = True
            score += GOLD_REWARD
            world.grid[self.x][self.y].has_gold = False
            gold_retrieved = True
        elif world.grid[new_x][new_y].has_pit or world.grid[new_x][new_y].has_wumpus:
            score += DEATH_PENALTY
            if world.grid[new_x][new_y].has_pit:
                print("You've fallen into a pit! Game over.")
                self.has_pit = True
            elif world.grid[new_x][new_y].has_wumpus:
                print("You've been eaten by the wumpus! Game over.")
                self.has_wumpus = True
        else:
            self.safe_cells.add((new_x, new_y))

    def wumpit_get_adj(self, x, y):

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_cells = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
                if (new_x, new_y) in self.safe_cells:
                    continue
                else:
                    adjacent_cells.append((new_x, new_y))

        return adjacent_cells

    def get_adjacent_cells(self):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        adjacent_cells = []

        for dx, dy in directions:
            new_x, new_y = self.x + dx, self.y + dy

            if 0 <= new_x < WORLD_SIZE and 0 <= new_y < WORLD_SIZE:
                adjacent_cells.append((new_x, new_y))


        return adjacent_cells

    def mark_pit(self, x, y):
        pit_adj = self.wumpit_get_adj(x, y)
        for cell in pit_adj:
            adjacent_x, adjacent_y = cell
            # Mark the adjacent cell as adjacent to the pit
            marked_pits.append((adjacent_x, adjacent_y))
            print(f"Perceived breeze at ({x}, {y}). Marking cell as pit.")
        print(pit_adj)

    def mark_wumpus(self, x, y):
        wumpus_adj = self.wumpit_get_adj(x, y)
        for cell in wumpus_adj:
            adjacent_x, adjacent_y = cell
            # Mark the adjacent cell as adjacent to the pit
            marked_wumpus.append((adjacent_x, adjacent_y))
            print(f"Perceived stench at ({x}, {y}). Marking cell as wumpus.")
        print(wumpus_adj)


    def shoot_at_stench(self):
        # Get the coordinates of adjacent cells
        adjacent_cells = [(self.x - 1, self.y), (self.x + 1, self.y), (self.x, self.y - 1), (self.x, self.y + 1)]

        # Check if any of the adjacent cells are safe
        safe_adjacent_cells = [cell for cell in adjacent_cells if cell in self.safe_cells]

        if safe_adjacent_cells:
            # If there are safe adjacent cells, randomly choose one to shoot
            target_cell = random.choice(safe_adjacent_cells)
            target_x, target_y = target_cell
            dx = target_x - self.x
            dy = target_y - self.y

            # Update agent's orientation
            if dx == 1:
                self.orientation = "DOWN"
            elif dx == -1:
                self.orientation = "UP"
            elif dy == 1:
                self.orientation = "RIGHT"
            elif dy == -1:
                self.orientation = "LEFT"

            # Shoot in the direction of the target cell
            self.shoot()

    def perform_action(self):
        if wumpus_shot or gold_retrieved == False:  # Check if the game is not over
            if world.grid[self.x][self.y].has_wumpus and self.has_arrow:
                # If the agent detects a stench and has an arrow, shoot
                self.shoot_at_stench()
            else:
                self.move()  # Move the agent based on inference


class WumpusWorld:
    def __init__(self):
        self.agent = Agent()
        self.grid = [[Cell() for _ in range(WORLD_SIZE)] for _ in range(WORLD_SIZE)]
        self.generate_world()

    def generate_world(self):
        occupied_cells = []  # Keep track of occupied cells

        # Randomly decide the number of pits (between 1 and 4)
        num_pits = random.randint(1, 4)

        # Randomly place the decided number of pits in the grid
        for _ in range(num_pits):
            while True:
                pit_row, pit_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
                if (pit_row, pit_col) in occupied_cells or (pit_row, pit_col) == (3, 0) or (pit_row, pit_col) ==(3,1) or (pit_row, pit_col) ==(2,0):
                    continue  # Skip occupied cells and [0, 3]
                # Add a probability check here
                if random.random() < PIT_PROBABILITY:
                    self.grid[pit_row][pit_col].has_pit = True
                    occupied_cells.append((pit_row, pit_col))  # Mark cell as occupied
                    break


        # Randomly place wumpus
        while True:
            wumpus_row, wumpus_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (wumpus_row, wumpus_col) in occupied_cells or (wumpus_row, wumpus_col) == (3, 0) or (wumpus_row, wumpus_col) ==(3,1) or (wumpus_row, wumpus_col) ==(2,0):
                continue  # Skip occupied cells and [0, 3]
            self.grid[wumpus_row][wumpus_col].has_wumpus = True
            occupied_cells.append((wumpus_row, wumpus_col))  # Mark cell as occupied
            break

        # Randomly place gold
        while True:
            gold_row, gold_col = random.randint(0, WORLD_SIZE - 1), random.randint(0, WORLD_SIZE - 1)
            if (gold_row, gold_col) in occupied_cells or (gold_row, gold_col) == (3, 0)  or (gold_row, gold_col) ==(3,1) or (gold_row, gold_col) ==(2,0):
                continue  # Skip occupied cells and [0, 3]
            self.grid[gold_row][gold_col].has_gold = True
            occupied_cells.append((gold_row, gold_col))  # Mark cell as occupied
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

    def detect_breeze(self, x, y):
        # Check if any adjacent cell contains a pit
        adjacent_pits = [
            (x - 1, y),  # Above
            (x + 1, y),  # Below
            (x, y - 1),  # Left
            (x, y + 1)  # Right
        ]

        for adjacent_x, adjacent_y in adjacent_pits:
            if 0 <= adjacent_x < WORLD_SIZE and 0 <= adjacent_y < WORLD_SIZE :
                if self.grid[adjacent_x][adjacent_y].has_pit:
                    return True  # Breeze detected

        return False

    def detect_stench(self, x, y):
        # Check if any adjacent cell contains a wumpus
        adjacent_wumpus = [
            (x - 1, y),  # Above
            (x + 1, y),  # Below
            (x, y - 1),  # Left
            (x, y + 1)  # Right
        ]

        for adjacent_x, adjacent_y in adjacent_wumpus:
            if 0 <= adjacent_x < WORLD_SIZE  and 0 <= adjacent_y < WORLD_SIZE :
                if self.grid[adjacent_x][adjacent_y].has_wumpus:
                    return True  # Stench detected

        return False  # No stench detected

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
    print("visired: ", world.agent.visited_cells)
    print("Ok: ", world.agent.safe_cells)


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
                sleep(0.1)

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

    if shooting_instructions_displayed == False and gold_retrieved == False and wumpus_shot == False \
         and world.agent.has_gold == False and world.agent.has_pit == False and world.agent.has_wumpus == False:
        world.agent.perform_action()

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
    elif world.grid[world.agent.x][world.agent.y].has_wumpus:
        state_text = "You've been eaten by\nthe wumpus! Game over."
    elif wumpus_shot:
        state_text = "You've shot the wumpus!\n You win!"
    elif gold_retrieved:
        state_text = "You've found the gold!\n You win!"
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
    #clock.tick(FPS)
    sleep(0.5)

# Quit Pygame
pygame.quit()
