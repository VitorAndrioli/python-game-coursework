import pygame;
from tile import Tile;
from brick import Brick;

class Menu():
    def __init__(self, message):
        
        self.message = message;
        self.surface = pygame.Surface((1200, 608), 0, 32);
        self.messageSurface = pygame.Surface((1200, 50), 0, 32);
        
        self.image = pygame.image.load("img/titulo.png");
        x = (self.surface.get_width() - self.image.get_width()) / 2;
        y = (self.surface.get_height() - self.image.get_height()) / 2;
        self.surface.blit(self.image, (x, y));
        
        self.menuBlink = 0;
        self.show = True;
        
        self.animationStep = 0;
        self.animationPosition = (0, 0);
        imageAdress = "img/menu_animation.png";
        self.tileSet = Tile(imageAdress, 10, 10);
        self.bricks = [Brick(0, 0, self.tileSet), Brick(1, 1, self.tileSet), Brick(2, 2, self.tileSet), Brick(3, 3, self.tileSet), Brick(4, 4, self.tileSet), Brick(5, 5, self.tileSet), Brick(6, 6, self.tileSet), Brick(7, 7, self.tileSet), Brick(8, 8, self.tileSet)]; 
        self.animationImage = self.bricks[0];
        
    def writeMessage(self):
        pygame.font.init();
        fontObject = pygame.font.SysFont("Arial", 28);
        text = fontObject.render(self.showMessage, True, (255, 255, 255));
        textRect = text.get_rect();
        textRect.centerx = self.messageSurface.get_rect().centerx
        textRect.centery = self.messageSurface.get_rect().centery
        self.messageSurface.blit(text, textRect);
        self.surface.blit(self.messageSurface, (0, 430));
        
        
    def getSurface(self):
        return self.surface;
    
    def update(self):
        self.menuBlink+=1;
        if (self.menuBlink == 300):
            self.messageSurface.fill((0, 0, 0));
            if (self.show):
                self.showMessage = self.message;
                self.show = False;
            else:
                self.showMessage = "";
                self.show = True;
            self.writeMessage();
            self.menuBlink = 0;
            
    def animation(self):
        if (self.stepAnimation < 300):
            self.animationPosition = (self.animationPosition[0], self.animationPosition[0] + 5);
        
        self.animationStep += 1;
            