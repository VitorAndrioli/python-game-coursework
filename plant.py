from brick import Brick;
from tile import Tile;

class Plant():
    def __init__( self, pos, surface ):
        self.pos = pos;
        self.tile = Tile("img/killer_plant.png", 96, 85);
        self.counter = 0;
        self.animationSpeed = 9;
        self.animationStep = 0;
        self.surface = surface;
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile)];
        self.bricksAttack = [Brick(0, 2, self.tile), Brick(0, 3, self.tile), Brick(0, 3, self.tile)]; 
        self.bricks = self.bricksStand;
        self.attacking = False;
        
    def attack(self):
        self.counter = 0;
        self.animationStep = 0;
        self.bricks = self.bricksAttack;
        self.attacking = True;
        self.animationSpeed = self.animationSpeed / 3;
        
    def backToNormal(self):
        self.animationStep = 0;
        self.bricks = self.bricksStand;
        self.animationSpeed = self.animationSpeed * 3;
        self.attacking = False;
        
    def update( self ):
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
                if (self.attacking):
                    self.backToNormal();
            self.animationStep = 0;
        self.render();
        
    def render( self ):
        self.surface.blit(self.bricks[self.counter].getImage(), self.pos);
        
        
        