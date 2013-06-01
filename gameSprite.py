import pygame;

class GameSprite():
    def __init__(self, bricks, pos):
        self.bricks = bricks;
        self.pos = pos;
        self.counter = 0;
        
    def update(self):
        self.rect = self.bricks[self.counter].image.get_rect();
        self.rect = self.rect.move(self.pos[0], self.pos[1]);
        self.counter+=1;
        if (self.counter >= len(self.bricks)):
            self.counter = 0;
            
    def render(self, surface):
        surface.blit(self.bricks[self.counter].getImage(), self.rect);
        
    def setPosition(self, pos):
        self.pos = pos;