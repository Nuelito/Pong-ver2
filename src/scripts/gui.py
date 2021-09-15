import pygame, os, sys
import src.scripts.game as game

pygame.init()
pygame.font.init()

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))

class Label(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0, text="Label", fontPath = 'src/fonts/ariblk.ttf',
                fontSize=14):
        pygame.sprite.Sprite.__init__(self)
        
        #Properties
        self.x, self.y = x,y
        self.color = color
        self.text = text
        
        self.fontPath = fontPath
        self.fontSize = fontSize
        
        #Graphics
        self.font = pygame.font.Font(os.path.join(cwd,fontPath), fontSize)
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def change_text(self, text):
        self.font = pygame.font.Font(os.path.join(cwd,self.fontPath), self.fontSize)
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        
class Button(pygame.sprite.Sprite):
    def __init__(self, color, bgColor=[0,0,0], x=0, y=0, text="Button", fontPath='src/fonts/ariblk.ttf',
                fontSize = 14, width=120, height=32, borderSize=2, innactColor=[0,0,0], hoverColor=[20,20,20],
                pressColor=[125,125,125], parent=None):
                
        pygame.sprite.Sprite.__init__(self)
        
        #Properties
        self.x, self.y = x,y
        self.text = text
        self.borderSize = borderSize
        self.width, self.height = width, height
        self.parent = parent
        
        #Color
        self.color = color
        self.bgColor = bgColor
        self.innactColor = innactColor
        self.hoverColor = hoverColor
        self.pressColor = pressColor
        
        
        
        #Graphics
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
        self.font = pygame.font.Font(os.path.join(cwd,fontPath), fontSize)
        self.iSurf = self.font.render(self.text, True, self.color)
        self.iRect = self.iSurf.get_rect()
        self.iRect.center = [width/2, height/2]
        
        self.image.fill(self.bgColor)
        pygame.draw.rect(self.image, color, [0,0,width, height], borderSize)
        self.image.blit(self.iSurf, self.iRect)
    
    def on_press(self):
        print("Nice pressing my guy")
        
    def resize(self, width, height):
        self.width, self.height = width, height
        self.image = pygame.transform.scale(self.image, [width, height])
        
    def update(self):
        mouse = pygame.mouse
        self.bgColor = self.innactColor
        
        #Getting relative and absolute value
        collideCoords = mouse.get_pos()
        canInteract = True
        if self.parent:
            collideCoords = pygame.Vector2(mouse.get_pos()[0] - self.parent.rect.topleft[0], mouse.get_pos()[1] - self.parent.rect.topleft[1])
            if not self.rect.collidepoint(collideCoords) or not self.parent.rect.collidepoint(mouse.get_pos()): canInteract = False
        
        if canInteract:
            if self.rect.collidepoint(collideCoords): self.bgColor = self.hoverColor
            if mouse.get_pressed()[0] == True and self.rect.collidepoint(collideCoords): self.bgColor = self.pressColor
            for event in game.gameEvents["Mouse Events"]:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.rect.collidepoint(collideCoords): self.on_press()
            
        
        self.image.fill(self.bgColor)
        self.rect.center = [self.x, self.y]
        self.image.blit(self.iSurf, self.iRect)
        pygame.draw.rect(self.image, self.color, [0,0, self.width, self.height], self.borderSize)
        

class List(pygame.sprite.Sprite):
    def __init__(self, color, bgColor=[0,0,0], x=0, y=0, width=120, height=150, borderSize=3):
    
        pygame.sprite.Sprite.__init__(self)
        
        #Properties
        self.x, self.y = x, y
        self.width, self.height = width, height
        
        self.color = color
        self.bgColor = bgColor
        self.borderSize = borderSize
        self.scrollOffset = 0
        self.children = pygame.sprite.Group()
        
        #Graphics
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.center = [self.x, self.y]
        self.image.fill(self.bgColor)
        
        pygame.draw.rect(self.image, color, [0,0,width, height], borderSize)
        
    def add(self, child):
        child.parent = self
        if type(child).__name__ != "Button": return
        child.resize(self.width, int(self.height/5))
        
        child.x = child.width/2
        child.y = child.height/2 + (len(self.children)*(child.height+1))
        self.children.add(child)
        
    def update(self):
        self.image.fill(self.bgColor)
        self.children.draw(self.image)
        
        #Scrolling
        maxOffset = len(self.children)*int(self.height/5) - 30
        for event in game.gameEvents["Mouse Events"]:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()):
                if event.button == 4: self.scrollOffset = max(0, self.scrollOffset - 1*len(self.children))
                if event.button == 5: self.scrollOffset = min(maxOffset, self.scrollOffset + 1*len(self.children))
                
        index = 0        
        for child in self.children:
            child.y = -self.scrollOffset +  child.height/2 + (index*(child.height+1)); index += 1
        
        #print(self.scrollOffset)
        self.children.update()
        pygame.draw.rect(self.image, self.bgColor, [self.width-10,0, self.width, self.height])
        pygame.draw.rect(self.image, self.color, [self.width-10, 4*self.scrollOffset/(len(self.children)+1), 10, 10])
        pygame.draw.rect(self.image, self.color, [self.width-10,0, self.width, self.height], 2)
        pygame.draw.rect(self.image, self.color, [0,0,self.width, self.height], self.borderSize)