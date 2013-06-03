import pygame;

class GameSprite():
    def __init__(self, bricks, pos):
        self.bricks = bricks;
        self.pos = pos;
        self.counter = 0;
        self.animationSpeed = 2;
        self.animationStep = 0;
        self.right = True;
        self.jumpCounter = 0;
        
    def update(self):
        self.rect = self.bricks[self.counter].image.get_rect();
        self.rect = self.rect.move(self.pos[0], self.pos[1]);
        self.animationStep+=1;
        if (self.animationStep == self.animationSpeed):
            self.counter+=1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
            
            self.animationStep = 0;
    
    def render(self, surface):
        if (self.right):
            sprite = self.bricks[self.counter].getImage();
        else :
            sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
            
        surface.blit(sprite, self.rect);
        
    def setPosition(self, pos):
        self.pos = pos;
        