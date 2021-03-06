#import modules
import pygame
import sys
import random
import math
from time import sleep
def getBaseLog(x, y):
  return math.log(y) / math.log(x)

#initial set up
pygame.init()
score=0
#screen set up
screen=pygame.display.set_mode((500,750))
#caption & icon
pygame.display.set_caption('Pygame')
icon=pygame.image.load('airplane.png')
pygame.display.set_icon(icon)
#color set
colorName=(255,200,200)
color=(25,100,200)
screen.fill(colorName)
#Draw the outlines
#Lines
pygame.draw.lines(screen, color, True,[(50,75), (450,75)],1)
pygame.draw.lines(screen, color, True,[(50,125),(450,125)],1)
pygame.draw.lines(screen, color, True,[(75,200),(425,200)],1)
#RECTs
pygame.draw.rect(screen, color, (50,25,400,650), 1)
pygame.draw.rect(screen, color, (161,81,37,37), 4)
pygame.draw.rect(screen, color, (75,150,350,500), 1)
pygame.draw.rect(screen, color, (50,685,25,25), 3)
pygame.draw.rect(screen, color, (385,685,25,25), 3)
pygame.draw.rect(screen, color, (420,685,25,25), 3)
for i in range(6):
    pygame.draw.lines(screen, color,True, [(125+i*50,150),(125+i*50,650)], 1)
pygame.display.update()
#textbox
#TITLE
font=pygame.font.Font('freesansbold.ttf',32)
text=font.render('Drop The Number!', True,(0,100,0))
screen.blit(text,(110,35))
#NEXT BLOCK
font=pygame.font.SysFont('dejavusans',18)
text=font.render('Next Block ▶ ', True,(255,0,100))
screen.blit(text,(55,85))
#SCORE
font=pygame.font.Font('freesansbold.ttf',20)
text=font.render('Score:'+str(score), True,(255,0,100))
screen.blit(text,(85,688))
#PAUSE
font=pygame.font.Font('freesansbold.ttf',20)
text=font.render('II', True,(0,0,0))
screen.blit(text,(57,689))
#ARROW DOWN
font=pygame.font.SysFont('dejavusans',40)
text=font.render('⇟', True,(0,0,0))
for i in range(7):
    screen.blit(text,(85+i*50,145))
#ARROW R&L
text=font.render('↔', True,(0,0,0))
screen.blit(text,(387,673))
#ARROW UP&DOWN
text=font.render('↕', True,(0,0,0))
screen.blit(text,(422,676.5))

font=pygame.font.SysFont('dejavusans',30)
#RANDOM NUMBER
#NEXT BLOCK NUMBER
random.seed()

#color array
col_list=[(0,255,0),(0,160,250),(0,255,255)
,(42,151,0),(42,151,188),(42,183,143),(179,140,143)]

#RUNNING
Running=True
cur =0
while Running:
    cur=pow(2,random.randint(1,6))
    pygame.draw.rect(screen, col_list[int(getBaseLog(2,cur))-1], (161,81,38,38), 0)
    pygame.display.update()
    print(getBaseLog(2,cur))
    text=font.render(str(cur),True,(255,0,100),col_list[int(getBaseLog(2,cur))-1])
    screen.blit(text,(170,85))
    pygame.display.update()
    sleep(1)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
#UPDATE
pygame.display.update()
