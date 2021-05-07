#Import modules
import pygame
import sys
import random
import math
from time import sleep
import time

#Initialize
pygame.init() 
y_axis = 0
x_axis = 0
score = 0 
cur_number = 0 #current number
track = 0 
blocks = []
next_num = pow(2, random.randint(1,9)) #next number
start_time = time.time() #time
fail = False #The game piont

#Background Music
pygame.mixer.music.load('let it go.ogg') #let it go.mp3 #mission.mp3
pygame.mixer.music.set_volume(0.5) #set volume
pygame.mixer.music.play(-1) #-1 => infinite replace

#color set
colorName = (255,200,200)
white = (255,255,255)
black = (0,0,0)
col_list = [(255,0,0),(0,255,0),(204,153,255),(209,237,0),
(209,237,240),(209,40,240),(254,239,222),(0,239,222),
(255,255,80),(51,102,255),(255,204,164),(153,255,153),
(194,194,214)]

#screen set up
screen = pygame.display.set_mode((500,750)) #display screen
background = pygame.image.load('jaguar.jpg') #screen background
background = pygame.transform.scale(background, (500, 750)) #screen background
pygame.display.set_caption('2048 V.2') #caption

#def
def Merge():
    for x in range(len(blocks)):
        for y in range(len(blocks[x])):
            try:
                #T shape
                if x>0 and x+1<len(blocks) and y>0 :
                    if blocks[x][y][0] == blocks[x-1][y][0] and blocks[x][y][0] == blocks[x][y-1][0] and blocks[x][y][0] == blocks[x+1][y][0]:
                        print("T shape")
                        blocks[x][y-1][0] *= 4
                        del blocks[x-1][y]
                        del blocks[x][y]
                        del blocks[x+1][y]
                        for i in range(y, len(blocks[x-1])):
                            print("dropped!")
                            blocks[x-1][i][2] += 70
                        for i in range(y,len(blocks[x])):
                            print("dropped!")
                            blocks[x][i][2] += 70
                        for i in range(y, len(blocks[x+1])):
                            print("dropped!")
                            blocks[x+1][i][2] +=70
                        continue 
            except IndexError:
                pass
    for x in range(len(blocks)):
        for y in range(len(blocks[x])):
            try:
                #horizontal three shape
                if x>0 and x+1<len(blocks):
                    if blocks[x][y][0] == blocks[x-1][y][0] and blocks[x][y][0] == blocks[x+1][y][0]:
                        print("horizontal three shape")
                        blocks[x][y][0] *= 4
                        del blocks[x-1][y]
                        del blocks[x+1][y]
                        for i in range(y, len(blocks[x-1])):
                            print("dropped!")
                            blocks[x-1][i][2] += 70
                        for i in range(y, len(blocks[x+1])):
                            print("dropped!")
                            blocks[x+1][i][2] +=70
                        continue 
                #left and right 7 shape
                if x>0 and y>0:
                    if blocks[x][y][0] == blocks[x-1][y][0] and blocks[x][y][0] == blocks[x][y-1][0]:
                        print("left 7 shape")
                        blocks[x][y-1][0] *= 4
                        del blocks[x-1][y]
                        del blocks[x][y]
                        for i in range(y, len(blocks[x-1])):
                            print("dropped")
                            blocks[x-1][i][2] += 70
                        for i in range(y,len(blocks[x])):
                            print("dropped!")
                            blocks[x][i][2] +=70
                        continue
                if x+1<len(blocks) and y>0 :
                    if blocks[x][y][0] == blocks[x+1][y][0] and blocks[x][y][0] == blocks[x][y-1][0]:
                        print("gamma shape")
                        blocks[x][y-1][0] *= 4
                        del blocks[x+1][y]
                        del blocks[x][y]
                        for i in range(y, len(blocks[x+1])):
                            print("dropped!")
                            blocks[x+1][i][2] += 70
                        for i in range(y,len(blocks[x])):
                            print("dropped!")
                            blocks[x][i][2] +=70
                        continue
            except IndexError:
                pass
    for x in range(len(blocks)):
        for y in range(len(blocks[x])):
            #L&R R&L
            if x>0 and x<len(blocks):
                try:
                    if blocks[x][y][0] == blocks[x-1][y][0]:  
                        print("right and left")
                        # print("y is", y)
                        blocks[x][y][0]*=2
                        del blocks[x-1][y]
                        for i in range(y,len(blocks[x-1])):
                            print("dropped!")
                            blocks[x-1][i][2]+=70
                        continue
                except IndexError:
                    pass
                #UP%DOWN
            if y>0:
                try:
                    if blocks[x][y][0] == blocks[x][y-1][0]:
                        print("up and down")
                        blocks[x][y-1][0]*=2
                        del blocks[x][y]
                        for i in range(y,len(blocks[x])):
                            print("dropped")
                            blocks[x][i][2] +=70
                        continue
                except IndexError:
                    pass

def initial():
    global x_axis
    global cur_number
    global next_num
    global track
    global y_axis
    y_axis = 226
    random.seed()
    track = random.randint(1,5)-1 #number of track 0~4 
    cur_number = next_num
    next_num = pow(2,random.randint(1,5))
    x_axis=75+70*track
    
def blockAppend():
    global x_axis
    global cur_number
    global next_num
    global track
    global y_axis
    global blocks
    if max_y_axis <= 223:
        screen.fill(white)
        createText('Game Over', 'arial.ttf', 40, black, (145,150))
        pygame.draw.rect(screen, black, (160,250,185,40), 5)
        createText('Restart','arial.ttf',25,black,(215,256))
        pygame.draw.rect(screen, black, (160,310,185,40), 5)
        createText('Quit','arial.ttf',25,black,(225,316))
        pygame.display.update()
        return False
    else:
        # print(blocks)
        l1 = []
        l1.append(cur_number)
        l1.append(x_axis)
        l1.append(max_y_axis)
        blocks[track].append(l1)
        initial()
        return True

