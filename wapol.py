import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from pygame import Rect;

class Wapol():
    def __init__(self, pos, surface, world, PPM):
        self.width = 80;
        self.height = 80;
        self.widthSprite = 128;
        self.heightSprite = 92;
        self.pos = (pos[0]/PPM, pos[1]/PPM);
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 100;
        
        self.tile = Tile("img/wapol.png", self.widthSprite, self.heightSprite);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), Brick(0, 3, self.tile)];
        self.bricksWalk = [Brick(4, 4, self.tile), Brick(4, 5, self.tile), Brick(4, 6, self.tile), Brick(4, 7, self.tile), Brick(4, 8, self.tile), Brick(4, 9, self.tile), Brick(4, 10, self.tile), Brick(4, 11, self.tile)];
        self.bricks = self.bricksStand;
        
        self.moveRight = False;
        self.moveLeft = False;
        self.right = True;
        
        self.createPhysicalBody();
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_kinematicBody;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "wapol"};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.density = 0;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture( bodyFixture);

    def update(self):
#        self.collision();
  
        if (self.moveRight):
            self.right = True;
            self.bricks = self.bricksWalk;
        elif (self.moveLeft):
            self.right = False;
            self.bricks = self.bricksWalk;
        else:
            self.bricks = self.bricksStand;
        
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
        
        pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
        if (self.right):
            sprite = self.bricks[self.counter].getImage();
        else :
            sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
        
        self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.widthSprite/2, self.body.position[1]*self.PPM - self.heightSprite/2 - 5));
        
    def die(self):
        print "DEATH";
        
#    def collision(self):
#        for contact_edge in self.body.contacts:
#            contact = contact_edge.contact;
#            other = contact.fixtureA.body;
#            otherName = other.userData["name"];
#            if (self.jumping and otherName == "floor"):
#                self.jumping = False;
#                self.animationStep = 0;
#                self.counter = 0;
#                self.bricks = self.bricksStand;
            
        
        
        
        
        