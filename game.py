import pygame
import sys
#initial set up
pygame.init()
screen=pygame.display.set_mode((500,750))
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
font=pygame.font.SysFont('arialunicode',18)
text=font.render('Next Block ▶ ', True,(255,0,100))
screen.blit(text,(55,85))
#SCORE
font=pygame.font.Font('freesansbold.ttf',20)
text=font.render('Score:', True,(255,0,100))
screen.blit(text,(85,688))
#PAUSE
font=pygame.font.Font('freesansbold.ttf',20)
text=font.render('II', True,(0,0,0))
screen.blit(text,(57,689))
#ARROW DOWN
font=pygame.font.SysFont('arialunicode',40)
text=font.render('⇟', True,(0,0,0))
for i in range(7):
    screen.blit(text,(85+i*50,145))
#ARROW R&L
font=pygame.font.SysFont('arialunicode',30)
text=font.render('↔', True,(0,0,0))
screen.blit(text,(387,673))
#ARROW UP&DOWN
font=pygame.font.SysFont('arialunicode',30)
text=font.render('↕', True,(0,0,0))
screen.blit(text,(422,676.5))
#UPDATE
pygame.display.update()









Running=True
while Running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            quit()
