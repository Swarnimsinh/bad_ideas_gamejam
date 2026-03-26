import pygame
import os
GRAVITY = 1
PLAYER_VEL = -10
pygame.init()
class Player(pygame.Rect):
    #pygame.draw.rect(screen, color, rect)and pygame.Rect diffrece todo->dynamically find size of image and 
    # put accodingly even option toscale

    def loadspritesheet(self,path,framefat,frameheight):
        sheet=pygame.image.load(path).convert_alpha()
        frames=[]

        fulllen= sheet.get_width()
        fullwidth=sheet.get_height()
        for i in range(0,fulllen,framefat):
            if i + framefat <= fulllen:  #stupid condition for overflow
                frame = sheet.subsurface((i, 0, framefat, frameheight))
                frames.append(frame)

        return frames


    def __init__(self,gamewindow,startx,starty,fat,tall,tiles):
        self.gamewindow=gamewindow
        self.tiles=tiles
        
        BASE_DIR = os.path.dirname(__file__)
        # player_L=pygame.image.load(image)
        self.walk_frames = self.loadspritesheet(os.path.join(BASE_DIR, "caracter", "walk.png"), 32,32)
        self.jump_frames = self.loadspritesheet(os.path.join(BASE_DIR, "caracter", "jumpframe.png"), 20, 35)

        self.imageR = pygame.image.load(os.path.join(BASE_DIR, "caracter", "guy.png"))
        self.imageL = pygame.transform.flip(self.imageR, True, False)
        self.image = self.imageR
        self.direction = "left"

        self.idle_frame = pygame.image.load(os.path.join(BASE_DIR, "caracter", "guy.png")).convert_alpha()

        # Flip versions for animation some advance python code must undestand more
        self.walk_frames_L = [pygame.transform.flip(f, True, False) for f in self.walk_frames]
        self.jump_frames_L = [pygame.transform.flip(f, True, False) for f in self.jump_frames]

        # Animationstate
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 0.2

        self.image = self.idle_frame
        self.direction = "right"
        
        self.vel_x = 0
        self.vel_y = 0
        pygame.Rect.__init__(self,startx,starty,fat,tall)

        #todo remove the player as in idle already passed him/her
    
    def update_direction(self,speed):
        #is this neeeded now ? todo justv see

        if self.direction == "right":
            self.image = self.imageR
        elif self.direction == "left":
            self.image = self.imageL

    def collision(self):
        # horizontal
        self.x += self.vel_x
        for tile in self.tiles:
            if self.colliderect(tile):
                if self.vel_x > 0:  # moving right
                    self.right = tile.left
                elif self.vel_x < 0:  # moving left
                    self.left = tile.right
                self.vel_x = 0

        # vertical
        self.y += self.vel_y
        for tile in self.tiles:
            if self.colliderect(tile):
                if self.vel_y > 0:  # falling
                    self.bottom = tile.top
                elif self.vel_y < 0:  # jumping
                    self.top = tile.bottom
                self.vel_y = 0
        
    def movement(self,speed):

        keys=pygame.key.get_pressed()
        
        self.vel_x = 0
        moving=False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "right"
            moving=True
            self.x=max(0,self.x-speed)
        # if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            # self.y=min(self.y+speed,self.gamewindow.get_height()-self.height)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "left"
            moving=True
            self.x=min(self.x+speed,self.gamewindow.get_width()-self.width)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()
            moving=True

        # STATE LOGIC for which spritesheet to choose in animation bro
        if self.vel_y != 0:
            self.state = "jump"
        elif moving:
            self.state = "walk"
        else:
            self.state = "idle"



    def jump(self):
        # Only jump if standing on a tile or ground
        on_ground = self.bottom >= self.gamewindow.get_height()
        for tile in self.tiles:
            if self.bottom == tile.top and self.right > tile.left and self.left < tile.right:
                on_ground = True
        if on_ground:
            self.vel_y = PLAYER_VEL    
        # if self.bottom >= self.gamewindow.get_height() - 24:
        #     self.vel = PLAYER_VEL
    def move(self):      
        self.vel_y += GRAVITY
        self.y += self.vel_y

        self.collision()
    
        # ground collision for now later blocks too
        if self.bottom >= self.gamewindow.get_height():
            self.bottom = self.gamewindow.get_height()
            self.vel_y = 0


    def draw(self):
        # SELECT ANIMATION
        if self.state == "walk":
            frames = self.walk_frames if self.direction == "right" else self.walk_frames_L
        elif self.state == "jump": #need to edit as jump i sjust 1 image now todo
            frames = self.jump_frames if self.direction == "right" else self.jump_frames_L
        else:
            self.image = self.idle_frame
            self.gamewindow.blit(self.image, self.topleft)
            return

        # ANIMATE logic still uncler gotta study more nad again
        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames): #modulo if over 8 go to 0 type shit
            self.frame_index = 0

        self.image = frames[int(self.frame_index)] #decimal to whole number

        self.gamewindow.blit(self.image, self.topleft)
"""must find some way to find x and y position to update it and 
 in rect it was as simple as rect.x nad rect.y to find x and y
 lol turns out sisnce i inherted rect so i can directly call rect.x lol 
 yahooooooo
 

 #def draw(self):
     #   self.gamewindow.blit(self.image,(self.topleft))
 old simple draw is gone now animation wala draw will come
 """


       
      
