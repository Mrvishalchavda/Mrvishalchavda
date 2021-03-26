import random
import pygame
import sys
from pygame.locals import *

# global variyable for Game
fps = 32
screenwidth = 720
screenheight = 576
screen = pygame.display.set_mode((screenwidth,screenheight))
game_sprite = {}
game_sprite['player'] = pygame.image.load('images/birdsing.png').convert_alpha()
game_sprite['welcome'] = pygame.image.load("images/wecome screen.jpg").convert()
game_sprite['bg'] = pygame.image.load("images/bg.jpg").convert_alpha()
game_sprite['pipeup'] = pygame.image.load("images/tube1.png").convert_alpha()
game_sprite['pipedown'] = pygame.image.load("images/tube2.png").convert_alpha()
game_sprite['numbers'] = (pygame.image.load("images/0.png").convert_alpha(),
                        pygame.image.load("images/1.png").convert_alpha(),
                        pygame.image.load("images/2.png").convert_alpha(),
                        pygame.image.load("images/3.png").convert_alpha(),
                        pygame.image.load("images/4.png").convert_alpha(),
                        pygame.image.load("images/5.png").convert_alpha(),
                        pygame.image.load("images/6.png").convert_alpha(),
                        pygame.image.load("images/7.png").convert_alpha(),
                        pygame.image.load("images/8.png").convert_alpha(),
                        pygame.image.load("images/9.png").convert_alpha() )
game_sprite['base'] = pygame.image.load("images/base.png").convert_alpha()

def welcomeScreen():
    playerx = int((screenwidth-game_sprite['player'].get_width())/2)
    playery = int((screenheight-game_sprite['player'].get_height())/2)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and ( event.key ==pygame.K_UP or event.key ==pygame.K_SPACE):
                maingame()
            else:
                screen.blit(game_sprite['welcome'],(0,0))
                screen.blit(game_sprite['player'],(playerx,playery))
        

                pygame.display.update()

def maingame():
    score = 0
    upperpipe = []
    lowerpipe = []
    for i in range(3):
        pipe = getrandompipe()
        upperpipe.append ({'x':screenwidth-(i*170), 'y':pipe[0]['y']})
        lowerpipe.append({'x':screenwidth-(i*170), 'y':pipe[1]['y']})
    upperpipe.reverse()
    lowerpipe.reverse()
    print(f"upper pipe list is {upperpipe}")
    pipevelx = -4
    testpipe = zip(upperpipe,lowerpipe)
    test_pipe =list(testpipe)
    # print(test_pipe)
    playerx = int(screenwidth/5)
    
    playery = int((400-game_sprite['player'].get_height())/2)
    playervely = -9
    playermaxvaly = 10
    playerminvaly = -8
    playeraccy = 1
    playerflappedaccv = -8
    playersignal = False
    while True:
        # print(f"your final lisst is\n{test_pipe}")
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key ==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and ( event.key == pygame.K_SPACE or event.key == pygame.K_UP):
                playervely = playerflappedaccv
                playersignal = True
                # print(f"current velocity when press up key {playervely}")

        if playervely<playermaxvaly and not playersignal:
            playervely += playeraccy            
            # print(f"velocity {playervely} and player y value is {playery}")
        if  playersignal:
            playersignal = False
        playery = playery + min(playervely, (420-playery-(game_sprite['player'].get_height())))
        # print(playery) 

        # moving pipe
        
        for upperPipe , lowerPipe in test_pipe:            
            upperPipe['x'] += pipevelx
            lowerPipe['x'] += pipevelx
        
        # add new pipe
        i = len(upperpipe)
        i -= 1
        # print(i)
        # print(upperpipe[(i)]['x'])
        if (720 - upperpipe[i]['x'] >= 170):
            npipe=getrandompipe()
            upperpipe.append ({'x': 720, 'y':npipe[0]['y']})
            lowerpipe.append({'x':720, 'y':npipe[1]['y']})
            # print(f"new pipe added in")
            # print(upperpipe)
        if upperpipe[0]['x'] <=-50:
            upperpipe.pop(0)
            lowerpipe.pop(0)
        testpipe = zip(upperpipe,lowerpipe)
        test_pipe =list(testpipe)

        if iscolide(playerx,playery,upperpipe,lowerpipe):
            print(f"game over at score {score}")
            break
        
        # score 
        playermidpoint = playerx+(game_sprite['player'].get_width()/2)
        pipewith = game_sprite['pipeup'].get_width()/2
        for up in range(2):
            if playermidpoint <upperpipe[up]['x']< playermidpoint+5:
                score += 1
                print(f"your score is {score} ")

        # generat frams by bliting
        screen.blit(game_sprite['bg'],(0,0))
        for lowerpipe1, upperpipe1 in test_pipe:
            #  print(f"up {upperpipe['x']} , {upperpipe['y']}")
            # print(f"down {lowerpipe['x']} , {lowerpipe['y']}")
            screen.blit(game_sprite['pipeup'],(upperpipe1['x'],upperpipe1['y']))
            screen.blit(game_sprite['pipedown'],(lowerpipe1['x'],lowerpipe1['y']))

        screen.blit(game_sprite['player'],(playerx,playery))
        mydigit = [int(x) for x in list(str(score))]
        withscrore =0
        for digit in mydigit:
            withscrore = withscrore + game_sprite['numbers'][digit].get_width()
        scoreoffset = (screenwidth -withscrore)/2
        for digit in mydigit:
            screen.blit(game_sprite['numbers'][digit],(scoreoffset,75))
            scoreoffset += game_sprite['numbers'][digit].get_width()
        screen.blit(game_sprite['base'],(0,420))
        pygame.display.update()
        fpsclock.tick(fps)
        # print("first sicle over")


