import sys
import time
import pygame
from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()

        SCREEN_WIDTH = 640
        SCREEN_HEIGHT = 480

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Ninja Game')
        pygame.display.set_icon(load_image('shuriken-icon.png'))
        self.display = pygame.Surface((320, 240))
        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'stone': load_images('tiles/stone'),
            'large_decor': load_images('tiles/large_decor'),
            'player': load_image('entities/player.png') 
        }

        self.player = PhysicsEntity(self, 'player', (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)

        self.key_time = 0
        self.fast_key_time = 200

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            self.display.fill((135, 206, 235))
            
            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if current_time < self.key_time + self.fast_key_time:
                            self.player.velocity[0] = -3.5
                        else:
                            self.movement[0] = 1
                        self.key_time = current_time
                    if event.key == pygame.K_d:
                        if current_time < self.key_time + self.fast_key_time:
                            self.player.velocity[0] = 3.5
                        else:
                            self.movement[1] = 1
                        self.key_time = current_time
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_LSHIFT:
                        self.movement[0] *= 2
                        self.movement[1] *= 2
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[1] = 0
                    # if event.key == pygame.K_LSHIFT:
                    #     self.movement[0] /= 2
                    #     self.movement[1] /= 2

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()