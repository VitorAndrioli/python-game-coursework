import pygame;
from pygame import locals;
from tile import Tile;
from brick import Brick;
from gameSprite import GameSprite;

surface = pygame.display.set_mode((640, 480), 0, 32);
clock = pygame.time.Clock();

tileFranky = Tile("img/sprite2.png", 150, 150);

bricksStand = [Brick(0, 0, tileFranky), Brick(0, 1, tileFranky), Brick(0, 2, tileFranky), Brick(0, 3, tileFranky)];
bricksWalk = [Brick(4, 4, tileFranky), Brick(4, 5, tileFranky), Brick(4, 6, tileFranky), Brick(4, 7, tileFranky), Brick(4, 8, tileFranky), Brick(4, 9, tileFranky), Brick(4, 10, tileFranky), Brick(4, 11, tileFranky)];
bricksDuck = [Brick(12, 12, tileFranky)];
bricksJump = [Brick(13, 13, tileFranky), Brick(13, 14, tileFranky), Brick(13, 15, tileFranky), Brick(13, 16, tileFranky), Brick(13, 17, tileFranky), Brick(13, 18, tileFranky), Brick(13, 19, tileFranky)]

franky = GameSprite(bricksStand, (100, 200));

moveRight = False;
moveLeft = False;
duck = False;
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
                franky.counter = 0;
                moveRight = True;
            elif (e.key == pygame.locals.K_LEFT):
                franky.counter = 0;
                moveLeft = True;
            elif (e.key == pygame.locals.K_DOWN):
                franky.counter = 0;
                duck = True;
            elif (e.key == pygame.locals.K_UP):
                franky.counter = 0;
                jump = True;
        elif (e.type == pygame.locals.KEYUP):
            if (e.key == pygame.locals.K_RIGHT):
                franky.counter = 0;
                moveRight = False;
            elif (e.key == pygame.locals.K_LEFT):
                franky.counter = 0;
                moveLeft = False;
            elif (e.key == pygame.locals.K_DOWN):
                franky.counter = 0;
                duck = False;
            elif (e.key == pygame.locals.K_UP):
                franky.counter = 0;
                jump = False;
        elif (e.type == pygame.locals.QUIT):
            exit();
            
    
    if (jump):
        franky.bricks = bricksJump;
        
    elif (duck):
        franky.bricks = bricksDuck;
    
    elif (moveRight):
        if (not franky.right):
            franky.right = True;
        franky.setPosition((franky.pos[0]+8, franky.pos[1]));
        franky.bricks = bricksWalk;
        
    elif (moveLeft):
        if (franky.right):
            franky.right = False;
        franky.setPosition((franky.pos[0]-8, franky.pos[1]));
        franky.bricks = bricksWalk;
    else:
        franky.bricks = bricksStand;