import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from rotating import Somersault;

class Boss():
    def __init__(self, pos, surface, world, PPM, mobList):

        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.width = 125;
        self.height = 129;
        self.pos = (pos[0]/self.PPM, pos[1]/self.PPM);
        self.life = 200;
        self.mobList = mobList;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 20;
        self.moveCounter = 0;
        self.deathCounter = 0;
        self.range = 900;
        
        self.tile = Tile("img/boss.png", self.width, self.height);
        self.bricksDie = [Brick(0, 0, self.tile), Brick(0, 3, self.tile), Brick(0, 4, self.tile)];
        self.bricks = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile)];
        
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
        bodyDef.linearVelocity = (0.5, 0)
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "boss"};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture);
    
    def update(self):
        
        self.collision();
        if (not self.dying):
            
            if (self.moveCounter == self.range):
                self.walk("left");
            elif (self.moveCounter == self.range*2):
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
        
    def newMob(self, qtde):
        for somersault in range(qtde):
            print (self.pos[0]*self.PPM, self.pos[1]*self.PPM)
            new = Somersault((self.pos[0]*self.PPM, self.pos[1]*self.PPM), self.surface, self.world, self.PPM);
            self.mobList.append(new);        
    
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
            
    def die(self):
        self.counter = 0;
        self.bricks = self.bricksDie;
        self.dying = True;
        
    def getHit(self, enemy):
        enemy.ApplyForce((0, -10), enemy.position, True);
        self.life -= 10;
        if (self.life <= 0):
            self.die();
        
    def collision(self):
        
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            if (contact.fixtureA.body.userData["name"] == "drake"):
                enemy = contact.fixtureA.body;
            elif (contact.fixtureB.body.userData["name"] == "drake"):
                enemy = contact.fixtureB.body;
           
            if (contact.manifold.localNormal == (0, 1)):
                self.getHit(enemy);
            else:
                enemy.userData["self"].getHit(10);
        