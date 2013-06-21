from brick import Brick;
from tile import Tile;
import Box2D as b2;
import pygame;

class Chopperman():
    def __init__(self, pos, surface, world, PPM):
        
        self.width = 50;
        self.height = 45;
        self.pos = (pos[0]/PPM, pos[1]/PPM);
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 100;
        
        self.tile = Tile("img/chopperman.png", self.width, self.height);
        self.bricks = [Brick(0, 0, self.tile), Brick(1, 1, self.tile), Brick(2, 2, self.tile), Brick(3, 3, self.tile)];
        
        self.PPM = PPM;
        self.surface = surface;
        self.world = world;
        
        self.createPhysicalBody();
        
        self.up = True;
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = self.pos;
        bodyDef.angle = 0;
        bodyDef.type = b2.b2_kinematicBody;
        self.body = self.world.CreateBody( bodyDef );
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.density = 1;
        bodyFixture.friction = 0;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture(bodyFixture);
        
    def update(self):
        #self.body.position = (self.body.position[0] + 5, self.body.position[1] + self.highValue);
        
        self.body.ApplyForce((10, 0), self.body.position, True);
        
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
            self.animationStep = 0;
        self.render();
    
    def render(self):
        shape = self.body.fixtures[0].shape;
        pixelVertices = [];
        for vertice in shape.vertices:
            v = self.body.transform * vertice * self.PPM;
            pixelVertices.append(v);
            
        pygame.draw.polygon(self.surface, (255, 0, 0), pixelVertices);
        self.surface.blit(self.bricks[self.counter].getImage(), (self.body.position[0]*self.PPM - self.width/2, self.body.position[1]*self.PPM - self.height/2));
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
        