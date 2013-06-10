import pygame;
import Box2D as b2;
from pygame import locals;
from plant import Plant;
from chopperman import Chopperman;
from background import Background;
from franky import Franky;

PPM = 1;
gravidade = b2.b2Vec2(0, 9.8);
world = b2.b2World(gravidade, True);

surface = pygame.display.set_mode((640, 480), 0, 32);
clock = pygame.time.Clock();

plant = Plant((400, 300), surface, world, PPM);
chopperman = Chopperman((150, 100), surface, world, PPM);
background = Background(surface, world);
franky = Franky((200, 200), surface, world, PPM);

while(True):
    
    world.Step(1.0/30, 8, 3);
    surface.fill((0, 0, 0));
    
    background.draw();
    plant.update();
    chopperman.update();
    franky.update();

    pygame.display.update();
#    clock.tick(60);
    
    for e in pygame.event.get():
        
        if (e.type == pygame.locals.KEYDOWN):
            franky.getEvent(e.type, e.key);
            if (e.key == pygame.locals.K_1):
                plant.colision = True;
            elif (e.key == pygame.locals.K_2):
                chopperman.body.position = (0, chopperman.body.position[1]);
        elif (e.type == pygame.locals.KEYUP):
            franky.getEvent(e.type, e.key);

        elif (e.type == pygame.locals.QUIT):
            exit();
            
    
