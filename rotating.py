import Box2D as b2;
from brick import Brick;
from tile import Tile;
import pygame;

#Personagem Somersault, summonado pelo Boss. Nao pode ser morto pelo Heroi.

class Somersault():
    def __init__(self, pos, surface, world, PPM, right):

        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.width = 63;
        self.height = 61;
        self.pos = (pos[0]/self.PPM, pos[1]/self.PPM);
        self.newborn = True;

        self.counter = 0;
        self.animationStep = 0;
        self.animationSpeed = 20;
        
        self.tile = Tile("img/rotating.png", self.width, self.height);
        self.bricks = [Brick(0, 0, self.tile), Brick(0, 1, self.tile), Brick(0, 2, self.tile), 
                       Brick(0, 3, self.tile), Brick(0, 4, self.tile), Brick(0, 5, self.tile),
                       Brick(0, 6, self.tile), Brick(0, 7, self.tile), Brick(0, 8, self.tile)];
        
        self.moveRight = True;
        self.moveLeft = False;
        self.right = right;
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
        bodyFixture.friction = 0.1;
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        
        self.body.CreateFixture( bodyFixture);
        
    def update(self):
        
        self.collision();
        
        self.checkLife();
        
        #aplica impulso para cima quando personagem "nasce"
        if (self.newborn):
            self.body.ApplyForce((0, -1000), self.body.position, True);
            self.newborn = False;
        
        #ajusta a velocidade relativa ao lado para o qual o personagem esta indo
        if (self.right):
            impulse = 1.4;
        else:
            impulse = -1.4;
        self.body.ApplyLinearImpulse((impulse, 0), self.body.position, True);
        
        self.animationStep += 1;
        if (self.animationStep == self.animationSpeed):
            self.counter += 1;
            if (self.counter == len(self.bricks)):
                self.counter = 0;
            self.animationStep = 0;
            
        self.render();
    
    def render(self):
        if (not self.dead):
            
            #ajusta a sprite de acordo com a direcao do personagem
            if (self.right):
                sprite = self.bricks[self.counter].getImage();
            else :
                sprite = pygame.transform.flip(self.bricks[self.counter].getImage(), True, False);
            self.surface.blit(sprite, (self.body.position[0]*self.PPM - self.width/2, self.body.position[1]*self.PPM - self.height/2 + 3));
    
            #desenha corpo para debug
#            shape = self.body.fixtures[0].shape;
#            pixelVertices = [];
#            for vertice in shape.vertices:
#                v = self.body.transform * vertice * self.PPM;
#                pixelVertices.append(v);
#            pygame.draw.polygon(self.surface, (0, 0, 255), pixelVertices);
            
    def checkLife(self):
        if (self.body.position[1] > 10):
            self.world.DestroyBody(self.body);
            self.dead = True;
    
    def collision(self):
        enemy = None;
        for contact_edges in self.body.contacts:
            contact = contact_edges.contact;
            if (contact.fixtureA.body.userData["name"] == "drake"):
                enemy = contact.fixtureA.body;
            elif (contact.fixtureB.body.userData["name"] == "drake"):
                enemy = contact.fixtureB.body;
            if (enemy != None):
                enemy.userData["self"].getHit();
        