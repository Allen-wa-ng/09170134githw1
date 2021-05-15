### Import modules
import pygame
import sys
import random
import math
import time
from time import sleep

### Initialize pygame
pygame.init()

### Random seed
random.seed()

### Color set
white = (255,255,255)
black = (0,0,0)
# The color of "next block" hint
nextBlockBorderColor = (255,200,200)
# The color of the block that every represent color for exponential of two
colorList = [(255,  0,  0), (  0,255,  0), (204,153,255), (209,237,  0), (209,237,240), 
             (209, 40,240), (254,239,222), (  0,239,222), (255,255, 80), ( 51,102,255), 
             (255,204,164), (153,255,153), (194,194,214)]

### Screen set up
screen = pygame.display.set_mode((500,750)) #display screen
background = pygame.image.load('jaguar.jpg') #screen background
background = pygame.transform.scale(background, (500, 750)) #screen background
pygame.display.set_caption('2048 V.2') #caption

### Background music
pygame.mixer.music.load('let it go.ogg') #let it go.mp3 #mission.mp3
pygame.mixer.music.set_volume(0.5) #set volume


### Set global variable
# If the game is pause
pause = False
# The track of current dropping block
track = random.randint(1,5)-1
# The x pixel position of current dropping block
x_axis = 75+70*track
# The y pixel position of current dropping block
y_axis = 226
# The value of current dropping block
currentNumber = pow(2,random.randint(1,5))
# The value of next number
nextNumber = pow(2, random.randint(1,5))
# The time of the game start, it will update when the game return from pause
startTime = time.time()
# Score of the game
score = 0
# The variable to save if the last main loop is paused, useful to check if it is need to calculate the pause duration
lastLoopPaused = False
    
# Initial the game (start or restart)
def resetGame():
    random.seed()
    global score
    score = 0
    global startTime
    startTime = time.time()
    global blocks
    blocks = []
    for i in range(5):
        blocks.append([])
    global gameOver
    gameOver = False
    lastLoopPaused = False
    track = random.randint(1,5)-1
    x_axis = 75+70*track
    y_axis = 226
    currentNumber = pow(2,random.randint(1,5))
    nextNumber = pow(2, random.randint(1,5))
    
    # Play already loaded background music, -1 => infinite replace
    pygame.mixer.music.play(-1)
# get the maximum tracks with the most elements
def getMaxTrack():
    elems = []
    for i in range(5):
        elems.append(len(blocks[i]))
    return elems.index(max(elems))
# Drop the vertical line of block down to specific position (drop one unit height)
def dropAboveBlocks(x, y):
    if len(blocks[x]) > 0:
        for i in range(y, len(blocks[x])-1):
            blocks[x][i][0] = blocks[x][i+1][0]
        del blocks[x][len(blocks[x])-1]
# a super power to remove the track that has the most elements
def super_vert():
    max_track = getMaxTrack()
    for i in range(6):
        try:
            del blocks[max_track][0]
        except:
            pass

# a superpower to remove the first horizontal line
def super_hor():
    for i in range(0,5):
        try:
            del blocks[i][0]
        except IndexError:
            pass
        for j in range(len(blocks[i])):
            try:
                blocks[i][j][2]+=70
                print("dropped")
            except IndexError:
                pass

