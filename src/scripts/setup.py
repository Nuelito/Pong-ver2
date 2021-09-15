import pygame, os, sys

from src.scripts.gui import *
import src.scripts.game as game

pygame.init()

fading = False
maxScore = 2
maxTime = 60
timer = maxTime

#Sounds
cFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
winPath = os.path.join(cFolder, "src\\sfx\\Win.ogg")
pausePath = os.path.join(cFolder, "src\\sfx\\Pause.ogg")
dissapPath = os.path.join(cFolder, "src\\sfx\\Dissapointment.ogg")

winSound = pygame.mixer.Sound(winPath)
pauseSound = pygame.mixer.Sound(pausePath)
dissapSound = pygame.mixer.Sound(dissapPath)

winSound.set_volume(.05); pauseSound.set_volume(.01); dissapSound.set_volume(.05)

#Pause objects
pauseGui = [
    Label(text="Paused", color=[255,255,255], x=450, y=230, fontSize=25),
    Label(text="Nobody wins!", color=[255,255,255], x=450, y=230, fontSize=25)
]

#Score
gameGui = [
    Label(text="0", color=[255,255,255], x=230, y=100, fontSize=110, fontPath= "src/fonts/Roboto-Bold.ttf"),
    Label(text="0", color=[255,255,255], x=670, y=100, fontSize=110, fontPath= "src/fonts/Roboto-Bold.ttf"),
    Label(text="", color=[255,255,255], x=450, y=114, fontSize=25) # Timer
]

menuGui = [
    Label(text="Pong", color=[255,255,255], x=450, y=140, fontSize=130),
    Label(text="Onuelito's Edition", color=[255,255,255], x=450, y=240, fontSize=20),
    Label(text="Press 'space' to start", color=[255,255,255], x= 450, y=450, fontSize=18),
    Label(text="Press 's' for settings", color=[255,255,255], x= 450, y = 480, fontSize=12)
]

settingsGui = [
    Label(text="Settings", color=[255,255,255], x = 450, y =100, fontSize=50),
    Button(color=[255,255,255], x=450, y=300, fontSize=20),
    List(color=[255,255,255], x=450, y=400)
]


for x in range(0, 100):
    bttn = Button(text=str(x), color=[255,255,255], borderSize=3)
    bttn.on_press = lambda: print(bttn.text)
    settingsGui[2].add(bttn)

def score_left(txt): gameGui[1].change_text(str(txt))
def score_right(txt): gameGui[0].change_text(str(txt))

def changeScene(scene):
    global fading; fading = True
    fade = pygame.Surface([900,600])
    fade.fill([0,0,0])
    for i in range(0,130):
        fade.set_alpha(i*2)
        game.draw_screen()
        game.screen.blit(fade, (0,0))
        
        pygame.time.delay(1)
        pygame.display.update()
    
    #Reseting the score
    gameGui[0].change_text("0")
    gameGui[1].change_text("0")
    
    game.gGroup.empty()
    game.mGroup.empty()
    game.sGroup.empty()
    scene()
    fade.fill([0,0,0])
    
    for i in range(0,130):
        fade.set_alpha(255-i*2)
        game.draw_screen()
        game.screen.blit(fade, (0,0))
        pygame.time.delay(1)
        pygame.display.update()