import pygame;
import Box2D as b2;
from pygame import locals;
from plant import Plant;
from background import Background;
from drake import Drake;
from menu import Menu;
from wapol import Wapol;
from boss import Boss;
from rotating import Somersault;

PPM = 60.0;
gravidade = b2.b2Vec2(0, 9.8);
world = b2.b2World(gravidade, True);

surface = pygame.display.set_mode((1200, 608), 0, 32);

somersaultList = [Somersault((200, 500), surface, world, PPM), Somersault((200, 400), surface, world, PPM)];


background = Background(surface, world, PPM);
#drake = Drake((200, 200), surface, world, PPM);
boss = Boss((14400, 520), surface, world, PPM, somersaultList);


#plantList = (Plant((600, 330), surface, world, PPM), Plant((1920, 550), surface, world, PPM), Plant((3550, 550), surface, world, PPM), 
#            Plant((3850, 550), surface, world, PPM), Plant((4120, 550), surface, world, PPM), Plant((4780, 550), surface, world, PPM), 
#            Plant((5350, 550), surface, world, PPM), Plant((8700, 550), surface, world, PPM), Plant((9680, 550), surface, world, PPM));


wapolList = (Wapol((1700, 547), surface, world, PPM, 500), Wapol((3240, 547), surface, world, PPM, 380), 
             Wapol((5236, 420), surface, world, PPM, 326), Wapol((6100, 547), surface, world, PPM, 526), 
             Wapol((6350, 547), surface, world, PPM, 882), Wapol((9050, 547), surface, world, PPM, 832),
             Wapol((9780, 547), surface, world, PPM, 218), Wapol((12200, 547), surface, world, PPM, 824),
             Wapol((12700, 547), surface, world, PPM, 632), Wapol((13400, 547), surface, world, PPM, 902),
             Wapol((13100, 547), surface, world, PPM, 500));

menuSurface = Menu("enter to start");
paused = True;
starting = True;

moveBackgroundRight = False;
moveBackgroundLeft = False;
worldOrigin = 0;
            
while(True):
    world.Step(1.0/30, 8, 3);
    
    if (paused):
        if (starting):
            surface.blit(menuSurface.getSurface(), (0, 0));
        else:
            menuSurface.message = ("enter to continue");
            surface.blit(menuSurface.getSurface(), (0, 0));
        menuSurface.update();
    else:
        surface.fill((0, 0, 0));
    
        background.update();
#        drake.update();
        boss.update();
        
#        for plant in plantList:
#            plant.update();
            
        for wapol in wapolList:
            if (not wapol.dead):
                wapol.update();
        
        for somersault in somersaultList:
            somersault.update();
        
        if (moveBackgroundRight):
            worldOrigin = 2/PPM;
            world.ShiftOrigin((worldOrigin, 0));
            background.move("right");
            
        if (moveBackgroundLeft):
            worldOrigin = -2/PPM;
            world.ShiftOrigin((worldOrigin, 0));
            background.move("left");
    
    pygame.display.update();
            
    for e in pygame.event.get():
        
        if (e.type == pygame.locals.KEYDOWN):
            if (e.key == pygame.locals.K_RETURN or e.key == pygame.locals.K_KP_ENTER):
                paused = False;
                starting = False;
            elif (not paused):
#                drake.getEvent(e.type, e.key);
                if (e.key == pygame.locals.K_RIGHT):
                    moveBackgroundRight = True;
                elif (e.key == pygame.locals.K_LEFT):
                    moveBackgroundLeft = True;
                elif (e.key == pygame.locals.K_p):
                    paused = True;
                elif (e.key == pygame.locals.K_z):
                    new = Somersault((200, 420), surface, world, PPM);
                    somersaultList.append(new);
                    
        elif (e.type == pygame.locals.KEYUP):
            if (not paused):
#                drake.getEvent(e.type, e.key);
                if (e.key == pygame.locals.K_RIGHT):
                    moveBackgroundRight = False;
                elif (e.key == pygame.locals.K_LEFT):
                    moveBackgroundLeft = False;
        elif (e.type == pygame.locals.QUIT):
            exit();
            
    
