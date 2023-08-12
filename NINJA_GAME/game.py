import sys
import pygame

class Game:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        pygame.display.set_caption('Ninja Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.clock.tick(60)

Game().run()