import os
from bird import Bird
import pygame
import neat
import pickle
from pipe import Pipe
from base import Base


class FlappyBird_game() :
    bg_image = pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\bg.png')) 
    def __init__(self , width , height , win) -> None:
        pygame.font.init()
        self.width = win 
        self.height = height 
        self.win = win
        self.Fontstate = pygame.font.SysFont("comicsans" , 50)
        self.score = 0
        self.flag = True
        self.pipes = [Pipe(300)]
        self.bird = Bird(100 ,300)
        self.base = Base(730)
    def draw(self , bird , base , pipes ) :
        self.win.blit(self.bg_image , (0,0))
        for pipe in pipes : 
            pipe.draw(self.win)
        bird.draw(self.win)
        base.draw(self.win)

        text  =self.Fontstate.render("score : " + str(self.score) ,1,  (255,255,255) )
        self.win.blit(text, (500 -10 - text.get_width(),10))  
        pygame.display.update()

    def move(self , base , pipes , bird ,AI) : 
        base.move()
        rem = []
        addpipe = False
        for pipe in pipes : 
            pipe.move()
            if pipe.collide(bird):
                self.resetgame()
                print("lose")
            if pipe.x + pipe.top_pipe.get_width() < 0 : 
                    rem.append(pipe)
            if not pipe.passed and bird.x > pipe.x :
                self.score +=1
                pipe.passed = True
                addpipe = True
        if addpipe : 
            pipes.append(Pipe(600))
        for r in rem : 
            pipes.remove(r)
        bird.move()
        if bird.y + bird.img.get_height() >= 730 or bird.y < 0 : 
            self.resetgame()
            print("lose")
        self.player_move(AI)
    
    def test_ai(self ,model , config) :
        self.nn =  neat.nn.FeedForwardNetwork.create(model, config)
        clock = pygame.time.Clock()
        while self.flag :
            clock.tick(30) 
            self.draw(self.bird , self.base, self.pipes )
            self.move(self.base , self.pipes , self.bird ,True ) 
    
        

    def play(self ):
        clock = pygame.time.Clock()
        while self.flag :
            clock.tick(30) 
            self.draw(self.bird , self.base, self.pipes )
            self.move(self.base , self.pipes , self.bird , False ) 

    def player_move(self , AI) :
        for event in pygame.event.get() : 
            if event.type == pygame.QUIT : 
                pygame.quit()
        if not AI : 
            keys = pygame.key.get_pressed()
            for key in keys : 
                if keys[pygame.K_UP] : 
                   self.bird.jump()
        else :
            pipe_ind = 0
            if len(self.pipes) > 1 and self.bird.x > self.pipes[0].x + self.pipes[0].top_pipe.get_width():  # determine whether to use the first or second
                 pipe_ind = 1 
            output = self.nn.activate((self.bird.y, abs(self.bird.y - self.pipes[pipe_ind].height), abs(self.bird.y - self.pipes[pipe_ind].bottom)))

            if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                self.bird.jump()   
    
    def resetgame(self) :
       self.pipes = [Pipe(300)]
       self.bird = Bird(100 ,300)
       self.base = Base(730)
       self.score = 0

