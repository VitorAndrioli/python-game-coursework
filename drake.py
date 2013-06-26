import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from pygame import Rect;

#Classe dp heroi, X-Drake

class Drake():
    def __init__(self, pos, surface, world, PPM):
        self.width = 60;
        self.height = 115;
        self.widthSprite = 265;
        self.heightSprite = 148;
        self.pos = (pos[0]/PPM, pos[1]/PPM);
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 80;
        
        self.tile = Tile("img/drake.png", self.widthSprite, self.heightSprite);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), Brick(0, 3, self.tile)];
        self.bricksWalk = [Brick(4, 4, self.tile), Brick(4, 5, self.tile), Brick(4, 6, self.tile), Brick(4, 7, self.tile), 
                           Brick(4, 8, self.tile), Brick(4, 9, self.tile), Brick(4, 10, self.tile), Brick(4, 11, self.tile)];
        self.bricksDuck = [Brick(21, 21, self.tile)];
        self.bricksDie = [Brick(22, 22, self.tile), Brick(21, 23, self.tile), Brick(21, 24, self.tile), Brick(21, 25, self.tile),
                         Brick(21, 26, self.tile)];
        self.bricksJump = [Brick(20, 20, self.tile)];
        self.bricksDefeated = [Brick(21, 26, self.tile), Brick(21, 26, self.tile)];
        self.bricks = self.bricksStand;
        
        self.moveRight = False;
        self.moveLeft = False;
        self.duck = False;
        self.jumping = False;
        self.right = True;
        self.inFinalStage = False;
        self.dead = False;
        self.dying = False;
        
        self.createPhysicalBody();
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_dynamicBody;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "drake", "self": self};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.density = 0.07;
        bodyFixture.restitution = 0;
        bodyFixture.friction = 0.1;
        
        self.body.CreateFixture( bodyFixture );
        
    def update(self):
        
#        print self.jumping
        if (not self.dying):
            self.collision();
        
            if (self.body.position[1] > 9):
                self.body.ApplyForce((-10, -20), self.body.position, True);
                self.die();
            
            if (self.jumping):
                self.bricks = self.bricksJump;
            elif (self.duck):
                self.bricks = self.bricksDuck;
            elif (self.moveRight and not self.jumping):
                self.right = True;
                if (self.body.position[0] < 10):
                    self.body.ApplyLinearImpulse((0.03, 0), self.body.position, True);
                self.bricks = self.bricksWalk;
            elif (self.moveLeft and not self.jumping):
                self.right = False;
                self.body.ApplyLinearImpulse((-0.03, 0), self.body.position, True);
                self.bricks = self.bricksWalk;
            else:
                self.bricks = self.bricksStand;
            
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                if (self.dying):
                    self.dead = True
                    self.bricks = self.bricksDefeated;
                self.counter = 0;
            self.animationStep = 0;
            
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
        
        self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.widthSprite/2, self.body.position[1]*self.PPM - self.heightSprite/2 - 5));
        
    def jump(self):
        self.animationStep = 0;
        self.jumping = True;
        self.animationSpeed = 80;
        self.bricks = self.bricksJump;
        impulse = self.body.mass * 350;
        self.body.ApplyForce((0, -impulse), self.body.position, True);
        
    def die(self):
        self.bricks = self.bricksDie;
        self.dying = True;
        
        
    def getEvent(self, eventType, eventKey):
        self.counter = 0;
        if (eventType == pygame.locals.KEYDOWN):
            if (eventKey == pygame.locals.K_RIGHT):
                self.moveRight = True;
                if (self.jumping):
                    self.body.ApplyForce((0.0001, 0), self.body.position, True);
                    
            elif (eventKey == pygame.locals.K_LEFT):
                self.moveLeft = True;
                if (self.jumping):
                    self.body.ApplyForce((-0.0001, 0), self.body.position, True);
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
            
    def getHit(self):
        if (not self.dying):
            self.die();    
        
    def collision(self):
        enemy = None;
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            
            if (contact.fixtureA.body.userData["name"] == "drake"):
                enemy = contact.fixtureB.body;
            elif (contact.fixtureB.body.userData["name"] == "drake"):
                enemy = contact.fixtureA.body;
            
            if (not self.inFinalStage):
                if (enemy.userData["name"] == "finalStage"):
                    self.inFinalStage = True;
            self.jumping = False;
        
        
        
        