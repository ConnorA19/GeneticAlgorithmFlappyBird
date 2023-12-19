import pygame, random, time
from pygame.locals import *
import pygame.freetype
import math
import matplotlib.pyplot as plt
import statistics

#VARIABLES
SCREEN_WIDHT = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 145


GENERATIONS = 100
BIRDCOUNT = 8

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        rand = random.randint(1,3)

        if rand == 1:
             self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
             
        elif rand == 2:
             self.images =  [pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()]

        else:
             self.images =  [pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha()]
       

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        #UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED + random.randint(1,6)
    

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]




class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        self.ysize = ysize
        pygame.sprite.Sprite.__init__(self)

        self. image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))


        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT  - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def printx(self):
        print(self.rect[0])
    def gety(self):
        return self.ysize

    def update(self):
        self.rect[0] -= GAME_SPEED

        

class Ground(pygame.sprite.Sprite):
    
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    def update(self):
        self.rect[0] -= GAME_SPEED
    def printx(self):
        print(self.rect[0])

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(200, 325)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

def combine(Genome1,Genome2):
    return ((Genome1[0] + Genome2[0]) // 2), (Genome1[1] + Genome2[1]) / 2, (Genome1[2] + Genome2[2])//2

def mutate(Genome, mutationSeverity):
   return Genome[0] + random.randint(-mutationSeverity,mutationSeverity), Genome[1] +  (0.01 * (random.randint(-mutationSeverity, mutationSeverity))), Genome[2] +  math.floor(0.5 * random.randint(-mutationSeverity, mutationSeverity))


def run(screen, BACKGROUND, BEGIN_IMAGE, bird_group, highestScoreGenomes, zeros, end, games, mutationSeverity):
    for generation in range(GENERATIONS):
        if end:
            break
        prevDistance = 1000
        birds = [Bird(), Bird(), Bird(), Bird(), Bird(), Bird(), Bird(), Bird()]
        birdScores = {}
        birdGenes = {}

        for bird in birds:
            bird_group.add(bird)
            birdScores[bird] = 0
            if zeros:
                highestScoreGenomes = (random.randint(-1000,1000), random.random(), random.randint(0,100)), (random.randint(-1000,1000), random.random(), random.randint(1,100))
            birdGenes[bird] = mutate(combine(highestScoreGenomes[0], highestScoreGenomes[1]), mutationSeverity)


        ground_group = pygame.sprite.Group()

        for i in range (2):
            ground = Ground(GROUND_WIDHT * i)
            ground_group.add(ground)

        pipe_group = pygame.sprite.Group()
        for i in range (2):
            pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        highest = bird_group.sprites()[0]
        second = bird_group.sprites()[1]

        clock = pygame.time.Clock()

        begin = True

        while begin:

            clock.tick(150)

            screen.blit(BACKGROUND, (0, 0))

            #screen.blit(BEGIN_IMAGE, (120, 150))

            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])

                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)

            
            for bird in birds:
                bird.begin()
            ground_group.update()

            bird_group.draw(screen)
            ground_group.draw(screen)

            pygame.display.update()

            begin = False



        zeros = True
        while bird_group.sprites():

            clock.tick(15)

            #differenceVector = (pipes[0].rect[0], pipes[0].rect[1] - bird1.rect[1])

            #print(pipe_group.sprites()[0].rect.x)
            
            for bird in bird_group.sprites():
                if ( (pipe_group.sprites()[0].rect.top - birdGenes[bird][0] < bird.rect.bottom) and (birdGenes[bird][2]) == 0 or pipe_group.sprites()[0].rect.x == 0):
                    bird.bump()
                    continue
                if ((pipe_group.sprites()[0].rect.top - birdGenes[bird][0] < bird.rect.bottom) and ((pipe_group.sprites()[0].rect.x % birdGenes[bird][2]) < PIPE_WIDHT)): 
                    if (pipe_group.sprites()[0].rect.right < 0):
                        if (birdGenes[bird][1] > 0.5):
                            bird.bump()
                        continue
                    bird.bump()
            
            
            if (pipe_group.sprites()[0].rect.right > prevDistance):
                for bird in bird_group.sprites():
                    birdScores[bird] += 1
                    zeros = False
                    print(str(pygame.time.get_ticks()))
            prevDistance = pipe_group.sprites()[0].rect.right


            #birds[0].rect.bottom = pipe_group.sprites()[0].rect.top


            
            if not bird_group.sprites():
                pygame.quit()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                # if event.type == KEYDOWN:
                #     if event.key == K_SPACE:
                #         bird_group.update()
                #         ground_group.update()
                #         pipe_group.update()
                #     if event.key == K_UP:
                #         bird_group.remove(bird_group.sprites()[0])


            screen.blit(BACKGROUND, (0, 0))



            if is_off_screen(ground_group.sprites()[0]):
                ground_group.remove(ground_group.sprites()[0])

                new_ground = Ground(GROUND_WIDHT - 20)
                ground_group.add(new_ground)

            if is_off_screen(pipe_group.sprites()[0]):
                pipe_group.remove(pipe_group.sprites()[0])
                pipe_group.remove(pipe_group.sprites()[0])

                pipes = get_random_pipes(SCREEN_WIDHT * 2)

                pipe_group.add(pipes[0])
                pipe_group.add(pipes[1])

            bird_group.update()
            ground_group.update()
            pipe_group.update()

            bird_group.draw(screen)
            pipe_group.draw(screen)
            ground_group.draw(screen)

            GAME_FONT = pygame.freetype.Font("arial.ttf", 14)
            if zeros:
               text_surface, rect = GAME_FONT.render("Genome Of Fittest in Last Generation: " + str(0) + " " + "0.0"  + " " + str(0), (0, 0, 0))
               text_surface2, rect = GAME_FONT.render("Genome Of Second Fittest in Last Generation: " + str(0) + " " + "0.0" + " " + str(0), (0, 0, 0))
            else:
                text_surface, rect = GAME_FONT.render("Genome Of Fittest in Last Generation: " + str(highestScoreGenomes[0][0]) + " " + "{:.2f}".format(highestScoreGenomes[0][1])  + " " + str(highestScoreGenomes[0][2]), (0, 0, 0))
                text_surface2, rect = GAME_FONT.render("Genome Of Second Fittest in Last Generation: " + str(highestScoreGenomes[1][0]) + " " + "{:.2f}".format(highestScoreGenomes[1][1])  + " " + str(highestScoreGenomes[0][2]), (0, 0, 0))
            text_surface3, rect = GAME_FONT.render("Generations: " + str(generation), (0,0,0))
            screen.blit(text_surface, (0, 0))
            screen.blit(text_surface2, (0,14))
            screen.blit(text_surface3,(0,28))

            pygame.display.update()


            for bird in bird_group.sprites():
                if birdScores[bird] >= 100:
                    end = True
                    # print("MAX SCORE REACHED IN " + str(generation + 1) + " GENERATIONS")
                    games.append(generation + 1)
                    pygame.quit()
                    return
                if (birdScores[bird] > birdScores[highest]):
                    highest = bird
                elif birdScores[bird] < birdScores[highest] and birdScores[bird] > birdScores[second] and highest != bird:
                    second = bird
            
            if birdScores[second] == 0:
                second = highest
            
            highestScoreGenomesThisGame = birdGenes[highest], birdGenes[second]


            for bird in bird_group.sprites():
                if (pygame.sprite.spritecollide(bird, ground_group, False,pygame.sprite.collide_mask)) or (pygame.sprite.spritecollide(bird, pipe_group, False, pygame.sprite.collide_mask)):
                    bird_group.remove(bird)
                #Remove bird if above screen
                if (bird.rect[1]) > SCREEN_HEIGHT:
                    bird_group.remove(bird)
                if (bird.rect[1]) < 0:
                    bird_group.remove(bird)
        
        highestScoreGenomes = highestScoreGenomesThisGame
mutationSeverityGenerations =[]
for mutationSeverity in range(0,10):
    games = []
    for game in range(10):
        pygame.init()
        pygame.font.init()
        screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')

        BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
        BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
        BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

        bird_group = pygame.sprite.Group()

        highestScoreGenomes = (random.randint(-1000,1000), random.random(), random.randint(0,100)), (random.randint(-1000,1000), random.random(), random.randint(1,100))
        zeros = True
        end = False

        run(screen, BACKGROUND, BEGIN_IMAGE, bird_group, highestScoreGenomes, zeros, end, games, mutationSeverity)

    print(str(mutationSeverity))
    mutationSeverityGenerations.append(statistics.mean(games))


# fig, ax = plt.subplots()

# ax.bar(range(0,10), mutationSeverityGenerations)

# ax.set_ylabel("Average Generations")
# ax.set_xlabel('Mutation Severity')
# ax.set_title('Mutation Severity vs. Average Generation')

# plt.show()

    





