import pygame
import sys
import time
from settings import *
from sprites import BG, Ground, Plane, Obstacle


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
        self.active = True

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Scale factor
        bg_height = pygame.image.load(
            './Graphics/Environment/background.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # Sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.9)

        # Timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Text
        self.font = pygame.font.Font(
            './Graphics/Font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # Menu
        self.menu_surf = pygame.image.load(
            './Graphics/UI/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Music
        self.music = pygame.mixer.Sound('./Sounds/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)
        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(
                            self.all_sprites, self.scale_factor / 1.9)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites],
                             self.scale_factor * 1.1)

            # Game Logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            # Update the display to show any changes
            pygame.display.update()

            # Control the frame rate of the game
            self.clock.tick(FRAMERATE)


if __name__ == '__main__':
    game = Game()
    game.run()