def Text():
    createText('Drop The Number!', 'arial.ttf',32, (255,255,80), (110,35))
    createText('Next Block ►','arial.ttf',17,white,(57,88))
    createText('Score:'+str(score),'arial.ttf',25,(255,0,100),(110,693))
    createText('II', 'arial.ttf',28,(255,255,255),(63,692))
    for i in range(5):
        createText('†', 'arial.ttf',47,(255,0,0),(98+i*70,161))

def createText(text,font_str, size, color, pos):
    font=pygame.font.Font(font_str,size)
    text1=font.render(text, True,color)
    screen.blit(text1,pos)

def getTimeformat(sec):
    s_sec=sec%60
    s_min=sec/60
    return "{0:0=2d}:{1:0=2d}".format(int(s_min), int(s_sec))

def getBaseLog(x, y):
  return math.log(y) / math.log(x)

def create_block(x,y, value):
    a=pygame.draw.rect(screen, col_list[int(getBaseLog(2,value))-1], (x,y,68,68), 0)
    b=pygame.draw.rect(screen,black, (x,y,68,68), 4)
    font=pygame.font.Font('arial.ttf',30)
    textX =x+26-len(str(value))*5
    text=font.render(str(value),True,black,col_list[int(getBaseLog(2,value))-1])
    screen.blit(text,(textX,y+15))
    return a,b,text,value,x,y

def move_block(block, borders, text, x, y):
    block.move(x,y)
    borders.move(x,y)
    screen.blit(text,(x,y)) 
    return block, borders

def set_background():
    global background
    screen.fill(white) 
    screen.blit(background, (0, 0))

def draw():
    global color
    global colorName
    #Lines
    pygame.draw.lines(screen, white, True,[(50,75), (450,75)],5)
    pygame.draw.lines(screen, white, True,[(50,125),(450,125)],5)
    pygame.draw.lines(screen, white, True,[(75,220),(425,220)],5)
    #RECTs
    pygame.draw.rect(screen, white, (50,25,400,650), 5)
    pygame.draw.rect(screen, colorName, (175,81,37,37), 10)
    pygame.draw.rect(screen, white, (75,150,350,500), 5)
    pygame.draw.rect(screen, white, (50,685,45,45), 5)
    pygame.draw.rect(screen, white, (350,685,45,45), 5)
    pygame.draw.rect(screen, white, (405,685,45,45), 5)
    pygame.draw.rect(screen, white, (105,685,235,45), 5)
    for i in range(5):
        pygame.draw.lines(screen, white, True, [(75+i*70,150),(75+i*70,650)], 5)

# blocks append empty list [] 
for i in range(5):
    blocks.append([])

#Run the game
Running = True
restarted = False
pause = False
paused = False
initial()
n=0
end_time = 0
duration = 0
pause_time=time.time()
pause_dur = 0
tttt =0
paused = False
totalPauseDur=0
checked = False
while Running:
    sleep(0.02)
    #Upload the screen everytime
    set_background()
    draw()
    #Time
    end_time = time.time() #End Time
    duration = (end_time - start_time) - totalPauseDur
    if not pause:
        totalPauseDur += pause_dur
        pause_dur = 0
        paused = False
    elif pause:
        if not paused:
            pause_time=time.time()
            paused = True
        pause_dur = time.time() - pause_time
        duration = duration -pause_dur
    createText('TIME:'+getTimeformat(duration),'arial.ttf',20,black,(315,91)) #display clock
    #Text 
    Text()
    #number set
    pygame.draw.rect(screen, col_list[int(getBaseLog(2,next_num))-1], (175,81,38,38), 0)
    createText(str(next_num),'arial.ttf',20,black,(168+25-len(str(next_num))*5,89))
    #block moving
    create_block(x_axis,y_axis,cur_number)
    if not pause:
        y_axis += 1
        try:
            max_y_axis = 582-70*(len(blocks[track]))
        except:
            max_y_axis = 582
    if pause:
        pygame.draw.rect(screen, colorName, (175,300,150,150), 0)
        createText('II', 'arial.ttf', 100, black, (220,322))
    #Merge()
    #blocks stack rule
    if y_axis > max_y_axis and not pause:
        if not blockAppend():
            pygame.mixer.music.stop()
            fail = True
    Merge()
    #quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            # print(pygame.mouse.get_pos())
            pos_x = pygame.mouse.get_pos()[0]
            pos_y = pygame.mouse.get_pos()[1]
            #Pause button
            if pos_x in range(50,95):
                if pos_y in range(685,730):
                    pause = not pause
            #Restart button
            if pos_x in range(160,345) and fail:
                if pos_y in range(250,290) and fail:
                    fail = False
                    blocks = []
                    for i in range(5):
                        blocks.append([])
                    pygame.mixer.music.play(-1) #music play
                    start_time = time.time() #time
                    end_time = time.time()
                    pause_dur = 0
                    restarted = True 
            #Quit button
                elif pos_y in range(310,350):
                    Running = False
            #Click the track
            if pos_x in range(76,426) and not pause:
                if pos_y in range(221,653):
                    track = int((pos_x-76)/70)
                    x_axis = 76+70*track
                    try:
                        max_y_axis = 582-70*(len(blocks[track]))
                    except:
                        max_y_axis = 582
                    #restart or restarted
                    if not restarted:
                        blockAppend()
            if restarted:
                restarted = False
    #UPDATE
    for dica in blocks:
        for dic in dica :
            if not fail:
                create_block(dic[1], dic[2], dic[0])
    pygame.display.update()
