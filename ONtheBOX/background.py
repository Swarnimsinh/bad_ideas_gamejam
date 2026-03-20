import pygame
class Background:
    """simple add color/none(tuple or string) and image/none done then todo -> make dynamic bg scaling for diff size windows?"""
    def __init__(self,gamewindow,color,pictureofbackground):
        self.gamewindow=gamewindow.fill(color)