# Given a line number and merge from top of the line
def merge(x, y):
    global score

    if not x>=0 or not x<=5:
        return
    if not y>=0 or not len(blocks[x])-1>=y:
        return
        
    # Check left and right and down (T Shape)
    if x>0 and x<4 and y>0:
        leftLineY = len(blocks[x-1])-1
        rightLineY = len(blocks[x+1])-1
        if leftLineY>=y and rightLineY>=y:
            if blocks[x][y][0]==blocks[x-1][y][0] and blocks[x][y][0]==blocks[x+1][y][0] and blocks[x][y][0]==blocks[x][y-1][0]:
                blocks[x][y-1][0] *= 8
                score += blocks[x][y-1][0]
                dropAboveBlocks(x,y)
                dropAboveBlocks(x-1,y)
                dropAboveBlocks(x+1,y)
                merge(x,y)
                merge(x,y-1)
                merge(x-1, y)
                merge(x+1, y)
                # something about to check above
                merge(x, len(blocks[x])-1)
                merge(x-1, len(blocks[x-1])-1)
                merge(x+1, len(blocks[x+1])-1)
                return
    # Check right and down (Gamma shape)
    if x<4 and y>0:
        rightLineY = len(blocks[x+1])-1
        if rightLineY>=y:
            if blocks[x][y][0]==blocks[x+1][y][0] and blocks[x][y][0]==blocks[x][y-1][0]:
                blocks[x][y-1][0] *= 4
                score += blocks[x][y-1][0]
                dropAboveBlocks(x,y)
                dropAboveBlocks(x+1, y)
                merge(x,y)
                merge(x,y-1)
                merge(x+1,y)
                # something about to check above
                merge(x,len(blocks[x])-1)
                merge(x+1,len(blocks[x+1])-1)
                return
    # Check left and down (7 Shape)
    if x>0 and y>0:
        leftLineY = len(blocks[x-1])-1
        if leftLineY>=y:
            if blocks[x][y][0]==blocks[x-1][y][0] and blocks[x][y][0]==blocks[x][y-1][0]:
                blocks[x][y-1][0] *= 4
                score += blocks[x][y-1][0]
                dropAboveBlocks(x,y)
                dropAboveBlocks(x-1, y)
                merge(x,y)
                merge(x,y-1)
                merge(x-1,y)
                # something about to check above
                merge(x,len(blocks[x])-1)
                merge(x-1,len(blocks[x-1])-1)
                return
    # Check left and right (Horizontal shape)
    if x>0 and x<4:
        leftLineY = len(blocks[x-1])-1
        rightLineY = len(blocks[x+1])-1
        if leftLineY>=y and rightLineY>=y:
            if blocks[x][y][0]==blocks[x-1][y][0] and blocks[x][y][0]==blocks[x+1][y][0]:
                blocks[x][y][0] *= 4
                score += blocks[x][y][0]
                dropAboveBlocks(x-1,y)
                dropAboveBlocks(x+1,y)
                merge(x,y)
                merge(x-1,y)
                merge(x+1,y)
                # something about to check above
                merge(x,len(blocks[x])-1)
                merge(x-1,len(blocks[x-1])-1)
                merge(x+1,len(blocks[x+1])-1)
                return
    # Check left
    if x>0:
        leftLineY = len(blocks[x-1])-1
        if leftLineY>=y:
            if blocks[x][y][0] == blocks[x-1][y][0]:
                blocks[x][y][0] *= 2
                score += blocks[x][y][0]
                dropAboveBlocks(x-1,y)
                merge(x,y)
                merge(x-1,y-1)
                # somehting baout to check above
                merge(x-1, len(blocks[x-1])-1)
                return
    # Check right
    if x<4:
        rightLineY = len(blocks[x+1])-1
        if rightLineY>=y:
            if blocks[x][y][0] == blocks[x+1][y][0]:
                blocks[x][y][0] *= 2
                score += blocks[x][y][0]
                dropAboveBlocks(x+1, y)
                merge(x,y)
                merge(x+1,y-1)
                # something about to check above
                merge(x+1, len(blocks[x+1])-1)
                return
    # Check down
    if y>0:
        if blocks[x][y][0] == blocks[x][y-1][0]:
            blocks[x][y-1][0] *= 2
            score += blocks[x][y-1][0]
            dropAboveBlocks(x,y)
            merge(x,y)
            merge(x,y-1)
            # something about to check above
            merge(x, len(blocks[x])-1)
            return

# Set the next number to current number and randomly create a next number
def getNewNextBlock():
    global x_axis
    global y_axis
    global currentNumber
    global nextNumber
    global track
    y_axis = 226
    random.seed()
    track = random.randint(1,5)-1 #number of track 0~4
    currentNumber = nextNumber
    if score > 40000:
        nextNumber = pow(2, random.randint(6,10))
    elif score > 15000:
        nextNumber = pow(2, random.randint(4,7))
    else:
        nextNumber = pow(2,random.randint(1,5))
    x_axis=75+70*track
    
# Create a stable block
def blockAppend():
    global track
    global x_axis
    global currentNumber
    global blocks
    max_y_axis = 582-70*(len(blocks[track]))
    if max_y_axis > 223:
        # print(blocks)
        block = [currentNumber, x_axis, max_y_axis]
        blocks[track].append(block)
        merge(track, len(blocks[track])-1)
        getNewNextBlock()
        return True
    elif currentNumber==blocks[track][-1][0]:
        block = [currentNumber, x_axis, max_y_axis]
        blocks[track].append(block)
        merge(track, len(blocks[track])-1)
        getNewNextBlock()
        return True
    else:
        return False

# Draw a text
def drawText(text,font_str, size, color, pos):
    font=pygame.font.Font(font_str,size)
    text1=font.render(text, True,color)
    screen.blit(text1,pos)

# Format the time from second to minute and second
def getTimeformat(totalSecond):
    second=totalSecond%60
    minute=totalSecond/60
    return "{0:0=2d}:{1:0=2d}".format(int(minute), int(second))

# Change the log base
def getBaseLog(x, y):
  return math.log(y) / math.log(x)

# Draw a block
def drawBlock(value,x,y):
    # check whether the color is enough for the block
    if int(getBaseLog(2,value))-1 < 13:
        a=pygame.draw.rect(screen, colorList[int(getBaseLog(2,value))-1], (x,y,68,68), 0)
    else:
        a=pygame.draw.rect(screen, colorList[13], (x,y,68,68), 0)

    b=pygame.draw.rect(screen,black, (x,y,68,68), 4)
    font=pygame.font.Font('arial.ttf',30)
    textX =x+26-len(str(value))*5
    text=font.render(str(value),True,black,colorList[int(getBaseLog(2,value))-1])
    screen.blit(text,(textX,y+15))
    return a,b,text,value,x,y

# Draw background color
def drawBackground():
    global background
    screen.blit(background, (0, 0))

