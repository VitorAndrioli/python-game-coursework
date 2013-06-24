import pygame;

class Menu():
    def __init__(self, message):
        
        self.message = message;
        self.surface = pygame.Surface((1200, 608), 0, 32);
        self.messageSurface = pygame.Surface((1200, 50), 0, 32);
        
        self.image = pygame.image.load("img/titulo.png");
        x = (self.surface.get_width() - self.image.get_width()) / 2;
        y = (self.surface.get_height() - self.image.get_height()) / 2;
        self.surface.blit(self.image, (x, y));
        
        self.animationStep = 0;
        self.show = True;
        
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
        self.animationStep+=1;
        if (self.animationStep == 300):
            self.messageSurface.fill((0, 0, 0));
            if (self.show):
                self.showMessage = self.message;
                self.show = False;
            else:
                self.showMessage = "";
                self.show = True;
            self.writeMessage();
            self.animationStep = 0;
            