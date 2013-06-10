from brick import Brick;
from tile import Tile;
import Box2D as b2;
import pygame

class Plant():
    def __init__(self, pos, surface, world, PPM):
        #physical variables
        self.width = 96;
        self.height = 75;
        
        #animation variables
        self.counter = 0;
        self.animationSpeed = 300;
        self.animationStep = 0;
        
        self.tile = Tile("img/killer_plant.png", self.width, self.height);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile)];
        self.bricksAttack = [Brick(0, 2, self.tile), Brick(0, 3, self.tile), Brick(0, 3, self.tile)]; 
        
        self.bricks = self.bricksStand;
        
        #drawing variables
        self.PPM = PPM;
        self.surface = surface;
        self.world = world;
        
        #checking variables
        self.attacking = False;
        self.colision = False;
        
        self.createPhysicalBody(pos);
        
            
    def createPhysicalBody(self, pos):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (pos[0]/self.PPM + self.width/2, pos[1]/self.PPM + self.height/2);
        bodyDef.angle = 0;
        bodyDef.type = b2.b2_staticBody;
        self.body = self.world.CreateBody(bodyDef);
    
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.shape = b2.b2PolygonShape( box = (self.width/2, self.height/2) );
        bodyFixture.friction = 0;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture(bodyFixture);
        
    def update(self):
        self.checkColision();
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
                if (self.attacking):
                    self.backToNormal();
            self.animationStep = 0;
        self.render();
        
    def render(self):
        shape = self.body.fixtures[0].shape;
        pixelVertices = [];
        for vertice in shape.vertices:
            v = self.body.transform * vertice * self.PPM;
            pixelVertices.append(v);
            
        pygame.draw.polygon(self.surface, (0, 255, 0), pixelVertices);
        self.surface.blit(self.bricks[self.counter].getImage(), (self.body.position[0] - self.width/2, self.body.position[1] - self.height/2));
        
   
    def checkColision(self):
        if (self.colision):
            self.attack();
            self.colision = False;

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
        
