import pygame;
from pygame import locals;
from tile import Tile;
from brick import Brick;
from gameSprite import GameSprite;

surface = pygame.display.set_mode((640, 480), 0, 32);
clock = pygame.time.Clock();

tileFranky = Tile("img/sprite_t.png", 240, 190);

bricksStand = [Brick(0, 0, tileFranky), Brick(1, 1, tileFranky), Brick(2, 2, tileFranky), Brick(3, 3, tileFranky)];
bricksWalk = [Brick(4, 4, tileFranky), Brick(5, 5, tileFranky), Brick(6, 6, tileFranky), Brick(7, 7, tileFranky), Brick(8, 8, tileFranky), Brick(9, 9, tileFranky)];

franky = GameSprite(bricksStand, (100, 100));

moveRight = False;
moveLeft = False;
stand = True;
while(True):
    
    surface.fill((0, 0, 0));
    franky.update();
    franky.render(surface);
    
    pygame.display.update();
    clock.tick(30);
    
    for e in pygame.event.get():
        if (e.type == pygame.locals.KEYDOWN):
            if (e.key == pygame.locals.K_RIGHT):
                moveRight = True;
                stand = False;
            elif (e.key == pygame.locals.K_LEFT):
                moveLeft = True;
                stand = False; 
        elif (e.type == pygame.locals.KEYUP):
            if (e.key == pygame.locals.K_RIGHT):
                moveRight = False;
                stand = True;
            elif (e.key == pygame.locals.K_LEFT):
                moveLeft = False;
                stand = True;
        elif (e.type == pygame.locals.QUIT):
            exit();
            
    
    if (stand):
        franky.bricks = bricksStand;
    if (moveRight):
        #franky.setPosition((franky.pos[0]+5, franky.pos[1]));
        franky.bricks = bricksWalk;
    if (moveLeft):
        franky.setPosition((franky.pos[0]-10, franky.pos[1]));