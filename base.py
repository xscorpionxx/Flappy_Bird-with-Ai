from re import X
import pygame 
from abc import ABC 

base_image = pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\base.png'))

class BaseABS(ABC) :
    def __init__(self) -> None:
        super().__init__()
        pass
    def draw(self , surface : pygame.display) : 
        pass
    def move(self) : 
        pass

class Base(BaseABS) :
    vel = 5
    width = base_image.get_width() 
    def __init__(self , y) -> None:
        super().__init__()
        self.y = y 
        self.x1 = 0
        self.x2 = self.width
        self.img = base_image
    def move(self) : 
        self.x1 -= self.vel
        self.x2 -= self.vel

        if self.x1 + self.width < 0 : 
            self.x1 = self.width -10
        if self.x2 + self.width < 0 : 
            self.x2 = self.width -10

    def draw(self , surface) : 
        surface.blit(self.img , (self.x1, self.y))
        surface.blit(self.img , (self.x2, self.y))