# Draw all border
def drawBorder():
    global color
    global nextBlockBorderColor
    # Draw line
    pygame.draw.lines(screen, white, True,[(50,75), (450,75)],5)
    pygame.draw.lines(screen, white, True,[(50,125),(450,125)],5)
    pygame.draw.lines(screen, white, True,[(75,220),(425,220)],5)
    # Draw rect
    pygame.draw.rect(screen, nextBlockBorderColor, (175,81,37,37), 10)
    pygame.draw.rect(screen, white, (50,25,400,650), 5)
    pygame.draw.rect(screen, white, (75,150,350,500), 5)
    pygame.draw.rect(screen, white, (50,685,45,45), 5)
    pygame.draw.rect(screen, white, (350,685,45,45), 5)
    pygame.draw.rect(screen, white, (405,685,45,45), 5)
    pygame.draw.rect(screen, white, (105,685,235,45), 0)
    for i in range(5):
        pygame.draw.lines(screen, white, True, [(75+i*70,150),(75+i*70,650)], 5)

# Draw all text
def drawAllTexts():
    drawText('Drop The Number!', 'arial.ttf',32, (255,255,80), (110,35))
    drawText('Next Block ►','arial.ttf',17,white,(57,88))
    drawText('Score:'+str(score),'arial.ttf',25,black,(110,693))
    drawText('II', 'arial.ttf',28,(255,255,255),(63,692))
    for i in range(5):
        drawText('†', 'arial.ttf',47,(255,0,0),(98+i*70,161))
        
# Draw blocks
def drawAllBlocks():
    global blocks
    for lineOfBlocksY in blocks:
            for block in lineOfBlocksY:
                if not gameOver:
                    drawBlock(block[0], block[1], block[2])
    
# Draw time
def drawTime():
    global lastLoopPaused
    global startTime
    global stopTimeText
    global startTimeOfPause
    if lastLoopPaused != pause:
        if pause:
            startTimeOfPause = time.time()
        else:
            startTime += (time.time()-startTimeOfPause)
    lastLoopPaused = pause
    if pause:
        duration = stopTimeText
    else:
        duration = time.time() - startTime
        stopTimeText = duration
    drawText('TIME:'+getTimeformat(duration),'arial.ttf',20,black,(315,91)) #display clock

# Draw next block hint
def drawNextBlock():
    pygame.draw.rect(screen, colorList[int(getBaseLog(2,nextNumber))-1], (175,81,38,38), 0)
    drawText(str(nextNumber),'arial.ttf',20,black,(168+25-len(str(nextNumber))*5,89))

# Draw game over screen
def drawGameOverScreen():
    screen.fill(white)
    drawText('Game Over', 'arial.ttf', 40, black, (145,150))
    drawText("Score:" ,'arial.ttf',30,black,(155,236))
    drawText(str(score),'arial.ttf',35,black,(255,235))
    pygame.draw.rect(screen, black, (160,320,185,40), 5)
    drawText('Restart','arial.ttf',25,black,(215,326))
    pygame.draw.rect(screen, black, (160,380,185,40), 5)
    drawText('Quit','arial.ttf',25,black,(225,386))
    pygame.display.update()

resetGame()

# Main loop
while True:
    sleep(0.02)
    
    if not gameOver:
        if not pause:
            y_axis += 1
            max_y_axis = 582-70*(len(blocks[track]))
        
        # Check if it is game over
        if y_axis > max_y_axis:
            if not blockAppend():
                pygame.mixer.music.stop()
                gameOver = True
                highest = 0
                
                with open('score.txt', 'w+') as hs:
                    hs.read(highest)
                    print(highest)
                    if int(highest)<score:
                        hs.write(str(score))
                    else:
                        hs.write(str(highest))
                
        
        # Draw
        drawBackground()
        drawBorder()
        drawAllTexts()
        drawTime()
        drawAllBlocks()
        
        # Draw next block hint
        drawNextBlock()
        
        # Draw dropping block
        drawBlock(currentNumber,x_axis,y_axis)
        
        # Draw pop pause button
        if pause:
            pygame.draw.rect(screen, nextBlockBorderColor, (175,300,150,150), 0)
            drawText('II', 'arial.ttf', 100, black, (220,322))
        
        # Flush draw buffer
        pygame.display.update()
        
    else:
        drawGameOverScreen()
        
    # Event handling
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            # Restart button
            if gameOver:
                if mouseX in range(160,345) and mouseY in range(320,360):
                        resetGame()
            # Quit button
                elif mouseY in range(380,420):
                    pygame.quit()
                    quit()
            # Pause button
            elif mouseX in range(50,95) and mouseY in range(685,730):
                pause = not pause
            elif pause:
                if mouseX in range(175,325) and mouseY in range(300,450):
                    pause = False
            # Click the track
            elif mouseX in range(76,426) and  mouseY in range(221,653):
                track = int((mouseX-76)/70)
                x_axis = 76+70*track
                max_y_axis = 582-70*(len(blocks[track]))
                blockAppend()
            elif mouseX in range(348,395) and mouseY in range(685,729):
                super_hor()
            elif mouseX in range(404,450) and mouseY in range(685,728):
                super_vert()