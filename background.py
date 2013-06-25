import Box2D as b2;
import json;
from tile import Tile;
from brick import Brick;
import pygame;

class Background():
    def __init__(self, surface, world, PPM):
        self.world = world;
        self.surface = surface;
        self.PPM = PPM;
        
        self.index = 0;
        self.pos = (0, 0);
        self.bgSurface = pygame.Surface((16000, 608), 0, 32);

        self.loadObjects();
        self.getTileSet();
        
    def loadObjects(self):
        arquivo = open("json/back.json");
        jsonFile = json.load(arquivo);
        self.objects = [];
        for layer in jsonFile["layers"]:
            if (layer["type"] == "objectgroup"):
                objects = layer["objects"];
                for obj in objects:
                    self.objects.append(obj);
                    width = obj["width"] / self.PPM;
                    height = obj["height"] / self.PPM;
                    
                    x = self.pos[0] + ((obj["x"] / self.PPM) + width/2);
                    y = self.pos[1] + (obj["y"] / self.PPM) + height/2;
                    pos = (x, y);
                    
                    self.createBody(pos, width, height);
        
    def createBody(self, pos, width, height):
        
        bodyDef = b2.b2BodyDef();
        bodyDef.position = pos;
        bodyDef.type = b2.b2_staticBody;
        bodyDef.angle = 0;
        self.body = self.world.CreateBody( bodyDef );
        self.body.userData = {"name": "floor"};
        
        bodyFixture = b2.b2FixtureDef();
        bodyFixture.shape = b2.b2PolygonShape( box=(width/2, height/2));
        bodyFixture.restitution = 0;
        bodyFixture.friction = 0.5;
        
        self.body.CreateFixture( bodyFixture );
    
        
    def getTileSet(self):        
        arquivo = open("json/back.json");
        jsonFile = json.load(arquivo);
        
        for layer in jsonFile["layers"]:
            if (layer["type"] == "tilelayer"):
                self.data = layer["data"];
                self.coluns = layer["width"];
                self.lines = layer["height"];
                tileSets = jsonFile["tilesets"];
                for ts in tileSets:
                    tileImage = ts["image"];
                    tileWidth = ts["tilewidth"];
                    tileHeight = ts["tileheight"];
                    self.tileSet = Tile(tileImage, tileWidth, tileHeight);
        
        self.drawBackground();
        
    def drawBackground(self):
        self.index = 0;
        for l in range(self.lines):
            for c in range(self.coluns):
                x = c*32;
                y = l*32;
                gid = self.data[self.index]-1;
                if (gid >= 0):
                    self.bgSurface.blit(Brick(0, gid, self.tileSet).getImage(), (x, y));
                self.index+=1;
                
    def update(self):
        self.surface.blit(self.bgSurface, self.pos);
        
    def move(self, dir):
        if (dir =="right"):
            self.pos = (self.pos[0] - 2, self.pos[1]);
        else:
            self.pos = (self.pos[0] + 2, self.pos[1]);
            