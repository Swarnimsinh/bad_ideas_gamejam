import pygame

class Stuff:
    def __init__(self,gamewindow,startx,starty,fat,tall,image,colour):
        self.caracter=pygame.Rect(startx,starty,fat,tall)  
        self.gamewindow=gamewindow
        self.colour=colour
            
    def draw(self):
        pygame.draw.rect(self.gamewindow,self.colour,self.caracter)


    
