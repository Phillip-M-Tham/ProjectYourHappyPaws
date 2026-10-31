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
#Set Main Menu Background
background = pygame.image.load(".\Pics\MainMenu\BackgroundPic.png").convert()
background = pygame.transform.scale(background, screen.get_size())

pygame.display.set_caption("Project Your Happy Paws")
# CREATE clock
clock = pygame.time.Clock()
# SET running = true
running = True

#start game loop
while running:
    #
    screen.blit(background, (0, 0))
    #set up exit
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    #fix the frame rate to 60
    pygame.display.flip()
    clock.tick(60)
pygame.quit()