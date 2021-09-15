import pygame, os, sys
import src.scripts.game as game

pygame.init()

cFolder = os.path.dirname(os.path.realpath(sys.argv[0]))
full_path = os.path.join(cFolder, "src\\sfx\\Wall_Hit.ogg")
wallHit = pygame.mixer.Sound(full_path)
wallHit.set_volume(.1)

full_path = os.path.join(cFolder, "src\\sfx\\Paddle_Hit.ogg")
paddleHit = pygame.mixer.Sound(full_path)
paddleHit.set_volume(.1)

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0, spd=5, uKey = pygame.K_w, dKey = pygame.K_s):
        pygame.sprite.Sprite.__init__(self)
        
        #Properties
        self.x = x
        self.y = y
        self.spd = 5
        
        #Controls
        self.uKey = uKey
        self.dKey = dKey
        
        #Graphics
        self.image = pygame.Surface([25,120])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
    def move_up(self): self.y -= self.spd
    def move_down(self): self.y += self.spd
        
    def update(self):
        keys = pygame.key.get_pressed()
        self.y += keys[self.uKey] * -self.spd or keys[self.dKey] * self.spd
        
        #Boundaries
        if self.y - 60 < 0: self.y = 60
        if self.y + 60 > 600: self.y = 540
    
        self.rect.center = [self.x, self.y]

        
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, x=0, y=0, vel_x=0, vel_y=0):
        pygame.sprite.Sprite.__init__(self)
        
        #Properties
        self.x = x
        self.y = y
        
        self.vel_x = vel_x
        self.vel_y = vel_y
        
        #Graphics
        self.image = pygame.Surface([26,26], pygame.SRCALPHA)
        
        pygame.draw.circle(self.image, color, [13,13], 13)
        self.rect = self.image.get_rect()
        
        self.rect.center = [x, y]
        
    def on_right(self):pass
    def on_left(self):pass
        
    def update(self):
        #Boundaries & Collision
        if self.y + 13 > 600: self.y = 587;self.vel_y *= -1; wallHit.play()
        elif self.y - 13 < 0: self.y = 13;self.vel_y *= -1; wallHit.play()
        
        #Score change
        if self.x + 13 < 0: self.on_left()
        elif self.x -13 > 900: self.on_right()
        for obj in game.gGroup:
            if type(obj).__name__ == "Paddle":
                if obj != self and obj.rect.colliderect(self):
                    if obj.rect.centerx < 450: 
                        self.x = obj.rect.centerx + obj.image.get_size()[0]/2 + 13
                        self.vel_x *= -1; paddleHit.play()
                            
                    else:
                        self.x =  obj.rect.centerx - obj.image.get_size()[0]/2 - 13
                        self.vel_x *= -1; paddleHit.play()
    
    
        #Coords update
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = [self.x, self.y]
        
        
class Net(pygame.sprite.Sprite):
    def __init__(self, color):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([900, 600], pygame.SRCALPHA)
        
        for i in range(0,5):
            child = pygame.Surface([15,55])
            child.fill(color)
            rect = child.get_rect()
            rect.centerx = 450
            rect.y = 120*i+ 25
            
            self.image.blit(child, rect)
            
        self.rect = self.image.get_rect()