def getrandompipe():
    pipeheight = game_sprite['pipeup'].get_height()
    offset = 100
    pipex = screenwidth+10
    pipey = random.randrange(120, 400)
    # pipey2 =random.randrange(100,280)
    # if pipey - pipey2 <80:
    pipey2 = pipey-80-pipeheight 
    # print(f"lower pipe {pipey} & upperpipe {pipey2+pipeheight} ")
    return [{'x':pipex, 'y':pipey},{'x':pipex, 'y':pipey2}]


def iscolide(px, py, up ,dp):
    revalue = False
    print(revalue)
    pmidpointx = px - (game_sprite['player'].get_width()/2)
    pmidpointy = py - (game_sprite['player'].get_height()/2)
    for upper , lower in zip(up,dp):
        # print(f"valu of up is {upper}, and {lower}")
        # print(f"checking pipe with {pmidpointx} & pipe valu is {upper['x']} & {upper['x'] + game_sprite['pipeup'].get_width()}")
        if   upper['x'] < pmidpointx < upper['x'] + game_sprite['pipeup'].get_width():
            # print("running first if")
            if   upper['x'] < pmidpointx < upper['x'] + game_sprite['pipeup'].get_width():
            # print("running first if")
            print(f"checking pipe with {int(pmidpointy)} & pipe valu is {lower['y'] + game_sprite['pipeup'].get_height()} & {upper['y']}")
            if int(lower['y'] + game_sprite['pipeup'].get_height()) > int(pmidpointy) or int(pmidpointy) > upper['y']:
                revalue = True
                print("its your fault")
                # (lower['y'] + game_sprite['pipeup'].get_height()) < 
    # print(f"player x position is ({px},{py}) & {game_sprite['player'].get_width()} ,{game_sprite['player'].get_height()}")
    # print(f"player x position is ({pmidpointx},{pmidpointy})\n upperpipe list is{up}\n downpipe list is{dp}")
    return revalue


if __name__ == "__main__":
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption("flappy game by vishal chavda")
    

    while True:
        welcomeScreen()
        maingame()
