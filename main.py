import pygame;
import Box2D as b2;
from pygame import locals;
from plant import Plant;
from chopperman import Chopperman;
from background import Background;
from franky import Franky;

PPM = 60.0;
gravidade = b2.b2Vec2(0, 9.8);
world = b2.b2World(gravidade, True);

surface = pygame.display.set_mode((1200, 608), 0, 32);
bgSurface = pygame.Surface((8000, 608), 0, 32);


plant = Plant((950, 470), bgSurface, world, PPM);
#chopperman = Chopperman((500, 30), surface, world, PPM);
background = Background(surface, world, bgSurface);
franky = Franky((200, 200), surface, world, PPM);

for body in world.bodies:
        if (body.userData["name"] == "franky"):
#            print body
#            body.position[0] = body.position[0] - (1/PPM);
            body.ApplyLinearImpulse((0.03, 0), body.position, True);
    
#print world.__GetBodyList_internal()

moveBackgroundRight = False;
moveBackgroundLeft = False;
            
while(True):
    world.Step(1.0/30, 8, 3);
    
    surface.fill((0, 0, 0));
    
    
    background.update()
    plant.update();
#    chopperman.update();
    franky.update();
    
    if (moveBackgroundRight):
        print franky.body.position;
        world.ShiftOrigin((1/PPM, 0));
        background.move("right");
    if (moveBackgroundLeft):
        world.ShiftOrigin((-1/PPM, 0));
        background.move("left");
    
    
    pygame.display.update();
        
    for e in pygame.event.get():
        
        if (e.type == pygame.locals.KEYDOWN):
            franky.getEvent(e.type, e.key);
            if (e.key == pygame.locals.K_RIGHT):
                moveBackgroundRight = True;
            elif (e.key == pygame.locals.K_LEFT):
                moveBackgroundLeft = True;
        elif (e.type == pygame.locals.KEYUP):
            franky.getEvent(e.type, e.key);
            if (e.key == pygame.locals.K_RIGHT):
                moveBackgroundRight = False;
            elif (e.key == pygame.locals.K_LEFT):
                moveBackgroundLeft = False;
        elif (e.type == pygame.locals.QUIT):
            exit();
            
    
