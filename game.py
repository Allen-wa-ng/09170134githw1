#import modules
import pygame
import sys
import random
import math
from time import sleep
import time

#initial set up
pygame.init()
moving = 0
index=0
score=0
cur =0
col_n = 0
blocks=[]
next_num = pow(2, random.randint(1,9))
start_time=time.time()  #time
fail = False #The game piont

#Background Music
pygame.mixer.music.load('mission.mp3') #let it go.mp3 #mission.mp3
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#color set
colorName=(255,200,200)
color=(255,255,255)
black=(0,0,0)
col_list=[(255,0,0),(0,255,0),(204,153,255),
(209,237,0),(209,237,240),
(209,40,240),(254,239,222),
(0,239,222),(255,255,80),
(51,102,255),(255,204,164),
(153,255,153),(194,194,214)]

#screen set up
screen=pygame.display.set_mode((500,750)) #display screen
background = pygame.image.load('jaguar.jpg') #screen background
background = pygame.transform.scale(background, (500, 750)) #screen background
pygame.display.set_caption('Pygame') #caption
icon=pygame.image.load('airplane.png') #icon
pygame.display.set_icon(icon) #display icon

#def
def ini():
    global index
    global cur
    global next_num
    global col_n
    global moving
    moving =226
    random.seed()
    col_n = random.randint(1,5)-1
    cur=next_num
    next_num = pow(2,random.randint(1,5))
    index=75+70*col_n
    
def blockAppend():
    global index
    global cur
    global next_num
    global col_n
    global moving
    global blocks
    if max_moving <= 223:
        screen.fill(color)
        createText('Game Over', 'arial.ttf', 40, black, (145,150))
        pygame.draw.rect(screen, black, (160,250,185,40), 5)
        createText('Restart','arial.ttf',25,black,(215,256))
        pygame.draw.rect(screen, black, (160,310,185,40), 5)
        createText('Quit','arial.ttf',25,black,(225,316))
        pygame.display.update()
        return False
    else:
        print(blocks)
        l1 = []
        l1.append(cur)
        l1.append(index)
        l1.append(max_moving)
        blocks[col_n].append(l1)
        ini()
        return True

def Text():
    createText('Drop The Number!', 'arial.ttf',32, (255,255,80), (110,35))
    createText('Next Block ►','arial.ttf',17,color,(57,88))
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
    # filled block
    a=pygame.draw.rect(screen, col_list[int(getBaseLog(2,value))-1], (x,y,68,68), 0)
    # borders
    b=pygame.draw.rect(screen,black, (x,y,68,68), 4)
    # font
    font=pygame.font.Font('arial.ttf',30)
    # print(getBaseLog(2,cur))
    textX =x+26-len(str(value))*5
    text=font.render(str(value),True,black,col_list[int(getBaseLog(2,value))-1])
    screen.blit(text,(textX,y+15))
    return a,b,text,value,x,y

def move_block(block, borders, text, x, y,value):
    block.move(x,y)
    borders.move(x,y)
    screen.blit(text,(x,y)) 
    return block, borders

def set_background():
    global background
    screen.fill(color) 
    screen.blit(background, (0, 0))

def draw_lc():
    global color
    global colorName
    #Lines
    pygame.draw.lines(screen, color, True,[(50,75), (450,75)],5)
    pygame.draw.lines(screen, color, True,[(50,125),(450,125)],5)
    pygame.draw.lines(screen, color, True,[(75,220),(425,220)],5)
    #RECTs
    pygame.draw.rect(screen, color, (50,25,400,650), 5)
    pygame.draw.rect(screen, colorName, (175,81,37,37), 10)
    pygame.draw.rect(screen, color, (75,150,350,500), 5)
    pygame.draw.rect(screen, color, (50,685,45,45), 5)
    pygame.draw.rect(screen, color, (350,685,45,45), 5)
    pygame.draw.rect(screen, color, (405,685,45,45), 5)
    pygame.draw.rect(screen, color, (105,685,235,45), 5)
    #Resct For loop
    for i in range(5):
        pygame.draw.lines(screen, color,True, [(75+i*70,150),(75+i*70,650)], 5)

# blocks array 
for i in range(6):
    blocks.append([])

#RUNNING
Running=True
ini()
n=0

while Running:
    #Upload the screen everytime
    set_background()
    draw_lc()
    #Time 
    end_time = time.time() #End Time
    dur = end_time-start_time
    createText('TIME:'+getTimeformat(dur),'arial.ttf',20,black,(315,91)) #display clock
    #Text 
    Text()
    #number set
    pygame.draw.rect(screen, col_list[int(getBaseLog(2,next_num))-1], (175,81,38,38), 0)
    createText(str(next_num),'arial.ttf',20,black,(168+25-len(str(next_num))*5,89))
    #block moving
    create_block(index,moving,cur)
    moving+=1
    try:
        max_moving = 582-70*(len(blocks[col_n]))
    except:
        max_moving = 582
    #blocks stack rule
    if moving > max_moving:
        if not blockAppend():
            pygame.mixer.music.stop()
            fail = True
    #quit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
        if event.type==pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos()) 
            print(index)
            pos = pygame.mouse.get_pos()[0]
            #Restart bottum
            if pos in range(160,345) and fail:
                if pygame.mouse.get_pos()[1] in range(250,290) and fail:
                    fail = False
                    blocks = []
                    blocks.append([])
                    blocks.append([])
                    blocks.append([])
                    blocks.append([])
                    blocks.append([])
                    pygame.mixer.music.play(-1) #music play
                    start_time=time.time() #time 
            #Quit buttom
                elif pygame.mouse.get_pos()[1] in range(310,350):
                    Running = False
            #Click the track
            if pos in range(76,426):
                col_n=int((pos-76)/70)
                index = 76+70*col_n
                try:
                    max_moving = 582-70*(len(blocks[col_n]))
                except:
                    max_moving = 582
            blockAppend()
    #UPDATE
    for dica in blocks:
        for dic in dica :
            if not fail:
                create_block(dic[1], dic[2], dic[0])
    pygame.display.update()
