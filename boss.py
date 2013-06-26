import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from pygame import Rect;
from rotating import Somersault;

#Boss do jogo

class Boss():
    def __init__(self, pos, surface, world, PPM, mobList):

        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.width = 125;
        self.height = 129;
        self.pos = (1100/self.PPM, -400/self.PPM);
        self.life = 2000;
        self.mobList = mobList;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 20;
        self.moveCounter = 0;
        self.deathCounter = 0;
        self.range = 900;
        self.mobCounter = 0;
        self.mobSpeed = 700;
        
        self.tile = Tile("img/boss.png", self.width, self.height);
        self.bricksDie = [Brick(0, 3, self.tile), Brick(0, 4, self.tile), Brick(0, 5, self.tile), Brick(0, 6, self.tile), 
                          Brick(0, 7, self.tile), Brick(0, 8, self.tile), Brick(0, 9, self.tile), Brick(0, 10, self.tile),
                          Brick(0, 11, self.tile), Brick(0, 12, self.tile), Brick(0, 13, self.tile), Brick(0, 14, self.tile),
                          Brick(0, 15, self.tile), Brick(0, 16, self.tile), Brick(0, 17, self.tile), Brick(0, 18, self.tile),
                          Brick(0, 19, self.tile), Brick(0, 20, self.tile), Brick(0, 21, self.tile), Brick(0, 22, self.tile),
                          Brick(0, 23, self.tile), Brick(0, 24, self.tile)];
        self.bricksDefeated = [Brick(0, 24, self.tile), Brick(0, 24, self.tile)];
                          
        self.bricks = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile)];
        
        self.moveRight = False;
        self.moveLeft = True;
        self.right = False;
        self.dying = False;
        self.dead = False;
        self.inGame = False;
        
        self.createPhysicalBody();
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_kinematicBody;
        bodyDef.linearVelocity = (0, 2)
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "boss"};
        
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.restitution = 0;
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture);
    
    def update(self):
        if (self.body.position[1] >= 8.7 and not self.inGame):
            self.walk("left")
            self.inGame = True;
        
        if (self.inGame):
            
            self.collision();
            
            if (not self.dying):
                if (self.moveCounter == self.range):
                    self.walk("right");
                elif (self.moveCounter == self.range*2):
                    self.walk("left");
                    self.moveCounter = 0;
            
                self.moveCounter += 1;
            
                self.animationStep += 1;
                if (self.animationStep == self.animationSpeed):
                    self.counter += 1;
                    if (self.counter == len(self.bricks)):
                        self.counter = 0;
                    self.animationStep = 0;
            else:
                self.body.linearVelocity = ((0, 0));
                if (self.deathCounter == 50):
                    self.counter += 1
                    self.deathCounter = 0;
                
                if (self.counter == 22):
                    self.dead = True;
                    self.counter = 0;
                    self.deathCounter = 0;
                self.deathCounter += 1;
                
                if (self.dead):
                    self.counter = 0;
                    self.bricks = self.bricksDefeated;
            if (self.mobCounter == self.mobSpeed and not self.dead and not self.dying):
                self.newMob();
                self.mobCounter = 0;
            self.mobCounter += 1;
            
        self.render();
        
    def drawLifeBar(self):
        pygame.draw.rect(self.surface, (255, 0, 0), Rect((10, 10), (self.life/2, 10)), 0);
    
    def newMob(self):
        if (self.right):
            right = True;
            x = self.body.position[0]*self.PPM;
            y = self.body.position[1]*self.PPM;
        else:
            right = False;
            x = self.body.position[0]*self.PPM - 1;
            y = self.body.position[1]*self.PPM - 1;
        
        new = Somersault((x, y), self.surface, self.world, self.PPM, right);
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
        self.drawLifeBar();
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
        enemy.ApplyForce((-10, -10), enemy.position, True);
        self.life -= 50;
        
        if (self.life >= 1500):
            self.mobSpeed = 700;
        elif (self.life >= 1000):
            self.mobSpeed = 500;
        elif (self.life >= 500):
            self.mobSpeed = 400;
        elif (self.life >= 0):
            self.mobSpeed = 300;
        else:
            self.die();
        
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
                    self.getHit(enemy);
                else:
                    enemy.userData["self"].getHit();
        