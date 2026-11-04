import ctypes
from ctypes import wintypes

import pygame
from pathlib import Path
#set root to current file
Root=Path(__file__).parent
backgroundPath = Root/"Pics"/"MainMenu"/"BackgroundPic.png"
fontPath = Root/"Fonts"/"PressStart2P-Regular.ttf"

# These structures describe how Windows gives us Xbox controller data.
# We don't modify these during the game.
class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", wintypes.WORD),
        ("bLeftTrigger", wintypes.BYTE),
        ("bRightTrigger", wintypes.BYTE),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short),
    ]


class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]


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
# ============================================================
# XBOX CONTROLLER SETUP
# ============================================================


# Load the Windows Xbox controller library
xinput = ctypes.WinDLL("xinput1_4.dll")

# Get the Windows function that reads the controller
XInputGetState = xinput.XInputGetState

XInputGetState.argtypes = [
    wintypes.DWORD,
    ctypes.POINTER(XINPUT_STATE)
]

XInputGetState.restype = wintypes.DWORD


# Xbox button translation values
# These values come from XInput.
DPAD_UP = 0x0001
DPAD_DOWN = 0x0002
DPAD_LEFT = 0x0004
DPAD_RIGHT = 0x0008

START_BUTTON = 0x0010
BACK_BUTTON = 0x0020

LEFT_STICK_BUTTON = 0x0040
RIGHT_STICK_BUTTON = 0x0080

LEFT_BUMPER = 0x0100
RIGHT_BUMPER = 0x0200

A_BUTTON = 0x1000
B_BUTTON = 0x2000
X_BUTTON = 0x4000
Y_BUTTON = 0x8000
# ============================================================
# CREATE CONTROLLER STATE
# ============================================================

# This variable will hold the current Xbox controller state.
controllerState = XINPUT_STATE()


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
    # ========================================================
    # READ XBOX CONTROLLER
    # ========================================================

    # Ask Windows for the current state of Xbox controller 0.
    controllerResult = XInputGetState(
        0,
        ctypes.byref(controllerState)
    )


    # 0 means Windows successfully read the controller.
    if controllerResult == 0:

        # Get the actual controller data.
        gamepad = controllerState.Gamepad


        # ----------------------------------------------------
        # LEFT JOYSTICK
        # ----------------------------------------------------

        leftX = gamepad.sThumbLX
        leftY = gamepad.sThumbLY


        # ----------------------------------------------------
        # RIGHT JOYSTICK
        # ----------------------------------------------------

        rightX = gamepad.sThumbRX
        rightY = gamepad.sThumbRY


        # ----------------------------------------------------
        # TRIGGERS
        # ----------------------------------------------------

        leftTrigger = gamepad.bLeftTrigger
        rightTrigger = gamepad.bRightTrigger


        # ----------------------------------------------------
        # TEMPORARY CONTROLLER TESTING
        # ----------------------------------------------------

        # Left joystick
        if abs(leftX) > 8000 or abs(leftY) > 8000:
            print("Left Stick:", leftX, leftY)

        # Right joystick
        if abs(rightX) > 8000 or abs(rightY) > 8000:
            print("Right Stick:", rightX, rightY)

        # Left trigger
        if leftTrigger > 30:
            print("LEFT TRIGGER:", leftTrigger)

        # Right trigger
        if rightTrigger > 30:
            print("RIGHT TRIGGER:", rightTrigger)

        # A button
        if gamepad.wButtons & A_BUTTON:
            print("A BUTTON")

        # B button
        if gamepad.wButtons & B_BUTTON:
            print("B BUTTON")

        # X button
        if gamepad.wButtons & X_BUTTON:
            print("X BUTTON")

        # Y button
        if gamepad.wButtons & Y_BUTTON:
            print("Y BUTTON")

        # D-pad Up
        if gamepad.wButtons & DPAD_UP:
            print("DPAD UP")

        # D-pad Down
        if gamepad.wButtons & DPAD_DOWN:
            print("DPAD DOWN")

        # D-pad Left
        if gamepad.wButtons & DPAD_LEFT:
            print("DPAD LEFT")

        # D-pad Right
        if gamepad.wButtons & DPAD_RIGHT:
            print("DPAD RIGHT")
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