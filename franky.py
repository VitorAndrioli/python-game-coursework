import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;

class Franky():
    def __init__(self, pos, surface, world, PPM):
        self.width = 150;
        self.height = 150;
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 100;
        
        self.tile = Tile("img/franky.png", 150, 150);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), Brick(0, 3, self.tile)];
        self.bricksWalk = [Brick(4, 4, self.tile), Brick(4, 5, self.tile), Brick(4, 6, self.tile), Brick(4, 7, self.tile), Brick(4, 8, self.tile), Brick(4, 9, self.tile), Brick(4, 10, self.tile), Brick(4, 11, self.tile)];
        self.bricksDuck = [Brick(12, 12, self.tile)];
        self.bricksJump = [Brick(13, 13, self.tile), Brick(13, 14, self.tile), Brick(13, 15, self.tile), Brick(13, 16, self.tile), Brick(13, 17, self.tile), Brick(13, 18, self.tile), Brick(13, 19, self.tile)]
        self.bricks = self.bricksStand;
        
        self.createPhysicalBody(pos);
        
    def createPhysicalBody(self, pos):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = pos;
        bodyDef.angle = 0;
        bodyDef.type = b2.b2_dynamicBody;
        self.body = self.world.CreateBody( bodyDef );
        
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.shape = b2.b2PolygonShape( box=(self.width/2, self.height/2));
        bodyFixture.density = 100;
        bodyFixture.friction = 1;
        bodyFixture.restitution = 0;
        
        self.moveRight = False;
        self.moveLeft = False;
        self.duck = False;
        self.jumping = False;
        self.right = True;
        
        self.body.CreateFixture( bodyFixture);
        
    def update(self):
        
        if (self.duck):
            self.bricks = self.bricksDuck;
        elif (self.moveRight):
            self.right = True;
            self.body.position = (self.body.position[0]+0.5, self.body.position[1]);
            self.bricks = self.bricksWalk;
        elif (self.moveLeft):
            self.right = False;
            self.body.position = (self.body.position[0]-0.5, self.body.position[1]);
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
        
        #pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
        if (self.right):
            sprite = self.bricks[self.counter].getImage();
        else :
            sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
        
        self.surface.blit(sprite, (self.body.position[0] - self.width/2, self.body.position[1] - self.height/2));
        
        
    def jump(self):
        self.animationStep = 0;
        self.jumping = True;
        self.animationSpeed = 50;
        self.body.ApplyForce((0, -7000000000), self.body.position, True);
        
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
            
        
        
        
        
        
        
        
        