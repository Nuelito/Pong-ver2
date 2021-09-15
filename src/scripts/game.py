import pygame, sys
import src.scripts.setup as setup
from src.scripts.Bodies import *

pygame.init()

#Game properties
screen = pygame.display.set_mode([900, 600])
clock = pygame.time.Clock()

#Variables
running = True
paused = False
scenes = ["Game", "Menu", "Settings", "Ended"]
currentScene = scenes[0]

#Scenes
gGroup = pygame.sprite.Group() #Game objects
mGroup = pygame.sprite.Group() #Menu objects
sGroup = pygame.sprite.Group() #Settings objects

def menu():
    global currentScene, paused
    
    currentScene = scenes[1]
    paused = False
    
    mGroup.add(setup.menuGui)
    
def settings():
    global currentScene
    currentScene = scenes[2]
    sGroup.add(setup.settingsGui)
    
def play():
    global currentScene
    
    setup.winSound.stop(); setup.dissapSound.stop()
    currentScene = scenes[0]
    
    setup.timer = setup.maxTime
    setup.gameGui[2].change_text(str(int(setup.timer)))
    #Game components
    net = Net(color=[255,255,255])
    p1 = Paddle(color=[255,255,255], x=80, y=300)
    p2 = Paddle(color=[255,255,255], x=820, y=300, uKey = pygame.K_KP8, dKey = pygame.K_KP5)
    
    #Stiff
    point1, point2 = 0,0
    
    #Setting up the ball
    def on_right():
        nonlocal point2
        ball.x = 450; point2 += 1
        setup.score_right(point2)
        if point2 >= setup.maxScore: setup.winSound.play(); endGame("Player 2")
        
    def on_left():
        nonlocal point1
        ball.x = 450; point1 += 1
        setup.score_left(point1)
        if point1 >= setup.maxScore: setup.winSound.play(); endGame("Player 1")
        
    ball = Ball(color=[255,255,255], x=450, y=300, vel_x=-4, vel_y=4)
    ball.on_right, ball.on_left = on_right, on_left
    
    gGroup.add(p1, p2, ball, net, setup.gameGui) #Setting up the scene
    
def pause(value): 
    global paused; paused = value
    
    if paused: gGroup.add(setup.pauseGui[0]); setup.pauseSound.play()
    else: gGroup.remove(setup.pauseGui[0]); setup.pauseSound.stop()
    
def draw_screen():
    screen.fill([0,0,0])
    mGroup.draw(screen); gGroup.draw(screen); sGroup.draw(screen) #Drawing
    
def endGame(txt):
    global currentScene
    currentScene = scenes[3]
    
    setup.pauseGui[1].change_text(txt+" wins!")
    gGroup.add(setup.pauseGui[1])

gameEvents = {
    "Key Events" : [],
    "Mouse Events" : []
}

def run():
    settings()
    while running:
        gameEvents["Mouse Events"] = []
        gameEvents["Key Events"] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if setup.fading: setup.fading = False; break
            gameEvents["Key Events"].append(event)
            if event.type == pygame.KEYDOWN:
                #Changing scenes
                if event.key == pygame.K_SPACE: 
                    if currentScene == scenes[0]: pause(not paused) # Pausing
                    elif currentScene == scenes[1]: setup.changeScene(play)
                    elif currentScene == scenes[3]: setup.changeScene(play)
                    
                if event.key == pygame.K_ESCAPE and currentScene != scenes[1]:
                    setup.pauseSound.stop(); setup.changeScene(menu)
                    
                if event.key == pygame.K_s and currentScene == scenes[1]:
                    setup.changeScene(settings)
                    
            if event.type == pygame.MOUSEBUTTONUP: gameEvents["Mouse Events"].append(event)
            if event.type == pygame.MOUSEBUTTONDOWN: gameEvents["Mouse Events"].append(event)
        
        draw_screen()
        clock.tick(60)
        
        if not paused and currentScene is scenes[0]:
            setup.gameGui[2].change_text(str(int(round(setup.timer, 0))))
            setup.timer = max(0, setup.timer - 1/60); gGroup.update()
            if setup.timer == 0:
                if int(setup.gameGui[0].text) == int(setup.gameGui[1].text): setup.dissapSound.play(); endGame("Nobody")
                else:
                    if int(setup.gameGui[0].text) > int(setup.gameGui[1].text): setup.dissapSound.play(); endGame("Player 1")
                    else: endGame("Player 2")
            
        if not paused and currentScene is scenes[2]: sGroup.update()
        pygame.display.update()