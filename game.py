### Import modules
import pygame
import glob
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

# Icon set
programIcon = pygame.image.load('images.png')
pygame.display.set_icon(programIcon)

### Screen set up
screen = pygame.display.set_mode((500,750)) #display screen
background = pygame.image.load('bg3.jpg') #screen background
background = pygame.transform.scale(background, (500, 750)) #screen background
pygame.display.set_caption('2048 V.2') #caption

### Background music
pygame.mixer.music.load('edm 2.ogg') #let it go.mp3 #mission.mp3
pygame.mixer.music.set_volume(0.5) #set volume

### Set global variables
# check whether to cross during the pause
blocked_hor = False
blocked_vert = False
# Cooldown time (s)
cooldown_period=180
# If mute
mute = False
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
# highest score
highest = 0
# delay
delay=0.02
# Merging Speed
mergingSpeed = 5
# The last time which horizontal superpower clicked
cooldown_time_hor = None
# Horizontal superpower cooldown duration
cool_down_hor = 0
# The last time which vertical superpower clicked
cooldown_time_vert = None
# Vertical superpower cooldown duration
cool_down_vert = 0

def playVideo(v,x,y,w,h):
    for frame in glob.glob(v+"/*.png"):
        image = pygame.image.load(frame)
        image = pygame.transform.smoothscale(image, (w,h)) 
        screen.blit(image, (x,y))
        pygame.display.update()
        
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
    global lastLoopPaused
    lastLoopPaused = False
    global track
    track = random.randint(1,5)-1
    global x_axis
    x_axis = 75+70*track
    global y_axis
    y_axis = 226
    global currentNumber
    currentNumber = pow(2,random.randint(1,5))
    global nextNumber
    nextNumber = pow(2, random.randint(1,5))
    global cooldown_time_hor
    cooldown_time_hor = 0
    global cooldown_time_vert
    cooldown_time_vert = 0
    
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
    try:
        playVideo("power1",blocks[max_track][0][1]-220,blocks[max_track][0][2]-367, 500, 500)
    except:
        pass
    for i in range(6):
        try:
            del blocks[max_track][0]
        except:
            pass

# a superpower to remove the first horizontal line
def super_hor():
    max_track = getMaxTrack()
    playVideo("power2",-350,50, 1200, 750)
    for i in range(0,5):
        try:
            del blocks[i][0]
        except IndexError:
            pass
        for j in range(len(blocks[i])):
            try:
                blocks[i][j][2]+=70
            except IndexError:
                pass

