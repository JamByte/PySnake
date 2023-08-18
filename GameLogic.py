import random
class Game:
    offsets = [[-1,0],[0,-1],[1,0],[0,1]]#left,up,right,down
    def __init__(self,width,height):
        self.width=width
        self.height=height
        self.foodPos =[0,0]
        self.map = [[0] * height for i in range(width)]#0=empty,1=head,2=body,3=food
        self.snake=Snake([int(width/2),int(height/2)])
        self.map[int(width/2)][int(height/2)]=1
        self.SpawnFood()
        self.dead=False
        self.grown=False

  
    def SpawnFood(self):
        randnum=[random.randrange(0,self.width),random.randrange(0,self.height)]
        count=0
        while self.map[randnum[0]][randnum[1]]!=0 and count<10000:
            randnum=[random.randrange(0,self.width),random.randrange(0,self.height)]
            count+=1
        if(count==10000):
            print("Could not place food")
            exit()#failsafe
        self.map[randnum[0]][randnum[1]]=3
        self.foodPos=randnum;
    def Cycle(self,direction):
        self.grown=False
        snakeHead=[0,0]
        snakeHead[0]+=self.offsets[direction][0] +  self.snake.bodySegments[self.snake.headIndex][0]
        snakeHead[1]+=self.offsets[direction][1] +  self.snake.bodySegments[self.snake.headIndex][1]
        if(snakeHead[0] >= self.width or snakeHead[0]<0 or snakeHead[1]>= self.height or snakeHead[1]< 0 ):
                #you died
                self.dead=True
                return
               
        if(self.map[snakeHead[0]][snakeHead[1]]==3):#food check
            self.grown=True
            self.SpawnFood()
            self.snake.Grow()
    
        if(self.grown==False):
            tailPos = self.snake.getTailPos()
            self.map[tailPos[0]][tailPos[1]]=0 #update tail 
        self.snake.UpdateHead(snakeHead)
        if(self.map[snakeHead[0]][snakeHead[1]]==1):
            #you died
                self.dead=True
        self.map[snakeHead[0]][snakeHead[1]]=1 
        return


class Snake:
    def __init__(self,startpos):
        self.bodySegments=[startpos]
        self.headIndex=0
        self.brain=None
        self.lifeSpan=0
    
    def Grow(self):
        self.bodySegments.insert(self.headIndex,self.getTailPos())
        self.headIndex+=1

    def UpdateHead(self, head):
        length = len(self.bodySegments)
        if(self.headIndex-1<0): #could use %length but i didnt want to
            self.headIndex=length-1
        else:
            self.headIndex-=1
        #override the old tail value with the head position, so i dont have to loop over the array and move every value
        self.bodySegments[self.headIndex][0]=head[0]
        self.bodySegments[self.headIndex][1]=head[1]
        self.lifeSpan+=1
    
    def getTailPos(self):
        index = self.headIndex-1
        if(index<0):
            index = len(self.bodySegments)-1
        return [self.bodySegments[index][0],self.bodySegments[index][1]]#copy values? unsure on python references 

        