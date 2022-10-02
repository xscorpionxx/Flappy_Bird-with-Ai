from numpy import float64
import pygame 
from abc import ABC



class BirdAbs(ABC) : 
    def __init__(self, x : int , y : int) -> None:
        super().__init__()
        pass
    def draw(self , surface : pygame.display) : 
        pass
    def move_up(self) : 
        pass
    def get_mask(self) : 
        pass
    def move_forward(self) :
        pass
Bird_images = [ pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\bird1.png')),
    pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\bird2.png')) ,
    pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\bird3.png'))]

class Bird(BirdAbs):
    MAX_ROTATION = 25
    ROT_VEL = 20 
        
    def __init__(self , x : int, y : int) -> None:
        super().__init__(x,y)
        self.x = x 
        self.y = y
        self.imgs = Bird_images 
        self.img_count = 0
        self.ANIMATION_TIME = 5
        self.tilt = 0
        self.height = y 
        self.vel = 0
        self.tick_count = 0
    def draw(self , surface : pygame.display ) :
        self.img_count +=1 
        if self.img_count < self.ANIMATION_TIME : 
            self.img =self.imgs[0]
        elif self.img_count < self.ANIMATION_TIME *2: 
            self.img =self.imgs[1]
        elif self.img_count < self.ANIMATION_TIME * 3 : 
            self.img =self.imgs[2]
        elif self.img_count < self.ANIMATION_TIME *4: 
            self.img =self.imgs[0]
        elif self.img_count < self.ANIMATION_TIME * 4 +1: 
            self.img =self.imgs[1]
            self.img_count =0                
        if self.tilt <= -80 : 
            self.img = self.imgs[1]
            self.img_count = self.ANIMATION_TIME *2
        rotated_img = pygame.transform.rotate(self.img , self.tilt)
        ### we need to rotate around the center
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft =(self.x ,self.y)).center)
        surface.blit(rotated_img , new_rect.topleft )
    
    
    def get_mask(self) : 
        return pygame.mask.from_surface(self.img)
    
    
    def jump(self) : 
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y   
         
    def move(self) :
        self.tick_count +=1 
        d = self.vel * self.tick_count + 1.5 * self.tick_count **2

        if d >= 16 : 
            d = 16
        if d < 0 : 
            d -= 2
        self.y = self.y + d
        
        if d < 0 or self.y < self.height + 50 :
            if self.tilt < self.MAX_ROTATION : 
                self.tilt = self.MAX_ROTATION
        else : 
            if self.tilt > -90 : 
                self.tilt -= self.ROT_VEL
    