import pygame;
from pygame import locals;
from tile import Tile;
from brick import Brick;
from gameSprite import GameSprite;

surface = pygame.display.set_mode((640, 480), 0, 32);
clock = pygame.time.Clock();

tileFranky = Tile("img/sprite_t.png", 240, 190);

bricksStand = [Brick(0, 0, tileFranky), Brick(1, 1, tileFranky), Brick(2, 2, tileFranky), Brick(3, 3, tileFranky)];

franky = GameSprite(bricksStand, (100, 100));

while(True):
    
    surface.fill((0, 0, 0));
    franky.update();
    franky.render(surface);
    
    pygame.display.update();
    clock.tick(5);
    
    for e in pygame.event.get():
        if e.type == pygame.locals.QUIT:
            exit();