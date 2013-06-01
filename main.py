import pygame;
from pygame import locals;
from tile import Tile;
from brick import Brick;
from gameSprite import GameSprite;

surface = pygame.display.set_mode((640, 480), 0, 32);
clock = pygame.time.Clock();

tileFranky = Tile("img/sprite_t.png", 240, 190);

bricksStand = [Brick(0, 0, tileFranky), Brick(0, 1, tileFranky), Brick(0, 2, tileFranky), Brick(0, 3, tileFranky)];
bricksWalk = [Brick(4, 4, tileFranky), Brick(4, 5, tileFranky), Brick(4, 6, tileFranky), Brick(4, 7, tileFranky), Brick(4, 8, tileFranky), Brick(4, 9, tileFranky), Brick(4, 10, tileFranky), Brick(4, 11, tileFranky)];
bricksJump = [Brick(12, 12, tileFranky), Brick(12, 13, tileFranky), Brick(12, 14, tileFranky), Brick(12, 15, tileFranky), Brick(12, 16, tileFranky),Brick(12, 17, tileFranky), Brick(12, 18, tileFranky)];

franky = GameSprite(bricksStand, (100, 100));

moveRight = False;
moveLeft = False;
stand = True;
jump = False;
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
            elif (e.key == pygame.locals.K_UP):
                jump = True;
                stand = False; 
        elif (e.type == pygame.locals.KEYUP):
            if (e.key == pygame.locals.K_RIGHT):
                moveRight = False;
                stand = True;
            elif (e.key == pygame.locals.K_LEFT):
                moveLeft = False;
                stand = True;
            elif (e.key == pygame.locals.K_UP):
                jump = False;
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
    
    if (jump):
        franky.bricks = bricksJump;
        franky.setPosition((franky.pos[0], franky.pos[1]));
        franky.jump();