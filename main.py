import pygame;
from pygame import locals;
import Box2D as b2;

from plant import Plant;
from drake import Drake;
from wapol import Wapol;
from boss import Boss;
from rotating import Somersault;

from background import Background;
from plataform import Plataform;
from menu import Menu;

#criacao da tela
surface = pygame.display.set_mode((1200, 608), 0, 32);

#criacao do menu inicial
initialMenu = True;
menu = Menu(initialMenu);
paused = True;
bossInGame = False;
gameStarted = False;

PPM = 60.0;
gravidade = b2.b2Vec2(0, 9.8);
world = b2.b2World(gravidade, True);

#Criacao fo cenario e do heroi
background = Background(surface, world, PPM);
plataformList = [Plataform((7200, 600),surface, world, PPM, 700, True), Plataform((14000, 220),surface, world, PPM, 3000, False),
                 Plataform((0, 200),surface, world, PPM, 15000, True)];


drake = Drake((10, 0), surface, world, PPM);

#criacao dos viloes
plantList = [Plant((600, 330), surface, world, PPM), Plant((1920, 550), surface, world, PPM), Plant((3550, 550), surface, world, PPM), 
            Plant((3850, 550), surface, world, PPM), Plant((4120, 550), surface, world, PPM), Plant((4780, 550), surface, world, PPM), 
            Plant((5350, 550), surface, world, PPM), Plant((8700, 550), surface, world, PPM), Plant((9680, 550), surface, world, PPM)];

wapolList = [Wapol((1700, 547), surface, world, PPM, 500), Wapol((3240, 547), surface, world, PPM, 380), 
             Wapol((5236, 420), surface, world, PPM, 326), Wapol((6100, 547), surface, world, PPM, 526), 
             Wapol((6350, 547), surface, world, PPM, 882), Wapol((9050, 547), surface, world, PPM, 832),
             Wapol((9780, 547), surface, world, PPM, 218), Wapol((12200, 547), surface, world, PPM, 824),
             Wapol((12700, 547), surface, world, PPM, 632), Wapol((13400, 547), surface, world, PPM, 902),
             Wapol((13100, 547), surface, world, PPM, 500)];

somersaultList = []
boss = None;

moveBackgroundRight = False;
moveBackgroundLeft = False;
worldOrigin = 0;


#Loop principal            
while(True):
    world.Step(1.0/30, 8, 3);
    surface.fill((0, 0, 0));
    if (paused or drake.dead):
        menu.update(surface);
    
    else:
        if (drake.inFinalStage and not bossInGame):
            boss = Boss((14630, 520), surface, world, PPM, somersaultList);
            bossInGame = True; 
    
        background.update();
        
        for plataform in plataformList:
            plataform.update();
        
        drake.update();
        
        if (boss != None):
            boss.update();
    
        for plant in plantList:
            plant.update();
        
        for wapol in wapolList:
            if (not wapol.dead):
                wapol.update();
    
        for somersault in somersaultList:
            if (not somersault.dead):
                somersault.update();
    
        #mover o cenario
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
        
        if (paused):
            if (e.type == pygame.locals.KEYDOWN):
                #Sair do menu
                if (e.key == pygame.locals.K_RETURN or e.key == pygame.locals.K_KP_ENTER):
                    paused = False;
            elif (e.type == pygame.locals.QUIT):
                exit();
        else:
            if (e.type == pygame.locals.KEYDOWN):
                #passar eventos do teclado para o heroi e mover o cenario
                drake.getEvent(e.type, e.key);
                if (e.key == pygame.locals.K_RIGHT):
                    moveBackgroundRight = True;
                elif (e.key == pygame.locals.K_LEFT):
                    moveBackgroundLeft = True;
                #pausar o jogo
                elif (e.key == pygame.locals.K_p):
                    paused = True;
                    menu = Menu(False);
#                elif (e.key == pygame.locals.K_z):
#                    new = Somersault((10, 10), surface, world, PPM, True);
#                    somersaultList.append(new);
            elif (e.type == pygame.locals.KEYUP):
                drake.getEvent(e.type, e.key);
                if (e.key == pygame.locals.K_RIGHT):
                    moveBackgroundRight = False;
                elif (e.key == pygame.locals.K_LEFT):
                    moveBackgroundLeft = False;
            elif (e.type == pygame.locals.QUIT):
                exit();
