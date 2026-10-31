import pygame

# INITIALIZE pygame
pygame.init()
# init the joysticks
pygame.joystick.init()

# Set up controller input
controllerCount = pygame.joystick.get_count()

print("Controllers detected:", controllerCount)

# SET screen width
#DEBUG MODE
screen = pygame.display.set_mode((1280, 720))
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

screenWidth=screen.get_width()
# SET screen height
screenHeight=screen.get_height()
# CREATE game window
pygame.display.set_caption("Project Your Happy Paws")
# CREATE clock
clock = pygame.time.Clock()
# SET running = true
running = True

#start game loop
while running:
    #set up exit
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
pygame.quit()