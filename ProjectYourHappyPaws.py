import pygame
from pathlib import Path
#set root to current file
Root=Path(__file__).parent
backgroundPath = Root/"Pics"/"MainMenu"/"BackgroundPic.png"
fontPath = Root/"Fonts"/"PressStart2P-Regular.ttf"

def setMainMenu():
    #set background pic to main menu pic
    background = pygame.image.load(backgroundPath).convert()
    background = pygame.transform.scale(background, screen.get_size())

    #Set font
    menuFont = pygame.font.Font(fontPath,45)
    #Set Title
    titleFont = pygame.font.Font(fontPath, 75)
    titleText= titleFont.render("YOUR HAPPY PAWS",True,"White")
    titleTextRect=titleText.get_rect( center=(screenWidth // 2, 100))

    #setStartButton
    # Create text FIRST
    startText = menuFont.render("START GAME", True, "white")
    startTextWidth = startText.get_width()

    # Create button using that width + padding
    startButton = pygame.Rect(0, 0, startTextWidth + 60, 70)
    # Position button
    startButton.center = (screenWidth // 2, screenHeight // 2)
    # Position text inside button
    startTextRect = startText.get_rect(center=startButton.center)

    #setOptionButton
    optionText = menuFont.render("OPTIONS", True, "white")
    optionTextWidth= optionText.get_width()
    optionButton=pygame.Rect(0,0,optionTextWidth+60,70)
    optionButton.center = (startButton.centerx, startButton.centery + 90)
    optionTextRect= optionText.get_rect(center=optionButton.center)
    
    #setQuit Button
    quitText = menuFont.render("QUIT", True, "white")
    quitButton=pygame.Rect(0,0,300,70)
    quitButton.center = (startButton.centerx,startButton.centery + 180)
    quitTextRect= quitText.get_rect(center=quitButton.center)

    return background,startButton,optionButton,quitButton,menuFont,startText,startTextRect,optionText,optionTextRect,quitText,quitTextRect,titleText,titleTextRect


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
background,startBtn,optionBtn,quitBtn,menuFont,startText,startTextRect,optionText,optionTextRect,quitText,quitTextRect,titleText,titleTextRect=setMainMenu()
#Set Main Menu Background
mainMenu=True
pygame.display.set_caption("Project Your Happy Paws")
# CREATE clock
clock = pygame.time.Clock()
# SET running = true
running = True

#start game loop
while running:
    
    screen.blit(background, (0, 0))
    #run this if we are using the main menu
    if mainMenu == True:
        #draw Title
        screen.blit(titleText,titleTextRect)
        #draw start button
        pygame.draw.rect(screen,"black",startBtn)
        screen.blit(startText, startTextRect)
        
        #draw option button
        pygame.draw.rect(screen,"black",optionBtn)
        screen.blit(optionText, optionTextRect)
        #draw exit button
        pygame.draw.rect(screen,"black",quitBtn)
        screen.blit(quitText, quitTextRect)
    #set up exit
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    #Draw the updated screen
    pygame.display.flip()
    #fix the frame rate to 60
    clock.tick(60)
pygame.quit()