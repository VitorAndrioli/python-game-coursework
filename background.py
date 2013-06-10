import Box2D as b2;
import pygame;

class Background():
    def __init__(self, surface, world):
        self.world = world;
        self.surface = surface;
        
        self.createBody();
        
    def createBody(self):
        
        bodyDef = b2.b2BodyDef();
        bodyDef.position = (0, 430);
        bodyDef.type = b2.b2_staticBody;
        bodyDef.angle = 0;
        self.body = self.world.CreateBody( bodyDef );
        
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.shape = b2.b2PolygonShape( box=(800, 80));
        bodyFixture.friction = 1;
        bodyFixture.restitution = 0;
        
        self.body.CreateFixture( bodyFixture );
    
    def draw(self):
        shape = self.body.fixtures[0].shape;
        pixelVertices = [];
        for vertice in shape.vertices:
            v = self.body.transform * vertice;
            pixelVertices.append(v);
            
        pygame.draw.polygon(self.surface, (0, 255, 0), pixelVertices);
        
        
    