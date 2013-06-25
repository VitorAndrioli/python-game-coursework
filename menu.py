import pygame;
from tile import Tile;
from brick import Brick;

class Menu():
    def __init__(self, message):
        
        self.message = message;
        self.surface = pygame.Surface((1200, 608), 0, 32);
        self.messageSurface = pygame.Surface((1200, 50), 0, 32);
        
        self.image = pygame.image.load("img/titulo.png");
        
        self.menuBlink = 0;
        self.show = True;
        
        self.bossAnimationStep = 0;
        self.bossAnimationPosition = (2000, 470);
        self.bossCounter = 0;
        self.bossAnimationSpeed = 10;
        imageAdress = "img/boss.png";
        self.bossTileSet = Tile(imageAdress, 125, 129);
        self.bossBricks = [Brick(0, 0, self.bossTileSet), Brick(0, 1, self.bossTileSet), Brick(0, 2, self.bossTileSet)]; 
        
        
        
    def writeMessage(self):
        pygame.font.init();
        fontObject = pygame.font.SysFont("Arial", 28);
        self.showMessage = self.message;
        text = fontObject.render(self.showMessage, True, (255, 255, 255));
        textRect = text.get_rect();
        textRect.centerx = self.messageSurface.get_rect().centerx
        textRect.centery = self.messageSurface.get_rect().centery
        self.messageSurface.blit(text, textRect);
#        self.surface.blit(self.messageSurface, (0, 430));
        
        
    def getSurface(self):
        return self.surface;
    
    def update(self):
        self.surface.fill((0, 0, 0));
        
        x = (self.surface.get_width() - self.image.get_width()) / 2;
        y = (self.surface.get_height() - self.image.get_height()) / 2;
        self.surface.blit(self.image, (x, y));
        
        
        self.menuBlink+=1;
        if (self.menuBlink == 300):
            print self.show;
            self.messageSurface.fill((0, 0, 0));
            if (self.show):
                self.showMessage = self.message;
                self.show = False;
            else:
                self.showMessage = "";
                self.show = True;
            self.writeMessage();
            self.menuBlink = 0;

        self.surface.blit(self.messageSurface, (0, 430));
        
        
        self.bossAnimationStep += 1;
        if (self.bossAnimationStep == self.bossAnimationSpeed):
            self.bossCounter += 1;
            if (self.bossCounter == len(self.bossBricks)):
                self.bossCounter = 0;
            self.bossAnimationStep = 0;
        
        self.bossAnimationPosition = (self.bossAnimationPosition[0] - 2, self.bossAnimationPosition[1]);
        if (self.bossAnimationPosition[0] < -1000):
            self.bossAnimationPosition = (2000, self.bossAnimationPosition[1]);
        bossSprite = pygame.transform.flip(self.bossBricks[self.bossCounter].getImage(), True, False);
        self.surface.blit(bossSprite, (self.bossAnimationPosition[0], self.bossAnimationPosition[1]));
            
            
#    def animation(self):
#        if (self.stepAnimation < 300):
#            self.animationPosition = (self.animationPosition[0], self.animationPosition[0] + 5);
#        
#        self.animationStep += 1;
            