# Given a line number and merge from top of the line
def merge(x, y):
    global score
    global delay
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
                old = blocks[x][y][0]
                ii = blocks[x][y][2]
                jj = blocks[x-1][y][1]
                kk = blocks[x+1][y][1]

                blocks[x][y-1][0] *= 8
                score += blocks[x][y-1][0]
                dropAboveBlocks(x-1,y)
                dropAboveBlocks(x+1,y)
                while jj < blocks[x][y-1][1] and kk > blocks[x][y-1][1]:
                   # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    
                    drawBlock(old,jj,blocks[x][y][2]) 
                    drawBlock(old,kk,blocks[x][y][2]) 
                    pygame.display.update()
                    
                    jj+=mergingSpeed
                    kk-=mergingSpeed
                dropAboveBlocks(x,y)
                while ii < blocks[x][y-1][2]:
                   # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    
                    drawBlock(old,blocks[x][y-1][1],ii)
                    pygame.display.update()
                    ii+=mergingSpeed
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
                old = blocks[x][y][0]
                ii = blocks[x][y][2]
                jj = blocks[x+1][y][1]
                print("Gamma",ii," ",blocks[x][y-1][2])

                blocks[x][y-1][0] *= 4
                score += blocks[x][y-1][0]
                dropAboveBlocks(x+1, y)
                while jj > blocks[x][y][1]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    drawBlock(old,jj,blocks[x][y][2])
                    pygame.display.update()
                    jj-=mergingSpeed
                dropAboveBlocks(x,y)
                while ii < blocks[x][y-1][2]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    drawBlock(old,blocks[x][y-1][1],ii)
                    pygame.display.update()
                    ii+=mergingSpeed
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
                old = blocks[x][y][0]
                ii = blocks[x][y][2]
                jj = blocks[x-1][y][1]
                blocks[x][y-1][0] *= 4
                score += blocks[x][y-1][0]
                dropAboveBlocks(x-1, y)
                print(blocks[x][y-1])
                while jj<blocks[x][y][1]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    # Draw next block hint
                    drawNextBlock()
                    
                    drawBlock(old,jj,blocks[x][y][2])
                    pygame.display.update()
                    jj+=mergingSpeed
                dropAboveBlocks(x,y)
                while ii < blocks[x][y-1][2]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    # Draw next block hint
                    drawNextBlock()
                    drawBlock(old,blocks[x][y-1][1],ii)
                    pygame.display.update()
                    ii+=mergingSpeed 
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
                old = blocks[x][y][0]
                ii=blocks[x+1][y][1]
                jj=blocks[x-1][y][1]
                blocks[x][y][0] *= 4
                score += blocks[x][y][0]
                dropAboveBlocks(x-1,y)
                dropAboveBlocks(x+1,y)
                while ii > blocks[x][y][1] and jj < blocks[x][y][1]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    
                    drawBlock(old,ii,blocks[x][y][2])
                    drawBlock(old,jj,blocks[x][y][2])
                    pygame.display.update()
                    ii-=mergingSpeed
                    jj+=mergingSpeed

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
                jj=blocks[x-1][y][1]
                old=blocks[x][y][0]

                blocks[x][y][0] *= 2
                score += blocks[x][y][0]
                dropAboveBlocks(x-1,y)
                while jj < blocks[x][y][1]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    drawBlock(old,jj,blocks[x][y][2])
                    pygame.display.update()
                    jj+=mergingSpeed
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
                old=blocks[x][y][0]
                jj=blocks[x+1][y][1]
                blocks[x][y][0] *= 2
                score += blocks[x][y][0]
                dropAboveBlocks(x+1, y)
                while jj > blocks[x][y][1]:
                    # Draw
                    drawBackground()
                    drawBorder()
                    drawAllTexts()
                    drawTime()
                    drawAllBlocks()
                    
                    # Draw next block hint
                    drawNextBlock()
                    drawBlock(old,jj,blocks[x][y][2])
                    pygame.display.update()
                    jj-=mergingSpeed
                merge(x,y)
                merge(x+1,y-1)
                # something about to check above
                merge(x+1, len(blocks[x+1])-1)
                return
    # Check down
    if y>0:
        if blocks[x][y][0] == blocks[x][y-1][0]:
            jj=blocks[x][y][2]
            old=blocks[x][y][0]
            blocks[x][y-1][0] *= 2
            score += blocks[x][y-1][0]
            dropAboveBlocks(x,y)
            while jj < blocks[x][y-1][2]:
                # Draw
                drawBackground()
                drawBorder()
                drawAllTexts()
                drawTime()
                drawAllBlocks()
                
                # Draw next block hint
                drawNextBlock()
                drawBlock(old,blocks[x][y-1][1],jj)
                pygame.display.update()
                jj+=mergingSpeed
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
    if score > 100000:
        nextNumber = pow(2, random.randint(7,12))
    elif score > 30000:
        nextNumber = pow(2, random.randint(1,9))
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
        a=pygame.draw.rect(screen, colorList[12], (x,y,68,68), 0)

    b=pygame.draw.rect(screen,black, (x,y,68,68), 4)
    font=pygame.font.Font('arial.ttf',27)
    textX =x+24-len(str(value))*5
    if value <= 8192:
        text=font.render(str(value),True,black,colorList[int(getBaseLog(2,value))-1])
    else:
        text=font.render(str(value),True,black,colorList[12])
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
    pygame.draw.rect(screen, nextBlockBorderColor, (180,81,37,37), 10)
    pygame.draw.rect(screen, white, (50,25,400,650), 5)
    pygame.draw.rect(screen, white, (75,150,350,500), 5)
    pygame.draw.rect(screen, white, (50,685,45,45), 5)
    pygame.draw.rect(screen, white, (350,685,45,45), 0)
    pygame.draw.rect(screen, white, (405,685,45,45), 0)
    pygame.draw.rect(screen, white, (105,685,235,45), 0)
    for i in range(5):
        pygame.draw.lines(screen, white, True, [(75+i*70,150),(75+i*70,650)], 5)
    # Draw mute icon
    if mute:
        image = pygame.image.load("mute-2.png")
        screen.blit(image, (402, 83))
    else:
        image = pygame.image.load("mute-1.png")
        screen.blit(image, (402, 83))

