import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;

class Somersault():
    def __init__(self, pos, surface, world, PPM):

        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.width = 63;
        self.height = 61;
        self.pos = (pos[0]/self.PPM, pos[1]/self.PPM);
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 20;
        self.moveCounter = 0;
        self.deathCounter = 0;
        self.range = 900;
        
        self.tile = Tile("img/rotating.png", self.width, self.height);
        self.bricks = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), 
                       Brick(0, 3, self.tile), Brick(0, 4, self.tile), Brick(0, 5, self.tile),
                       Brick(0, 6, self.tile), Brick(0, 7, self.tile), Brick(0, 8, self.tile)];
        
        self.moveRight = True;
        self.moveLeft = False;
        self.right = True;
        self.dying = False;
        self.dead = False;
        
        self.createPhysicalBody();
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_dynamicBody;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "somersault"};
        
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.density = 17;
        bodyFixture.restitution = 0.7;
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture);
        
    def update(self):
        
        self.collision();
        if (not self.dying):
            
            self.body.ApplyLinearImpulse((1.9, 0), self.body.position, True);
        
#            if (self.moveCounter == self.range):
#                self.walk("left");
#            elif (self.moveCounter == self.range*2):
#                self.walk("right");
#                self.moveCounter = 0;
#        
            self.moveCounter += 1;
        
            self.animationStep += 1;
            if (self.animationStep == self.animationSpeed):
                self.counter += 1;
                if (self.counter == len(self.bricks)):
                    self.counter = 0;
                self.animationStep = 0;
        else:
            if (self.deathCounter == 50):
                self.counter = 1
            elif (self.deathCounter == 70):
                self.world.DestroyBody(self.body);
                self.dead = True;
            self.deathCounter += 1;
            
        self.render();
    
    def walk(self, direction):
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 30;
        if (direction == "right"):
            self.moveRight = True;
            self.moveLeft = False;
            self.right = True;
            vel = 0.5;
        else:
            self.moveRight = False;
            self.moveLeft = True;
            self.right = False;
            vel = -0.5;
                
        self.body.linearVelocity = ((vel, 0));
        
    def render(self):
        if (not self.dead):
            shape = self.body.fixtures[0].shape;
            pixelVertices = [];
            for vertice in shape.vertices:
                v = self.body.transform * vertice * self.PPM;
                pixelVertices.append(v);
            
#            pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
            if (self.right):
                sprite = self.bricks[self.counter].getImage();
            else :
                sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
            
            self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.width/2, self.body.position[1]*self.PPM - self.height/2 - 5));
            
    def die(self, enemy):
        enemy.ApplyForce((0, -10), enemy.position, True);
        self.counter = 0;
        self.bricks = self.bricksDie;
        self.dying = True;
        
    def collision(self):
        
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            if (contact.fixtureA.body.userData["name"] == "somersault"):
                enemy = contact.fixtureB.body;
            else :
                enemy = contact.fixtureA.body;
           
#            if (contact.manifold.localNormal == (0, 1)):
#                self.die(enemy);
#            else:
#                enemy.userData["self"].getHit(10);
#        