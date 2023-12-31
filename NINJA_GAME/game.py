import sys
import random
import math
import pygame
from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

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

        self.movement = [0, 0]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'stone': load_images('tiles/stone'),
            'large_decor': load_images('tiles/large_decor'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur = 6),
            'player/run': Animation(load_images('entities/player/run'), img_dur = 4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur = 20, loop = False),
        }

        self.clouds = Clouds(self.assets['clouds'], count = 16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('NINJA_GAME/map.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        self.particles = []

        self.scroll = [0, 0]

        self.running = False
        self.key_time = 0
        self.fast_key_time = 200

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 15
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 15
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity = [-0.1, 0.3], frame = random.randint(0, 20)))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if current_time < self.key_time + self.fast_key_time:
                            self.player.velocity[0] = -3.5
                            if self.running:
                                self.movement[0] = 2
                            else:
                                self.movement[0] = 1
                        else:
                            if self.running:
                                self.movement[0] = 2
                            else:
                                self.movement[0] = 1
                        self.key_time = current_time
                    if event.key == pygame.K_d:
                        if current_time < self.key_time + self.fast_key_time:
                            self.player.velocity[0] = 3.5
                            if self.running:
                                self.movement[1] = 2
                            else:
                                self.movement[1] = 1
                        else:
                            if self.running:
                                self.movement[1] = 2
                            else:
                                self.movement[1] = 1
                        self.key_time = current_time
                    if event.key == pygame.K_w:
                        self.player.velocity[1] = -3
                    if event.key == pygame.K_LSHIFT:
                            self.running = True
                            if self.movement[0] == 1:
                                self.movement[0] = 2
                            else:
                                self.movement[0] = 0
                            if self.movement[1] == 1:
                                self.movement[1] = 2
                            else:
                                self.movement[1] = 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[1] = 0
                    if event.key == pygame.K_LSHIFT:
                        self.running = False
                        if self.movement[0] == 2:
                            self.movement[0] /= 2
                        if self.movement[1] == 2:
                            self.movement[1] /= 2

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()