import pygame;

class Tile():
    def __init__(self, fileAddress, width, height):
        self.width = width;
        self.height = height;
        self.image = pygame.image.load(fileAddress);
        self.list = [];
        
        maxX, maxY = self.image.get_size();
        coluns = maxX/self.width;
        lines = maxY/self.height;
        
        for l in range(lines):
            for c in range(coluns):
                x = c*width;
                y = l*height;
                subImage = self.image.subsurface(x, y, self.width, self.height);
                self.list.append(subImage);
                
    def getImage(self, index):
        return self.list[index];