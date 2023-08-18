import numpy as np
import random as rand
from GameLogic import Game, Snake
import math

HIDDENLAYERSIZE = 11

VIEWSIZENUM=5
VIEWSIZE=[int(0-math.floor(VIEWSIZENUM/2)),int(math.ceil(VIEWSIZENUM/2))]

class Brain:
    #https://www.youtube.com/watch?v=SGxVaptD9Ug 
    #Huge shoutout to this youtube video which helped a lot with making this part
    def __init__(self, input_size, hidden_size, output_size):
        #generate random starting points for the matrix
        self.hiddenlayer1=np.array([[rand.uniform(-1,1) for _ in range(input_size+1)] for _ in range(hidden_size)])
        self.hiddenlayer2=np.array([[rand.uniform(-1,1) for _ in range(hidden_size+1)] for _ in range(hidden_size)])
        self.outputlayer=np.array([[rand.uniform(-1,1) for _ in range(hidden_size+1)] for _ in range(output_size)])
    def determineMove(self, game: Game, snake:Snake):

        #The snake can see a 5x5(can be changed) around the head and the direction of the food 
        inputVector=[]
        head = snake.bodySegments[snake.headIndex]
        for i in range(VIEWSIZE[0],VIEWSIZE[1]):#offset x
            for j in range(VIEWSIZE[0],VIEWSIZE[1]):#offset y
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
       
        #Give the position of the food on the map to input, 
        vector=np.array([game.foodPos[0]-head[0], game.foodPos[1]-head[1]])
        vector = vector/np.linalg.norm(vector)
        inputVector.append(vector[0])
        inputVector.append(vector[1])

        inputVector+=[1]
        #Get output from input, multiply the matrix and squish the output down with tanh (todo lookup how to actually calc tanh)
        hiddenResult1= np.array([math.tanh(np.dot(inputVector,self.hiddenlayer1[i])) for i in range(self.hiddenlayer1.shape[0])]+ [1])#[1] is for bias, todo read up
        hiddenResult2= np.array([math.tanh(np.dot(hiddenResult1,self.hiddenlayer2[i])) for i in range(self.hiddenlayer2.shape[0])]+ [1])#[1] is for bias, todo read up
        outputResult= np.array([np.dot(hiddenResult2,self.outputlayer[i]) for i in range(self.outputlayer.shape[0])])
       
        #return the direction to move in 
        return np.argmax(outputResult)


                                



    
class Population:
    def __init__(self, popSize, mutationChance, mutationSize):
        self.pop = np.array([Brain((VIEWSIZENUM*VIEWSIZENUM)+2,HIDDENLAYERSIZE,4) for _ in range(0,popSize)])
        self.mutationChance =mutationChance
        self.mutationSize=mutationSize
        self.scores= np.array([[0,0]]*popSize)

    def Reproduce(self, scores):
        newpop=[]
        amount = int(len(self.pop)/4)
        #take top 25% 
        #TODO implement different ways of mutation like crossover
        for i in range (0,amount):
            newpop.append(self.pop[scores[i][1]])#winners get to live


            newpop.append(Brain((VIEWSIZENUM*VIEWSIZENUM)+2,HIDDENLAYERSIZE,4))#append some new brains as well
        for i in range(0,1):#mutate the winners 2 different times, i dont know whats best i am just making this up
            for j in range (0,amount):
                newpop.append(self.Mutate(self.pop[scores[j][1]]))
                newpop.append(self.Mutate(self.pop[scores[j][1]]))
        self.pop=np.array(newpop)
        


    def Mutate(self,brain: Brain):
        layers = [np.copy(brain.hiddenlayer1), np.copy(brain.hiddenlayer2), np.copy(brain.outputlayer)]#easy to loop
        for layer in layers:
            for i in range(0,layer.shape[0]):
                for j in range(0,layer.shape[1]):
                    #loop over each matrix and mutate the values
                    if(rand.uniform(0,1)< self.mutationChance):
                        layer[i][j] += rand.uniform(-1,1)*self.mutationSize
        brain= Brain.__new__(Brain)
        brain.hiddenlayer1=layers[0]
        brain.hiddenlayer2=layers[1]
        brain.outputlayer=layers[2]
        return brain


        
    def Cycle(self, gameSize):
        for i in range(0,self.pop.shape[0]):

            score = 0
        
            game = Game(gameSize,gameSize)
            game.snake.brain=self.pop[i]
            iter = 0
            
            while iter<500 and game.dead!=True:
                game.Cycle(game.snake.brain.determineMove(game,game.snake))#todo: refactor this is getting out of hand lmao
                iter+=1
            score+=len(game.snake.bodySegments)#could be expanded upon with lifetime?

            self.scores[i] = [score,i]
        sorted_scores =  self.scores[ self.scores[:, 0].argsort()]#https://stackoverflow.com/questions/22698687/how-to-sort-2d-array-numpy-ndarray-based-to-the-second-column-in-python
        #print(self.scores)
        return sorted_scores[::-1] #reverse it
