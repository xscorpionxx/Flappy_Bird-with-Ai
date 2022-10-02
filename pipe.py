from abc import ABC
from re import X
from bird import Bird
import pygame
import random
pipe_image = pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\pipe.png'))

class PipeABS(ABC) : 
    def __init__(self , x) -> None:
        super().__init__()
        pass
    def draw(self , surface : pygame.display): 
        pass
    def collide(self , bird) : 
        pass
    def set_height(self) : 
        pass
    def move(self) : 
        pass

class Pipe(PipeABS) : 
    def __init__(self, x) -> None:
        super().__init__(x)
        self.x = x 
        self.top = 0
        self.gap = 200
        self.vel = 5
        self.passed = False
        self.bottom = 0
        self.top_pipe = pygame.transform.flip(pipe_image , False ,True)
        self.bottom_pipe = pipe_image
        self.height = 0
        self.set_height()
    def set_height(self) : 
        self.height = random.randrange(50 , 450) 
        self.top = self.height - self.top_pipe.get_height()
        self.bottom = self.height + self.gap
    def draw(self, surface: pygame.display):
        surface.blit(self.top_pipe , (self.x , self.top))
        surface.blit(self.bottom_pipe , (self.x , self.bottom))

    def move(self) : 
        self.x -= self.vel

    def collide(self , bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)
        top_offset = (self.x - bird.x , self.top -round(bird.y))
        bottom_offset = (self.x - bird.x , self.bottom -round(bird.y))

        b_point = bird_mask.overlap(bottom_mask , bottom_offset)
        t_point = bird_mask.overlap(top_mask , top_offset)

        if t_point or b_point : 
            return True
        return False