# Draw all text
def drawAllTexts():
    drawText('Drop The Number', 'arial.ttf',35, colorList[int(getBaseLog(2,nextNumber))-1], (111,30))
    drawText('Next Block ►','arial.ttf',20, white,(57,88))
    drawText('Score:'+str(score),'arial.ttf',25, black,(110,693))
    for i in range(5):
        drawText('†', 'arial.ttf',47,(0,0,0),(98+i*70,161))
        
# Draw blocks
def drawAllBlocks():
    global blocks
    for lineOfBlocksY in blocks:
            for block in lineOfBlocksY:
                if not gameOver:
                    drawBlock(block[0], block[1], block[2])
    image = pygame.image.load("fire-4.png")
    screen.blit(image, (402,678))
    image = pygame.image.load("vertical-2.png")
    screen.blit(image, (350, 678))
    
# Draw time
def drawTime():
    global lastLoopPaused
    global startTime
    global stopTimeText
    global startTimeOfPause
    global duration
    if lastLoopPaused != pause:
        if pause:
            startTimeOfPause = time.time()
        else:
            pauseDuration = time.time()-startTimeOfPause
            # Stop horizontal super skill cooldown when puase
            global cooldown_time_hor
            if cooldown_time_hor != 0:
                cooldown_time_hor += pauseDuration
            # Stop vertical super skill cooldown when puase
            global cooldown_time_vert
            if cooldown_time_vert != 0:
                cooldown_time_vert += pauseDuration
            # Change start time of the game which use to count the timer
            startTime += pauseDuration
    lastLoopPaused = pause
    if pause:
        drawText('►','arial.ttf',28,white,(61,692))
        duration = stopTimeText
    else:
        drawText('II', 'arial.ttf',28,white,(63,692))
        duration = time.time() - startTime
        stopTimeText = duration
    drawText('TIME:'+getTimeformat(duration),'arial.ttf',20,black,(275,91)) #display clock

# Draw next block hint
def drawNextBlock():
    pygame.draw.rect(screen, colorList[int(getBaseLog(2,nextNumber))-1], (180,81,38,38), 0)
    drawText(str(nextNumber),'arial.ttf',18,black,(168+25-len(str(nextNumber))*5,89))
    global blocked_hor
    global blocked_vert
    cdh = time.time() - cooldown_time_hor
    cdv = time.time() - cooldown_time_vert
    #Cool down hor X        
    if cdh<cooldown_period and cdh!=0:
        blocked_hor = True
        pygame.draw.rect(screen, black, (352,685,45,45), 5)
        drawText('X','arial.ttf',60,black,(352,675))
    elif not pause:
        blocked_hor = False
        image = pygame.image.load("vertical-2.png")
        screen.blit(image, (350, 678))

    if cdv<cooldown_period and cdv!=0:
        blocked_vert = True
        pygame.draw.rect(screen, black, (403,685,45,45), 5)
        drawText('X','arial.ttf',60,black,(405,675))
    elif not pause:
        blocked_vert = False
        image = pygame.image.load("fire-4.png")
        screen.blit(image, (402,678))

# Draw game over screen
def drawGameOverScreen():
    global highest
    screen.fill(white)
    drawText('Game Over', 'arial.ttf', 40, black, (145,150))
    drawText("TIME:", 'arial.ttf', 30, black, (165,220))
    drawText(str(getTimeformat(duration)), 'arial.ttf', 30, black, (252,220))
    drawText("Highest Score:", 'arial.ttf', 30, black, (100,270))
    drawText(str(highest), 'arial.ttf', 30, black, (304,271))
    drawText("Your Score:" ,'arial.ttf',30,black,(120,320))
    drawText(str(score),'arial.ttf',30,black,(280,322))
    pygame.draw.rect(screen, black, (160,380,185,40), 5)
    drawText('Restart','arial.ttf',25,black,(215,384))
    pygame.draw.rect(screen, black, (160,430,185,40), 5)
    drawText('Quit','arial.ttf',25,black,(225,435))
    pygame.display.update()

