import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from pygame import Rect;

class Franky():
    def __init__(self, pos, surface, world, PPM):
        self.width = 120;
        self.height = 115;
        self.spriteWidth = 150;
        self.spriteHeight = 150;
        self.pos = (pos[0]/PPM, pos[1]/PPM);
        self.life = 200;
        self.franky = self;
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 100;
        
        self.tile = Tile("img/franky.png", self.spriteWidth, self.spriteHeight);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), Brick(0, 3, self.tile)];
        self.bricksWalk = [Brick(4, 4, self.tile), Brick(4, 5, self.tile), Brick(4, 6, self.tile), Brick(4, 7, self.tile), Brick(4, 8, self.tile), Brick(4, 9, self.tile), Brick(4, 10, self.tile), Brick(4, 11, self.tile)];
        self.bricksDuck = [Brick(12, 12, self.tile)];
        self.bricksJump = [Brick(13, 13, self.tile), Brick(13, 14, self.tile), Brick(13, 15, self.tile), Brick(13, 16, self.tile), Brick(13, 17, self.tile), Brick(13, 18, self.tile), Brick(13, 19, self.tile)]
        self.bricks = self.bricksStand;
        
        self.moveRight = False;
        self.moveLeft = False;
        self.duck = False;
        self.jumping = False;
        self.right = True;
        self.moveBody = True;
        
        self.createPhysicalBody();
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_dynamicBody;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "franky", "self": self};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.density = 0.07;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture( bodyFixture);

    def update(self):
        if (self.life > 0):
            self.collision();
      
            if (self.jumping):
                self.bricks = self.bricksJump;
#                if (self.moveRight):
#                    self.right = True;
#                    self.body.ApplyForce((0.06, 0), self.body.position, True);
#                elif (self.moveLeft):
#                    self.right = False;
#                    self.body.ApplyForce((-0.06, 0), self.body.position, True);
            
            elif (self.duck):
                self.bricks = self.bricksDuck;
           
            if (self.body.position[0] >= self.surface.get_width()/(2*self.PPM)):
                self.moveBody = False;
            
            if (self.moveRight):
                if (self.moveBody or True):
                    self.right = True;
                    self.body.ApplyLinearImpulse((0.03, 0), self.body.position, True);
                    self.bricks = self.bricksWalk;
            elif (self.moveLeft):
                self.moveBody = True;
                self.right = False;
                self.body.ApplyLinearImpulse((-0.03, 0), self.body.position, True);
                self.bricks = self.bricksWalk;
            else:
                self.bricks = self.bricksStand;
            
            self.animationStep += 1;
            if (self.animationStep == self.animationSpeed):
                self.counter += 1;
                if (self.counter == len(self.bricks)):
                    self.counter = 0;
                self.animationStep = 0;
            
            self.drawLifeBar();
            
        else:
            self.die();
        
        self.render();
        
    def render(self):
        shape = self.body.fixtures[0].shape;
        pixelVertices = [];
        for vertice in shape.vertices:
            v = self.body.transform * vertice * self.PPM;
            pixelVertices.append(v);
        
#        pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
        if (self.right):
            sprite = self.bricks[self.counter].getImage();
        else :
            sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
        
        self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.spriteWidth/2, self.body.position[1]*self.PPM - self.spriteHeight/2 - 5));
        
    def drawLifeBar(self):
        
        pygame.draw.rect(self.surface, (255, 0, 0), Rect((10, 10), (self.life*2, 10)), 0);
    
    def jump(self):
        self.animationStep = 0;
        self.jumping = True;
        self.animationSpeed = 80;
        impulse = self.body.mass * 500;
        self.body.ApplyForce((0, -impulse), self.body.position, True);
        
    def die(self):
        print "DEATH";
        
        
    def getEvent(self, eventType, eventKey):
        self.counter = 0;
        if (eventType == pygame.locals.KEYDOWN):
            if (eventKey == pygame.locals.K_RIGHT):
                self.moveRight = True;
            elif (eventKey == pygame.locals.K_LEFT):
                self.moveLeft = True;
            elif (eventKey == pygame.locals.K_DOWN):
                self.duck = True;
            elif (eventKey == pygame.locals.K_UP):
                self.jump()
        elif (eventType == pygame.locals.KEYUP):
            if (eventKey == pygame.locals.K_RIGHT):
                self.moveRight = False;
            elif (eventKey == pygame.locals.K_LEFT):
                self.moveLeft = False;
            elif (eventKey == pygame.locals.K_DOWN):
                self.duck = False;
            
    def getHit(self, damage):
        self.life -= damage;    
        
    def collision(self):
        for contact_edge in self.body.contacts:
            contact = contact_edge.contact;
            other = contact.fixtureA.body;
            otherName = other.userData["name"];
            if (self.jumping and otherName == "floor"):
                self.jumping = False;
                self.animationStep = 0;
                self.counter = 0;
                self.bricks = self.bricksStand;
            
        
        
        
        
        