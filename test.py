
from Box2D import b2World, b2FixtureDef, b2PolygonShape;

import pygame;
from pygame import locals;
from pygame import time;

PPM=20.0 # pixels per meter
WORLD_WIDTH = 30;
WORLD_HEIGHT = 30;
SCREEN_WIDTH = 800;
SCREEN_HEIGHT = 600;


world = b2World( gravity=(0,-10), doSleep=True);
timeStep = 1 / 6.0;
vel_iters, pos_iters = 6, 2;

# This is our little game loop.

    
    
screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32);

listaObjetos = [ {"type":"static", "vertices":[(0, 1), (30, 1), (30, 0), (0, 0), (0, 1)], "angulo":0, "cor":(0, 255, 0)} ];
#                 {"type":"dynamic", "x":5, "y":20, "w":2, "h":2, "angulo":15, "cor":(255, 0, 0)},
#                 {"type":"dynamic", "x":5, "y":10, "w":1, "h":2, "angulo":15, "cor":(0, 0, 255)},
#                 {"type":"dynamic", "x":10, "y":30, "w":1, "h":2, "angulo":15, "cor":(255, 255, 0)} ];
                 
physicsObjects = [];   


def setup_physics():
#    groundBodyDef = b2BodyDef();
#    groundBodyDef.position = (0, -10);
#    
#    groundBody = world.CreateBody(groundBodyDef);
#    
#    groundBox=b2PolygonShape(box=(50,10));
#    
#    # And create a fixture definition to hold the shape
#    groundBoxFixture=b2FixtureDef(shape=groundBox);
#    
#    # Add the ground shape to the ground body.
#    groundBody.CreateFixture(groundBoxFixture);
#    
#    body=world.CreateDynamicBody(position=(0,4));
#    
#    box=body.CreatePolygonFixture(box=(1,1), density=1, friction=0.3);
    for obj in listaObjetos:
        simpleBoxBody = [];
        shape = None;
        pos = None;
        fixture = None;
        if ( obj.has_key("vertices") ) :
            shape = b2PolygonShape(vetices=obj["vertices"]);
            #shape = b2EdgeShape(vetices=obj["vertices"]),
            fixture = b2FixtureDef(vetices=obj["vertices"], density=1, friciton=0.3);
            pos = None;
        else:
            shape = b2PolygonShape(box=( obj["w"], obj["h"] ));
            fixture = b2FixtureDef(box=( obj["w"], obj["h"] ), density=1, friciton=0.3);
            pos = ( obj["x"], obj["y"]);
            
        if (obj["type"] == "dynamic") :
            simpleBoxBody = world.CreateDynamicBody(
                                                shapes=shape,
                                                position=pos,
                                                angle=obj["angulo"]
                                                );
            simpleBoxBody.CreateFixture(fixture);
        else :
            simpleBoxBody = world.CreateStaticBody(
                                                shapes=shape,
                                                position=pos,
                                                angle=obj["angulo"]
                                                );
        simpleBoxBody.objeto = obj;
        physicsObjects.append( simpleBoxBody );
        print simpleBoxBody.objeto;
    

def tX(coordX):
    return coordX * PPM;

def tY(coordY):
    return SCREEN_HEIGHT-(coordY * PPM); 
    

def update():
    # Instruct the world to perform a single step of simulation. It is
    # generally best to keep the time step and iterations fixed.
    world.Step(timeStep, vel_iters, pos_iters);

    # Clear applied body forces. We didn't apply any forces, but you
    # should know about this function.
    world.ClearForces();
 
    # Now print the position and angle of the body.
    # print body.position, body.angle;
    for count in range(len(physicsObjects)):
        obj = physicsObjects[count];
        objPic = listaObjetos[count];
        objPic["x"] = obj.position.x;
        objPic["y"] = obj.position.y;
        
        
            
        
 

def draw():
    screen.fill( (0,0,0) );
    for body in physicsObjects:
        for fixture in body.fixtures:
            # The fixture holds information like density and friction,
            # and also the shape.
            shape=fixture.shape
            
            # Naively assume that this is a polygon shape. (not good normally!)
            # We take the body's transform and multiply it with each 
            # vertex, and then convert from meters to pixels with the scale
            # factor. 
            vertices=[(body.transform*v)*PPM for v in shape.vertices];
            vertices=[(v[0], SCREEN_HEIGHT - v[1]) for v in vertices];
            print vertices;
            pygame.draw.polygon( screen, body.objeto["cor"], vertices);
    pygame.display.update();    
    
    
def events():
    for e in pygame.event.get():
        if (e.type == locals.QUIT):
            exit();
            
setup_physics();
clock = time.Clock();

while(True): 
    update();
    clock.tick(30);
    draw();
    events();