# Pause if it is not gameOver yet
def tryToPause():
    global pause
    global gameOver
    if not gameOver:
        pause = not pause

resetGame()

# Main loop
while True:
    #delay time
    sleep(delay)

    if not gameOver:
        if not pause:
            y_axis += 1
            max_y_axis = 582-70*(len(blocks[track]))
        
        # Check if it is game over
        if y_axis > max_y_axis:
            if not blockAppend():
                pygame.mixer.music.stop()
                gameOver = True
                with open('score.txt', 'r') as hs:
                    highest = int(hs.read())
                with open('score.txt', 'w') as hs:
                    if highest < score:
                        hs.write(str(score))
                    else:
                        hs.write(str(highest))
                with open('score.txt', 'r') as hs:
                    highest = int(hs.read())

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
            image = pygame.image.load("pause.png")
            screen.blit(image, (140, 290))
            image = pygame.image.load("ball-1.png")
            screen.blit(image, (142, 294))
            #print(blocked_hor, " ",blocked_vert)
            if blocked_hor:
                pygame.draw.rect(screen, black, (352,685,45,45), 5)
                drawText('X','arial.ttf',60,black,(352,675))
            if blocked_vert:
                pygame.draw.rect(screen, black, (403,685,45,45), 5)
                drawText('X','arial.ttf',60,black,(405,675))

        # Flush draw buffer
        pygame.display.update()
        
    else:
        drawGameOverScreen()
        
    # Event handling
    for event in pygame.event.get():
        # Quit event
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        # Keyboard event
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT:
                if track<5 and track>0:
                    track-=1
                    x_axis-=70
            if event.key==pygame.K_RIGHT:
                if track<4:
                    track+=1
                    x_axis+=70
            if event.key==pygame.K_DOWN:
                blockAppend()
            if event.key==pygame.K_SPACE:
                tryToPause()
            if event.key==pygame.K_RETURN:
                tryToPause()
            if event.key==pygame.K_m:
                mute = not mute
                if mute:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
            if event.key==pygame.K_h:
                if cooldown_time_hor==0:
                    cooldown_time_hor = time.time()
                    super_hor()
                cool_down_hor = time.time() - cooldown_time_hor
                if cool_down_hor>cooldown_period:
                    cool_down_hor=0
                    cooldown_time_hor = time.time()
                    super_hor()

            if event.key==pygame.K_v:
                if cooldown_time_vert==0:
                    cooldown_time_vert = time.time()
                    super_vert()
                cool_down_vert = time.time() - cooldown_time_vert
                if cool_down_vert>cooldown_period:
                    cool_down_vert=0
                    cooldown_time_vert = time.time()
                    super_vert()
        # Mouse event
        if event.type==pygame.MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pos())
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            #Stop play the music
            if mouseX in range(402,437) and mouseY in range(83,118):
                mute = not mute
                if mute:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()
                

            # Restart button
            if gameOver:
                if mouseX in range(160,345) and mouseY in range(380,420):
                        resetGame()
            # Quit button
                elif mouseY in range(430,470):
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
            # Horizontal superpower
            elif mouseX in range(348,395) and mouseY in range(685,729):
                if cooldown_time_hor==0:
                    cooldown_time_hor = time.time()
                    super_hor()
                cool_down_hor = time.time() - cooldown_time_hor
                if cool_down_hor>cooldown_period:
                    cool_down_hor=0
                    cooldown_time_hor = time.time()
                    super_hor()
            # Vertical superpower
            elif mouseX in range(404,450) and mouseY in range(685,728):
                if cooldown_time_vert==0:
                    cooldown_time_vert = time.time()
                    super_vert()
                cool_down_vert = time.time() - cooldown_time_vert
                if cool_down_vert>cooldown_period:
                    cool_down_vert=0
                    cooldown_time_vert = time.time()
                    super_vert()
