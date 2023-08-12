# import the pygame module
import pygame

# initialize pygame
pygame.init()

# set screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# render screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# establish player character
player = pygame.Rect((300, 250, 50, 50))

# create game loop
run = True
while run:

    # update with black screen to erase trails
    screen.fill((0, 0, 0))

    # drawing the player rectangle
    pygame.draw.rect(screen, (255, 0, 0), player)

    # search for key inputs
    key = pygame.key.get_pressed()

    # basic wasd movement
    if key[pygame.K_w] == True:
        player.move_ip(0, -1)
    elif key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)

    # establish event handler
    for event in pygame.event.get():

        # check for closing window
        if event.type == pygame.QUIT:
            run = False
    
    #force update the game for each loop iteration
    pygame.display.update()

# quit pygame
pygame.quit()