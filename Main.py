import os,time
import msvcrt #keyboard stuff
import Graphics
from GameLogic import Game
from Genetics import Brain, Population
import numpy as np
import easygui

GAMESIZE = 20

def main():

    userInput=""
    while (userInput != "1" and userInput !="2" and userInput != "3"):
        userInput = input("Select Game type, 1: Manual play, 2:Train AI, 3:Replay AI from file\n")
    if(userInput=="1"):
        game = Game(GAMESIZE,GAMESIZE)
        Graphics.initalDraw(game)
        previousDirection=0#default up
        while True:
            direction = getUserInput()
            if(direction==99):
                direction=previousDirection
            
            game.Cycle(direction)
            Graphics.UpdateGame(game)
            


            previousDirection=direction
            time.sleep(0.5)
    elif(userInput=="2"):
    
        pop= Population(100,0.1,0.1)
        gens = 1
        while True:
            print("Running Generation "+str(gens))
            result =pop.Cycle(GAMESIZE)
            print("Top 5 snakes had scores:", end="")
            for i in range(0,5):
                print(" " + str(result[i]), end =" ")
            print("")
            pop.Reproduce(result)
    
            if(gens%100 == 0):
                if not os.path.exists("brains/gen"+str(gens)):
                    os.makedirs("brains/gen"+str(gens))
                    for i in range(0,5):
                        snake = pop.pop[result[i][1]]
                        np.savetxt("brains/gen"+str(gens)+"/l1"+str(i)+".txt", snake.hiddenlayer1)
                        np.savetxt("brains/gen"+str(gens)+"/l2"+str(i)+".txt", snake.hiddenlayer2)
                        np.savetxt("brains/gen"+str(gens)+"/l3"+str(i)+".txt", snake.outputlayer)
            gens+=1
    else:
        path = easygui.fileopenbox()
        #pathsplit = path.split("\\")
        #path = path[:-len(pathsplit[len(pathsplit)-1])]
        brain = Brain.__new__(Brain)
        index = len(path)-6
        path1=path[:index] + str(1) + path[index + 1:]
        path2=path[:index] + str(2) + path[index + 1:]
        path3=path[:index] + str(3) + path[index + 1:]
        print(path1)
        print(path2)
        print(path3)
        input()
        brain.hiddenlayer1 =np.loadtxt(path1)
        brain.hiddenlayer2 =np.loadtxt(path2)
        brain.outputlayer =np.loadtxt(path3)
        game = Game(GAMESIZE,GAMESIZE)
        game.snake.brain=brain
        Graphics.initalDraw(game)
        while True:

            inputVector=[]
            game.Cycle(game.snake.brain.determineMove(game,game.snake))
            head = game.snake.bodySegments[game.snake.headIndex]
            for i in range(-2,3):
                for j in range(-2,3):
                    pos = [head[0]+i, head[1]+j]
                    if(pos[0]<0 or pos[1] < 0 or pos[0]>= game.width or pos[1]>=game.height):
                        inputVector.append(-1)#wall bad
                    else:
                        if(game.map[pos[0]][pos[1]]==0):
                            inputVector.append(0)#nothing neutral
                        elif(game.map[pos[0]][pos[1]]==3):
                            inputVector.append(1)#food good
                            
                        else:
                            inputVector.append(-1)#self bad


            
             
            Graphics.UpdateGame(game)
            Graphics.debugAI(inputVector)
            time.sleep(0.08)
            
            #input()
            if(game.dead==True):
                exit()

        


def getUserInput():
    if(msvcrt.kbhit()):#if there is a input to read, so the main loop isnt stopped
        key = ord(msvcrt.getch())
        if(key==27):
            exit()
        if(key == 224):#Special input key check
            keycode = ord(msvcrt.getch())
            match keycode:
                case 75:#left
                    return 0
                case 72:#up
                    return 1 
                case 77:#right
                    return 2 
                case 80:#down
                    return 3
    else:
        return 99





main()