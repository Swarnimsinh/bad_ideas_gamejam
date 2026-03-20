import pygame

class Player:
    #pygame.draw.rect(screen, color, rect)and pygame.Rect diffrece todo->dynamically find size of image and 
    # put accodingly even option toscale
    def __init__(self,gamewindow,startx,starty,fat,tall,image,colour):
        caracter=pygame.Rect(startx,starty,fat,tall) #makes a rectange in topleft part in x,y of fat*tall size
        pygame.draw.rect(gamewindow,colour,caracter)

"""(function) def rect(
    surface: Surface,
    color: ColorValue,
    rect: RectValue,
    width: int = 0,
    border_radius: int = -1,
    border_top_left_radius: int = -1,
    border_top_right_radius: int = -1,
    border_bottom_left_radius: int = -1,
    border_bottom_right_radius: int = -1
) -> Rect"""


    
