import pygame;
from tile import Tile;
from brick import Brick;

#Classe para cria o Menu inicial e o de Pause

class Menu():
    def __init__(self, initialMenu):
        
        if (initialMenu):
            message = "Click enter to start";
        else:
            message = "Click enter to continue";
        self.message = message;
        
        self.surface = pygame.Surface((1200, 608), 0, 32);
        
        self.image = pygame.image.load("img/titulo.png");
        
        self.menuBlink = 0;
        self.show = True;
        
        #Variaveis para nimacao do personagem Boss no menu
        self.bossAnimationStep = 0;
        self.bossAnimationPosition = (2000, 470);
        self.bossCounter = 0;
        self.bossAnimationSpeed = 10;
        imageAdress = "img/boss.png";
        self.bossTileSet = Tile(imageAdress, 125, 129);
        self.bossBricks = [Brick(0, 0, self.bossTileSet), Brick(0, 1, self.bossTileSet), Brick(0, 2, self.bossTileSet)]; 
        
        #Variaveis para nimacao do personagem Drake no menu
        self.drakeAnimationStep = 0;
        self.drakeAnimationPosition = (3000, 380);
        self.drakeCounter = 0;
        self.drakeAnimationSpeed = 10;
        self.drakeAnimationCounter = 0;
        imageAdress = "img/dino.png";
        self.drakeTileSet = Tile(imageAdress, 340, 209);
        self.drakeBricksStand = [Brick(0, 17, self.drakeTileSet), Brick(0, 18, self.drakeTileSet)];
        self.drakeBricksRun = [Brick(0, 11, self.drakeTileSet), Brick(0, 12, self.drakeTileSet), Brick(0, 13, self.drakeTileSet),
                               Brick(0, 14, self.drakeTileSet), Brick(0, 15, self.drakeTileSet), Brick(0, 16, self.drakeTileSet)];
        self.drakeBricks = self.drakeBricksRun;

    def writeMessage(self):
        pygame.font.init();
        fontObject = pygame.font.SysFont("Arial", 28);
        if (self.show):
            self.showMessage = self.message;
        else:
            self.showMessage = "";
            
        text = fontObject.render(self.showMessage, True, (255, 255, 255));
        
        #centralizar texto na tela
        textRect = text.get_rect();
        textRect.centerx = self.surface.get_rect().centerx
        textRect.centery = self.surface.get_rect().centery + 170
        self.surface.blit(text, textRect);
        
    def getSurface(self):
        return self.surface;
    
    def update(self, gameSurface):
        #Limpa a tela da imagem e da mensagem
        self.surface.fill((0, 0, 0));
        
        #centraliza a imagem
        x = (self.surface.get_width() - self.image.get_width()) / 2;
        y = (self.surface.get_height() - self.image.get_height()) / 2;
        
        #pisca a mensagem
        if (self.menuBlink == 70):
            self.show = not self.show;
            self.menuBlink = 0;
        else:
            self.menuBlink+=1;
        
        #Animacao do personagem Boss do menu
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
        
        #Animacao do personagem Drake do menu
        self.drakeAnimationStep += 1;
        if (self.drakeAnimationStep == self.drakeAnimationSpeed):
            self.drakeCounter += 1;
            if (self.drakeCounter == len(self.drakeBricks)):
                self.drakeCounter = 0;
            self.drakeAnimationStep = 0;
        
        self.drakeAnimationPosition = (self.drakeAnimationPosition[0] - 2.5, self.drakeAnimationPosition[1]);
        if (self.drakeAnimationPosition[0] < -1000):
            self.drakeAnimationPosition = (2500, self.drakeAnimationPosition[1]);
        drakeSprite = pygame.transform.flip(self.drakeBricks[self.drakeCounter].getImage(), True, False);
        
        #Junta todos os elementos na surface do menu        
        self.surface.blit(self.image, (x, y));
        self.surface.blit(bossSprite, (self.bossAnimationPosition[0], self.bossAnimationPosition[1]));
        self.surface.blit(drakeSprite, (self.drakeAnimationPosition[0], self.drakeAnimationPosition[1]));
        self.writeMessage()
        
        #cola a surface do menu na tela do jogo
        gameSurface.blit(self.surface, (0, 0));    