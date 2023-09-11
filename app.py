# Import necessary libraries

from tokenize import Number
from numpy import testing
from numpy.lib.type_check import imag
import pygame,sys
from pygame import image
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2
from tensorflow.python.keras.backend import constant

# Set window size and other constants
WINDOWSIZEX= 640
WINDOWSIZEY= 480

BOUNDRYINC = 5

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

IMAGESAVE = False
# Load a pre-trained Keras model for hand recognition
MODEL = load_model("handrecogmodel.h5")

# Define labels for digits
LABELS={0:"Zero",1:"One",
        2:"Two",3:"Three",
        4:"Four",5:"Five",
        6:"Six",7:"Seven",
        8:"Eight",9:"Nine"}
# Initialize pygame
pygame.init()
FONT = pygame.font.Font(None, 18)
#Font =pygame.font.Font("freesansbold.tff",18)
DISPLAYSURF=pygame.display.set_mode((WINDOWSIZEX,WINDOWSIZEY))
pygame.display.set_caption("Digit Board")

# Variables to handle drawing
iswriting= False
number_xcord=[]
number_ycord=[]
image_cnt= 1

# Flag to enable digit prediction
PREDICT = True

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION and iswriting:
            xcord,ycord = event.pos
            pygame.draw.circle(DISPLAYSURF,WHITE,(xcord,ycord),4,0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting= True
        
        if event.type ==MOUSEBUTTONUP:
            iswriting=False
            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)   

            rect_min_x,rect_max_x= max(number_xcord[0]-BOUNDRYINC,0),min(WINDOWSIZEX,number_xcord[-1]+BOUNDRYINC)
            rect_min_Y = max(number_ycord[0] - BOUNDRYINC, 0)
            rect_max_Y = min(number_ycord[-1] + BOUNDRYINC, WINDOWSIZEY)


            number_xcord=[]
            number_ycord=[]
            pygame.draw.rect(DISPLAYSURF, RED, (rect_min_x, rect_min_Y, rect_max_x - rect_min_x, rect_max_Y - rect_min_Y), 2)

            ing_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_Y:rect_max_Y].T.astype(np.float32)


            if IMAGESAVE:
                cv2.imwrite("image.png")
                image_cnt+=1
            
            if PREDICT:
                  # Preprocess the drawn digit and predict its label
                image=cv2.resize(ing_arr,(28,28))  
                image= np.pad(image,(10,10),'constant',constant_values= 0)
                image = cv2.resize(image,(28,28))/255

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1,28,28,1)))])  

                textSurface = FONT.render(label,True,RED,WHITE)
                textRecobj = textSurface.get_rect()
                textRecobj.left,textRecobj.bottom = rect_min_x,rect_max_Y

                DISPLAYSURF.blit(textSurface,textRecobj)
            if event.type == KEYDOWN:
             if event.unicode =='n':
                DISPLAYSURF.fill(BLACK) 

        pygame.display.update()            

