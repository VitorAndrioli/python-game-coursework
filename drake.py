import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;
from pygame import Rect;

#Classe do heroi, X-Drake

class Drake():
    def __init__(self, pos, surface, world, PPM):
        #Constantes do personagem
        self.width = 60;
        self.height = 115;
        self.widthSprite = 265;
        self.heightSprite = 148;
        self.dinoWidth = 100;
        self.dinoHeight = 100;
        self.dinoWidthSprite = 100;
        self.dinoHeightSprite = 100;
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        #Variaveis para animacao
        self.pos = (pos[0]/PPM, pos[1]/PPM);
        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 80;
        self.deathCounter = 0;
        self.dino = False;
        
        #Tilesets e Bricks
        tileSet = Tile("img/drake.png", self.widthSprite, self.heightSprite);
        self.bricksDrakeStand = [Brick(0, 0, tileSet), Brick(0, 1, tileSet), Brick(0, 2, tileSet), Brick(0, 3, tileSet)];
        self.bricksDrakeWalk = [Brick(4, 4, tileSet), Brick(4, 5, tileSet), Brick(4, 6, tileSet), Brick(4, 7, tileSet), 
                           Brick(4, 8, tileSet), Brick(4, 9, tileSet), Brick(4, 10, tileSet), Brick(4, 11, tileSet)];
        self.bricksDrakeDuck = [Brick(21, 21, tileSet)];
        self.bricksDie = [Brick(22, 22, tileSet), Brick(21, 23, tileSet), Brick(21, 24, tileSet), Brick(21, 25, tileSet),
                         Brick(21, 26, tileSet)];
        self.bricksDrakeJump = [Brick(20, 20, tileSet)];
        self.bricksDefeated = [Brick(21, 24, tileSet), Brick(21, 24, tileSet)];
        
        dinoTileSet = Tile("img/dino.png", self.dinoWidthSprite, self.dinoHeightSprite);
        self.bricksDinoTransform = [Brick(0, 0, dinoTileSet), Brick(0, 1, dinoTileSet), Brick(0, 2, dinoTileSet),
                                    Brick(0, 3, dinoTileSet), Brick(0, 4, dinoTileSet), Brick(0, 5, dinoTileSet),
                                    Brick(0, 6, dinoTileSet), Brick(0, 7, dinoTileSet)];
        self.bricksdinoStand = [Brick(17, 17, dinoTileSet), Brick(17, 18, dinoTileSet)];
        self.bricksDinoWalk = [Brick(11, 11, dinoTileSet), Brick(11, 12, dinoTileSet), Brick(11, 13, dinoTileSet),
                               Brick(11, 14, dinoTileSet), Brick(11, 15, dinoTileSet), Brick(11, 16, dinoTileSet)];
        self.bricksDrakeTransform = [Brick(7, 7, dinoTileSet), Brick(7, 8, dinoTileSet), Brick(7, 9, dinoTileSet),
                                     Brick(7, 10, dinoTileSet)];
                                     
        self.bricksStand = self.bricksDrakeStand;
        self.bricksWalk = self.bricksDrakeWalk;
        self.bricksDuck = self.bricksDrakeDuck;
        self.bricksJump = self.bricksDrakeJump;
        
        self.bricks = self.bricksStand;
        
        #Booleanas para controlar a movimentacao
        self.moveRight = False;
        self.moveLeft = False;
        self.duck = False;
        self.jumping = False;
        self.right = True;
        self.inFinalStage = False;
        self.dead = False;
        self.dying = False;
        
        self.createPhysicalBody("normal");
        
    def createPhysicalBody(self, mode):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (self.pos[0], self.pos[1]);
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_dynamicBody;
        
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "drake", "self": self};
        
        if (mode == "normal"):
            width = float(self.width)/(2*self.PPM);
            height = float(self.height)/(2*self.PPM);
            density = 0.07;
        elif (mode == "dino"):
            width = float(self.dinoWidth)/(2*self.PPM);
            height = float(self.dinoHeight)/(2*self.PPM);
            density = 0.07;
            
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.density = density;
        bodyFixture.restitution = 0;
        bodyFixture.friction = 0.1;
        
        self.body.CreateFixture( bodyFixture );
    
    #Transformar o body em kinematic, para animação de "morte"
    def turnToKinemact(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = self.body.position;
        bodyDef.angle = 0;
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_kinematicBody;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "drake", "self": self};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture );
        
    def update(self):
        if (self.body.type == 2):
            if (self.body.position[1] > 9):
                self.body.ApplyForce((-10, -10), self.body.position, True);
                self.die();
    
        if (not self.dying):
            self.collision();
            
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
            
        else:
            self.deathCounter += 1;
            if (self.deathCounter == 60):
                self.body.linearVelocity = (-0.1, 2);
        
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                if (self.dying):
                    self.dead = True
                self.counter = 0;
            self.animationStep = 0;    
        self.render();
        
    def render(self):
    #Desenhar o body para debug
#        shape = self.body.fixtures[0].shape;
#        pixelVertices = [];
#        for vertice in shape.vertices:
#            v = self.body.transform * vertice * self.PPM;
#            pixelVertices.append(v);
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
        
    def getHit(self):
        if (not self.dying):
            self.die();    
        
    def die(self):
        self.bricks = self.bricksDefeated;
        self.turnToKinemact();
        self.body.linearVelocity = (-0.1, -2);
        self.dying = True;
        
    def turnToDino(self):
        if (not self.dino):
        self.dino = True;
            self.createPhysicalBody("dino");
            self.bricks = self.bricksDinoTransform;
            self.bricksStand = self.bricksDinoStand;
            self.bricksWalk = self.bricksDinoWalk;
            self.bricksDuck = self.bricksDinoDuck;
            self.bricksJump = self.bricksDinoJump;
    
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
            elif (eventKey == pygame.locals.K_SPACEBAR):
                self.turnToDino();
        elif (eventType == pygame.locals.KEYUP):
            if (eventKey == pygame.locals.K_RIGHT):
                self.moveRight = False;
            elif (eventKey == pygame.locals.K_LEFT):
                self.moveLeft = False;
            elif (eventKey == pygame.locals.K_DOWN):
                self.duck = False;
            
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
        