class FlappyBird_trainai() :
    bg_image = pygame.transform.scale2x(pygame.image.load(r'C:\Users\abd\python_training\flappy bird 2\img\bg.png')) 
    
    def __init__(self , width , height , win , config_path ,num_of_pop) -> None:
        pygame.font.init()
        self.width = win 
        self.height = height 
        self.win = win
        self.config_path = config_path
        self.num_of_pop = num_of_pop
        self.Fontstate = pygame.font.SysFont("comicsans" , 50)
        self.score = 0
        self.flag = True
        self.pipes = [Pipe(300)]
        self.base = Base(730)
        self.Gen = 0
        self.DRAW_LINES = False
        self.run()



   
    def draw_window(self,win, birds, pipes, base, score, gen, pipe_ind):
            if gen == 0:
                gen = 1
            win.blit(self.bg_image, (0,0))
            base.draw(win)
            for pipe in pipes:
                pipe.draw(win)

            base.draw(win)
            for bird in birds:
                # draw bird
                bird.draw(win)

            # score
            score_label = self.Fontstate.render("Score: " + str(score),1,(255,255,255))
            win.blit(score_label, (500 - score_label.get_width() - 15, 10))

            # generations
            score_label = self.Fontstate.render("Gens: " + str(gen-1),1,(255,255,255))
            win.blit(score_label, (10, 10))

            # alive
            score_label = self.Fontstate.render("Alive: " + str(len(birds)),1,(255,255,255))
            win.blit(score_label, (10, 50))

            pygame.display.update()

    def eval_genoms(self ,genoms , config):
        self.Gen += 1

        # start by creating lists holding the genome itself, the
        # neural network associated with the genome and the
        # bird object that uses that network to play
        nets = []
        birds = []
        ge = []
        for genome_id, genome in genoms:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            birds.append(Bird(230,350))
            ge.append(genome)

        base = Base(730)
        pipes = [Pipe(700)]
        score = 0

        clock = pygame.time.Clock()

        run = True
        while run and len(birds) > 0:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                    break

            pipe_ind = 0
            if len(birds) > 0:
                if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].top_pipe.get_width():  # determine whether to use the first or second
                    pipe_ind = 1                                                                 # pipe on the screen for neural network input

            for x, bird in enumerate(birds):  # give each bird a fitness of 0.1 for each frame it stays alive
                ge[x].fitness += 0.1
                bird.move()

                # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
                output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

                if output[0] > 0.5:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                    bird.jump()

            base.move()
            self.draw_window(self.win, birds, pipes, base, score, self.Gen, pipe_ind)
            rem = []
            add_pipe = False
            for pipe in pipes:
                pipe.move()
                # check for collision
                for bird in birds:
                    if pipe.collide(bird):
                        ge[birds.index(bird)].fitness -= 1
                        nets.pop(birds.index(bird))
                        ge.pop(birds.index(bird))
                        birds.pop(birds.index(bird))

                if pipe.x + pipe.top_pipe.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if add_pipe:
                score += 1
                # can add this line to give more reward for passing through a pipe (not required)
                for genome in ge:
                    genome.fitness += 5
                pipes.append(Pipe(700))

            for r in rem:
                pipes.remove(r)

            for bird in birds:
                if bird.y + bird.img.get_height() - 10 >= 730 or bird.y < -50:
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
            if score > 5 : 
                break

        
    def run(self,):
        config = neat.Config(neat.DefaultGenome , neat.DefaultReproduction ,
        neat.DefaultSpeciesSet , neat.DefaultStagnation , 
        self.config_path)
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        ##### 50 is the maximum generations we will run
        winner = p.run(self.eval_genoms , self.num_of_pop)
        local_dir = os.path.dirname(__file__)
        winner_path = os.path.join(local_dir , "best.pickle")
        with open(winner_path, "wb") as f:
            pickle.dump(winner, f)




        


            

        

def test_ai() :
    local_dir = os.path.dirname(__file__)
    config = os.path.join(local_dir , 'config-feedforward.txt')
    width = 500
    height = 800
    win = pygame.display.set_mode((width , height))
    try : 
        path = os.path.join(local_dir , 'best.pickle')
        with open(path, "rb") as f:
            winner = pickle.load(f)
    except Exception as e : 
        print(e.args)
    config = neat.Config(neat.DefaultGenome , neat.DefaultReproduction ,
        neat.DefaultSpeciesSet , neat.DefaultStagnation , 
        config)
    flapy = FlappyBird_game(width , height , win)
    flapy.test_ai(winner , config)

def train_ai():
    width = 500
    height = 800
    win = pygame.display.set_mode((width , height))
    local_dir = os.path.dirname(__file__)
    config = os.path.join(local_dir , 'config-feedforward.txt')
    width = 500
    height = 800
    Ai = FlappyBird_trainai(width ,height , win , config ,2)

def play():
    width = 500
    height = 800
    win = pygame.display.set_mode((width , height))
    flapy = FlappyBird_game(width , height , win)
    flapy.play()


if __name__ == '__main__' : 
    #### if you want to play 
    #play()
    ###### if you want to test ai 
    test_ai()
    ###### if you want to train the ai
    #train_ai()
    