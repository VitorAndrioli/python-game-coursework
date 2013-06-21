from brick import Brick;
from tile import Tile;
import Box2D as b2;
import pygame;

class Plant():
    def __init__(self, pos, surface, world, PPM):
        #physical variables
        self.width = 96;
        self.height = 75;
        self.pos = pos;
        self.damage = 11;
        #animation variables
        self.counter = 0;
        self.animationSpeed = 300;
        self.animationStep = 0;
        self.ableToMove = True;
        
        self.tile = Tile("img/killer_plant.png", self.width, self.height);
        self.bricksStand = [Brick(0, 0, self.tile), Brick(0, 1, self.tile)];
        self.bricksAttack = [Brick(0, 2, self.tile), Brick(0, 3, self.tile), Brick(0, 3, self.tile), Brick(0, 1, self.tile)]; 
        
        self.bricks = self.bricksStand;
        
        #drawing variables
        self.PPM = PPM;
        self.surface = surface;
        self.world = world;
        
        #checking variables
        self.attacking = False;
        self.colision = False;
        
        self.createBody();
        
    def createBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (float(self.pos[0])/self.PPM, float(self.pos[1]+7)/self.PPM);
        bodyDef.angle = 0;
        bodyDef.type = b2.b2_staticBody;
        self.body = self.world.CreateBody(bodyDef);
        self.body.userData = {"name": "plant"};
        
        bodyFixture = b2.b2FixtureDef();
        height = float(self.height - 20)/(2*self.PPM);
        width = float(self.width)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box = (width, height) );
        bodyFixture.friction = 0.1;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture(bodyFixture);
        
    def update(self):
        self.collision();
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
                if (self.attacking):
                    self.backToNormal();
            self.animationStep = 0;
        self.render();
        
    def render(self):
        shape = self.body.fixtures[0].shape;
        pixelVertices = [];
        for vertice in shape.vertices:
            v = self.body.transform * vertice * self.PPM;
            pixelVertices.append(v);
            
#        pygame.draw.polygon(self.surface, (0, 255, 255), pixelVertices);
        self.surface.blit(self.bricks[self.counter].getImage(), (self.pos[0] - self.width/2, self.pos[1] - self.height/2));
    
    def attack(self, enemy):
        enemy.ApplyForce((-3, -5), enemy.position, True);
        enemy.userData["self"].getHit(self.damage);
        self.counter = 0;
        self.animationStep = 0;
        self.bricks = self.bricksAttack;
        self.attacking = True;
        self.animationSpeed = self.animationSpeed / 3;
        
    def backToNormal(self):
        self.ableToMove = True;
        self.animationStep = 0;
        self.bricks = self.bricksStand;
        self.animationSpeed = self.animationSpeed * 3;
        self.attacking = False;
        
    def collision(self):
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            enemy = contact.fixtureB.body;
            if (self.ableToMove):
                self.ableToMove = False;
                self.attack(enemy);
