import sys

# import the pygame module
import pygame

class Game:
    def __init__(self):

        # initialize pygame
        pygame.init()

        # set screen width and height
        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        # change caption for game window
        pygame.display.set_caption('Basic Pygame Scripts')

        # render screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # adding clock to force 60 fps game
        self.clock = pygame.time.Clock()

        # establish player character
        self.player = pygame.Rect((300, 250, 50, 50))

    def run(self):
        # create game loop
        while True:

            # update with black screen to erase trails
            self.screen.fill((0, 0, 0))

            # drawing the player rectangle
            pygame.draw.rect(self.screen, (255, 0, 0), self.player)

            # search for key inputs
            key = pygame.key.get_pressed()

            # basic wasd movement
            if key[pygame.K_w] == True:
                self.player.move_ip(0, -1)
            elif key[pygame.K_a] == True:
                self.player.move_ip(-1, 0)
            elif key[pygame.K_s] == True:
                self.player.move_ip(0, 1)
            elif key[pygame.K_d] == True:
                self.player.move_ip(1, 0)

            # establish event handler
            for event in pygame.event.get():

                # check for closing window and quit both pygame and app
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # force update the game for each loop iteration
            pygame.display.update()

            # enable the fps limit
            self.clock.tick(60)

Game().run()