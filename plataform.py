import pygame;
import Box2D as b2;

class Plataform():
    def __init__(self, pos, surface, world, PPM, range, right):
        self.height = 64;
        self.width = 288;
        self.pos = (pos[0]/PPM, pos[1]/PPM) ;
        self.image = pygame.image.load("img/plataform.png")
        self.range = range;
        self.right = right;
        
        self.counter = 0;
        
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.createPhysicalBody()
        
    def createPhysicalBody(self):
        bodyDef = b2.b2BodyDef();
        bodyDef.position = self.pos;
        bodyDef.angle = 0;
        if (self.right):
            vel = 0.5;
        else:
            vel = -0.5;
        bodyDef.linearVelocity = (vel, 0);
        bodyDef.fixedRotation = True;
        bodyDef.type = b2.b2_kinematicBody;
        
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "plataform"};
        
        bodyFixture = b2.b2FixtureDef();
        width = float(self.width)/(2*self.PPM);
        height = float(self.height)/(2*self.PPM);
        bodyFixture.shape = b2.b2PolygonShape( box=(width, height));
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture( bodyFixture );
        
    def update(self):
        self.counter += 1;
        if (self.counter == self.range):
            if (self.right):
                vel = -0.5;
                self.right = False;
            else:
                vel = 0.5;
                self.right = True;
            self.body.linearVelocity = (vel, 0);
            self.counter = 0;
        self.render();
        
    def render(self):
        #desenha o corpo para debug
#        shape = self.body.fixtures[0].shape;
#        pixelVertices = [];
#        for vertice in shape.vertices:
#            v = self.body.transform * vertice * self.PPM;
#            pixelVertices.append(v);
#        pygame.draw.polygon(self.surface, (0, 255, 255), pixelVertices);
        self.surface.blit(self.image, (self.body.position[0]*self.PPM - self.width/2, self.body.position[1]*self.PPM - self.height/2));
        
    