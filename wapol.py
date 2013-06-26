import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;

class Wapol():
    def __init__(self, pos, surface, world, PPM, walkingRange):

        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.width = 80;
        self.height = 80;
        self.widthSprite = 128;
        self.heightSprite = 92;
        self.pos = (pos[0]/self.PPM, pos[1]/self.PPM);
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 30;
        self.range = walkingRange;
        self.moveCounter = self.range/2;
        self.deathCounter = 0;
        
        self.tile = Tile("img/wapol.png", self.widthSprite, self.heightSprite);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), Brick(0, 3, self.tile)];
        self.bricksWalk = [Brick(4, 4, self.tile), Brick(4, 5, self.tile), Brick(4, 6, self.tile), Brick(4, 7, self.tile), Brick(4, 8, self.tile), Brick(4, 9, self.tile), Brick(4, 10, self.tile), Brick(4, 11, self.tile)];
        self.bricksDie = [Brick(12, 12, self.tile), Brick(12, 13, self.tile)]
        self.bricks = self.bricksWalk;
        
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
        bodyDef.type = b2.b2_kinematicBody;
        bodyDef.linearVelocity = (0, 0)
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "wapol"};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture);
    
    def update(self):
        
        self.collision();
        if (not self.dying):
            if ((self.moveCounter == self.range) or (self.moveCounter == (self.range + 400 + self.range))):
                self.stopWalking();
            elif (self.moveCounter == (self.range + 400)):
                self.walk("left");
            elif (self.moveCounter == (self.range + 800 + self.range)):
                self.walk("right");
                self.moveCounter = 0;
        
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
    
    def stopWalking(self):
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 70;
        self.moveRight = False;
        self.moveLeft = False;
        self.bricks = self.bricksStand;
        self.body.linearVelocity = ((0, 0));
        
    def walk(self, direction):
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 30;
        self.bricks = self.bricksWalk;
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
            
#            pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
            if (self.right):
                sprite = self.bricks[self.counter].getImage();
            else :
                sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
            
            self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.widthSprite/2, self.body.position[1]*self.PPM - self.heightSprite/2 - 5));
            
    def die(self, enemy):
        enemy.ApplyForce((0, -10), enemy.position, True);
        self.counter = 0;
        self.bricks = self.bricksDie;
        self.dying = True;
        
    def collision(self):
        enemy = None;
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            if (contact.fixtureA.body.userData["name"] == "drake"):
                enemy = contact.fixtureA.body;
            elif (contact.fixtureB.body.userData["name"] == "drake"):
                enemy = contact.fixtureB.body;
            
            if (enemy != None):
                if (contact.manifold.localNormal == (0, 1)):
                    self.die(enemy);
                else:
                    enemy.userData["self"].getHit();
        