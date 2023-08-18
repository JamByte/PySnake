from GameLogic import Game
import os

def UpdateGame(game: Game):
    for i in range(0,game.height):
        line="██"
        for j in range(0,game.width):
            if(game.map[j][i]==0):
                line+="  "
            elif(game.map[j][i]==1):
                line+="██"
            elif(game.map[j][i]==2):
                line+="▓▓"
            else:
                line+="▚▚"
        print("\033[%d;%dH" % (i+1, j))#https://stackoverflow.com/questions/54630766/how-can-move-terminal-cursor-in-python
        print(line)

    #print(game.debugMsg+"                                           ")

def debugAI(vector):
    count = 0
    for i in range(0,5):
        string = ""
        print("\033[%d;%dH" % (22+i, 0))#https://stackoverflow.com/questions/54630766/how-can-move-terminal-cursor-in-python
        for j in range(0,5):
            string += str(vector[count])+", "
            count +=1
        print(string)
        
def initalDraw(game: Game):
    
    board=""
    #Top border
    for i in range(0,game.width+2):
        board+="██"
    board+="\n"  
    for i in range(0,game.height):
        #Left border
        board+="██"

        for j in range(0,game.width):
            if(game.map[j][i]==0):
                board+="  "
            elif(game.map[j][i]==1):
                board+="██"
            elif(game.map[j][i]==2):
                board+="▓▓"
            else:
                board+="▚▚"

        #Right border
        board+="██\n"
    
    #Bottom border
    for i in range(0,game.width+2):
        board+="██"
    os.system("cls")
    print(board)