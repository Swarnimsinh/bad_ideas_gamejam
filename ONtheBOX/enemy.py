import pygame
import os
# from player import Player

class Enemy(pygame.Rect):
    
    def loadspritesheet(self,path,framefat,frameheight, scale=1):
        sheet=pygame.image.load(path).convert_alpha()
        frames=[]

        fulllen= sheet.get_width()
        fullheight=sheet.get_height()
        for i in range(0,fulllen,framefat):
            if i + framefat <= fulllen:  #stupid condition for overflow
                frame = sheet.subsurface((i, 0, framefat, frameheight))
                
                if scale != 1:
                    frame = pygame.transform.scale(
                        frame,
                        (int(framefat * scale), int(frameheight * scale))
                    )
                frames.append(frame)
                  
        return frames


    def __init__(self,gamewindow,startx,starty,fat,tall,RATIO=None,colour=None):
        pygame.Rect.__init__(self,startx,starty,fat,tall)
        self.gamewindow=gamewindow
        self.image=None
        self.colour=None
        BASE_DIR = os.path.dirname(__file__)
        
        self.idle_frames = self.loadspritesheet(os.path.join(BASE_DIR, "enemies", "meow.png"),32,28,scale=2)
        self.scratch_frames = self.loadspritesheet(os.path.join(BASE_DIR, "enemies", "monster.png"), 32,28,scale=2)
        
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.idle_frames[0]
        
        self.vel_x = 0
        self.vel_y = 0
        pygame.Rect.__init__(self,startx,starty,fat,tall)
       
    def update(self, player):
        if self.colliderect(player):
            self.state = "scratch"
        else:
            self.state = "idle"   
            
    def draw(self):

        if self.state == "idle":
            frames = self.idle_frames
        elif self.state == "scratch":
            frames = self.scratch_frames

        # ANIMATE (for both states)
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        self.image = frames[int(self.frame_index)]

        self.gamewindow.blit(self.image, self.topleft)
