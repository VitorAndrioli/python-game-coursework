#Classe para criar os Bricks do jogo

class Brick():
    def __init__(self, gid, index, tileSet):
        self.tile = tileSet;
        self.gid = gid;
        self.index = index;
        self.image = self.tile.getImage(self.index);
        (self.width, self.height) = self.image.get_size();
    
    def getImage(self):
        return self.image; 