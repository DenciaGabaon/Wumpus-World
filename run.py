'''Name: Gabaon, Deniece Winslhet A.
   Course & Section: BSCS - 3B
   MP5: WUMPUS WORLD'''

'''run this file to start the game.
 This file will display the main menu of the game
  where you can choose between playing as 
  a human player or an AI player.'''

"""
Copyright © 2024 Gabaon, Deniece Winslhet A.

This code is protected by copyright law. Unauthorized reproduction, distribution,
or modification is prohibited.
"""



import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 300
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wumpus World")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 46, 14)

# Fonts
FONT = pygame.font.Font('assets/font/PixelifySans-Medium.ttf', 30)
bg_img = pygame.image.load("assets/img/bg1.png")
bg_img = pygame.transform.scale(bg_img, (500, 300))

pygame.mixer.init()
gameloop = pygame.mixer.Sound("assets/sounds/gameloop.mp3")  # Replace "breeze_sound.wav" with your actual breeze sound file



def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_button(x, y, width, height, color, text, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw the shadow
    shadow_color = (color[0] // 2, color[1] // 2, color[2] // 2)  # Darker version of the button color
    pygame.draw.rect(SCREEN, shadow_color, (x + 5, y + 5, width, height), border_radius=15)

    if x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height:
        pygame.draw.rect(SCREEN, GRAY, (x, y, width, height), border_radius=15)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(SCREEN, color, (x, y, width, height), border_radius=15)

    draw_text(text, FONT, WHITE, SCREEN, x + width // 2, y + height // 2)
def launch_human_player():
    pygame.quit()
    os.system("python main.py")

def launch_ai_player():
    pygame.quit()
    os.system("python main2.py")

def main():
    while True:
        gameloop.play(-1)
        SCREEN.blit(bg_img, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        button_width = 230
        button_height = 45

        # Calculate the x and y coordinates for the buttons
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y1 = SCREEN_HEIGHT // 2 - button_height - 10  # 10 is the space between the buttons
        button_y2 = SCREEN_HEIGHT // 2 + 10  # 10 is the space between the buttons

        draw_button(button_x, button_y1, button_width, button_height, GREEN, "Human Player", launch_human_player)
        draw_button(button_x, button_y2, button_width, button_height, GREEN, "AI Player", launch_ai_player)

        pygame.display.flip()
if __name__ == "__main__":
    main()
