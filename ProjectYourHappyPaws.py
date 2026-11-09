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

def fitText(text, fontPath, maxFontSize, maxWidth):

    fontSize = maxFontSize
    font = pygame.font.Font(fontPath, fontSize)

    while font.size(text)[0] > maxWidth:
        fontSize -= 1
        font = pygame.font.Font(fontPath, fontSize)

    return font

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
#
selectedButton=0
dpadPressedVertical = False
dpadPressedHorizontal=False
aButtonPressed=False
bButtonPressed=False


options=False
outOfOrderText1 = menuFont.render("Out of Order", True, "white")
outOfOrderText2 = menuFont.render("Press B to back out!", True, "white")
outOfOrderSign=pygame.Rect(0,0,1000,500)
outOfOrderSign.center=(screenWidth // 2, screenHeight // 2)

gameMode=False
gauntletText = menuFont.render("Gauntlet",True,"white")
levelSelectText = menuFont.render("Level Select",True,"white")
gameModeBtnWidth=max(gauntletText.get_width(),levelSelectText.get_width())+60
guantletBtn= pygame.Rect(0,0,gameModeBtnWidth,70)
levelSelectBtn= pygame.Rect(0,0,gameModeBtnWidth,70)
guantletBtn.center=(startBtn.centerx, startBtn.centery)
levelSelectBtn.center=(startBtn.centerx, startBtn.centery + 90)
guantletTextRect=gauntletText.get_rect(center=guantletBtn.center)
levelSelectTextRect=levelSelectText.get_rect(center=levelSelectBtn.center)

characterSelect=False
#char select font scale
availableWidth = int(screenWidth * 0.90)
gap = 20

charBtnWidth = (availableWidth - (2 * gap)) // 3
charBtnHeight = 70

rowStart = (screenWidth - availableWidth) // 2

char1Btn = pygame.Rect(rowStart, 0, charBtnWidth, charBtnHeight)
char2Btn = pygame.Rect(rowStart + charBtnWidth + gap, 0, charBtnWidth, charBtnHeight)
char3Btn = pygame.Rect(rowStart + (charBtnWidth + gap) * 2, 0, charBtnWidth, charBtnHeight)

char1Btn.centery = startBtn.centery
char2Btn.centery = startBtn.centery
char3Btn.centery = startBtn.centery

textWidth = charBtnWidth - 30

char1Font = fitText("Elsa", fontPath, 50, textWidth)
char2Font = fitText("Hugh's Char", fontPath, 50, textWidth)
char3Font = fitText("Yaun-Shuo's Char", fontPath, 50, textWidth)

selectedCharacter=0
#char 0,1,2 for 3 characters

char1Text = char1Font.render("Elsa", True, "white")
char2Text = char2Font.render("Hugh's Char", True, "white")
char3Text = char3Font.render("Yaun-Shuo's Char", True, "white")

char1TextRect=char1Text.get_rect(center=char1Btn.center)
char2TextRect=char2Text.get_rect(center=char2Btn.center)
char3TextRect=char3Text.get_rect(center=char3Btn.center)


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
            #Quit Action
            if(aButtonPressed ==False):
                if(mainMenu==True and selectedButton==2):
                    running = False
                elif(mainMenu==True and selectedButton==1):
                    options=True
                elif(mainMenu==True and selectedButton==0):
                    gameMode=True
                    selectedButton=3
                elif(gameMode==True and selectedButton==3):
                    gameMode=False
                    characterSelect=True
                    selectedCharacter=0
                aButtonPressed=True
        else:
            aButtonPressed=False

        # B button
        if gamepad.wButtons & B_BUTTON:
            print("B BUTTON")
            if(bButtonPressed==False):
                if options==True:
                    options=False
                elif gameMode==True:
                    selectedButton=0
                    gameMode=False
                elif characterSelect==True:
                    characterSelect=False
                    gameMode=True
                    selectedButton=3
                elif mainMenu==True:
                    selectedButton=0
                bButtonPressed=True
        else:
            bButtonPressed=False

        # X button
        if gamepad.wButtons & X_BUTTON:
            print("X BUTTON")

        # Y button
        if gamepad.wButtons & Y_BUTTON:
            print("Y BUTTON")

        # D-pad Up
        if gamepad.wButtons & DPAD_UP:
            print("DPAD UP")
            if mainMenu==True and gameMode==False and dpadPressedVertical==False:
                selectedButton = selectedButton-1
                if selectedButton < 0:
                    selectedButton=2
                dpadPressedVertical=True
            elif gameMode==True and dpadPressedVertical==False:
                if selectedButton==3:
                    selectedButton=4
                else:
                    selectedButton=3
                dpadPressedVertical=True
        # D-pad Down
        elif gamepad.wButtons & DPAD_DOWN:
            print("DPAD DOWN")
            if mainMenu==True and gameMode==False and dpadPressedVertical==False:
                selectedButton +=1
                if selectedButton >2:
                    selectedButton=0
                dpadPressedVertical=True
            elif gameMode==True and dpadPressedVertical==False:
                if selectedButton==3:
                    selectedButton=4
                else:
                    selectedButton=3
                dpadPressedVertical=True
        else:
            dpadPressedVertical=False

        # D-pad Left
        if gamepad.wButtons & DPAD_LEFT:
            print("DPAD LEFT")
            if characterSelect==True and dpadPressedHorizontal==False:
                selectedCharacter =selectedCharacter-1
                if selectedCharacter <0:
                    selectedCharacter=2
                dpadPressedHorizontal=True
        # D-pad Right
        elif gamepad.wButtons & DPAD_RIGHT:
            print("DPAD RIGHT")
            if characterSelect==True and dpadPressedHorizontal==False:
                selectedCharacter +=1
                if selectedCharacter >2:
                    selectedCharacter=0
                dpadPressedHorizontal =True
        else:
            dpadPressedHorizontal=False
    screen.blit(background, (0, 0))
    #run this if we are using the main menu
    if mainMenu == True and options==False and gameMode==False and characterSelect==False:
        #draw Title
        screen.blit(titleText,titleTextRect)
        #draw start button
        
        if selectedButton==0:
            pygame.draw.rect(screen, "gray", startBtn)
        else:
            pygame.draw.rect(screen,"black",startBtn)
        
        screen.blit(startText, startTextRect)
        
        #draw option button
        if selectedButton==1:
            pygame.draw.rect(screen,"gray",optionBtn)
        else:
            pygame.draw.rect(screen,"black",optionBtn)
        screen.blit(optionText, optionTextRect)
        #draw exit button
        if selectedButton==2:
            pygame.draw.rect(screen,"gray",quitBtn)
        else:
            pygame.draw.rect(screen,"black",quitBtn)
        screen.blit(quitText, quitTextRect)

        #selectedButton=0 Start
        #selectedButton=1 Options
        #selectdButton=2 Quit
    #run this if using options
    elif options==True:
        pygame.draw.rect(screen,"gray",outOfOrderSign)
        
        text1Rect = outOfOrderText1.get_rect(center=(outOfOrderSign.centerx, outOfOrderSign.centery - 45))

        text2Rect = outOfOrderText2.get_rect(center=(outOfOrderSign.centerx, outOfOrderSign.centery + 45))

        screen.blit(outOfOrderText1, text1Rect)
        screen.blit(outOfOrderText2, text2Rect)
    elif gameMode==True and characterSelect==False:
        #selectedButton=3 Gauntlet
        #selectdButton=4 Level Select

        if selectedButton==3:
            pygame.draw.rect(screen, "gray", guantletBtn)
        else:
            pygame.draw.rect(screen,"black",guantletBtn)
        screen.blit(gauntletText, guantletTextRect)

        if selectedButton==4:
            pygame.draw.rect(screen, "gray", levelSelectBtn)
        else:
            pygame.draw.rect(screen,"black",levelSelectBtn)
        screen.blit(levelSelectText, levelSelectTextRect)
    elif characterSelect==True:
        if selectedCharacter==0:
            pygame.draw.rect(screen,"grey",char1Btn)
        else:
            pygame.draw.rect(screen,"black",char1Btn)
        screen.blit(char1Text, char1TextRect)

        if selectedCharacter==1:
            pygame.draw.rect(screen,"gray",char2Btn)
        else:
            pygame.draw.rect(screen,"black",char2Btn)
        screen.blit(char2Text, char2TextRect)

        if selectedCharacter==2:
            pygame.draw.rect(screen,"gray",char3Btn)
        else:
            pygame.draw.rect(screen,"black",char3Btn)
        screen.blit(char3Text, char3TextRect)

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