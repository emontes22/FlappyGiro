import pygame
import sys
import time
from settings import *
from sprites import BG, Ground


class Game:
    def __init__(self):

        # Initialize Pygame
        pygame.init()

        # Create a display surface with a specific width and height
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Set the window caption
        pygame.display.set_caption('Flappy Bird')

        # Create a clock object to track the framerate
        self.clock = pygame.time.Clock()

        #Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Scale factor
        bg_height = pygame.image.load('./Graphics/Environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        #Sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground(self.all_sprites, self.scale_factor)

    def run(self):
        # Track the last recorded time
        last_time = time.time()

        while True:

            # Calculate the time difference between the current time and the last recorded time
            dt = time.time() - last_time
            last_time = time.time()

            # Event loop to handle user input and window events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #Game Logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            # Update the display to show any changes
            pygame.display.update()

            # Control the frame rate of the game
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
