__author__ = 'lucasgago'


#Importamos las librerias


import libs

import argparse

import cv2

import numpy as np

import RPi.GPIO as gpio
from picamera.array 
import PiRGBArray
from picamera 
import PiCamera

import time

import tweepy
from subprocess 
import call
from datetime 
import datetime





#Preparamos los puertos de salida


gpio.setmode(gpio.BOARD)

gpio.setup(7,gpio.OUT)

gpio.setup(11,gpio.OUT)

gpio.setup(13,gpio.OUT)

gpio.setup(15,gpio.OUT)

gpio.setup(38,gpio.OUT)

gpio.setup(37,gpio.OUT)




#LLamamos a la funcion que lee los valores de entrada


parser = argparse.ArgumentParser()

parser.add_argument("-r" ,"--rot", type=int,
                    help="1 if the camera is rotated, 0 if not")

parser.add_argument("-f", "--form",type=str,
                    help="form of object to detect, could be sq (square), tr (triangle) or pn (pentagon)")


parser.add_argument("-tw", "--twitter",type=str,
                    help="Activate twitter functionality ,yes (Y) or no (N)")


args = parser.parse_args()


formaa=libs.check(args)
cv2.namedWindow("Adjustment")




#Creamos los deslizadores para controlar los distintos parametros


only=1
centres=[]
Hmin = 44

Hmax = 187

Smin = 0

Smax = 171

Vmin = 0

Vmax = 33

lower = np.array([Hmin, Smin, Vmin])

upper = np.array([Hmax, Smax, Vmax])

Pscale=38
Pscalef=0.1
lados = {'cuadrado': 4, 'triangulo': 3,"pentagono":5}


cv2.createTrackbar("Hmin", "Adjustment", Hmin, 255, libs.nothing)

cv2.createTrackbar("Hmax", "Adjustment", Hmax, 255, libs.nothing)

cv2.createTrackbar("Smin", "Adjustment", Smin, 255, libs.nothing)

cv2.createTrackbar("Smax", "Adjustment", Smax, 255, libs.nothing)

cv2.createTrackbar("Vmin", "Adjustment", Vmin, 255, libs.nothing)
cv2.createTrackbar("Vmax", "Adjustment", Vmax, 255, libs.nothing)

cv2.createTrackbar("PoliScale", "Adjustment", Pscale, 1000, libs.nothing)
h=640
v=480
center = (h / 2, v / 2)




#Accedemos a la camara


Rect=40
camera = PiCamera()

camera.resolution = (h,v)

camera.framerate = 32

rawCapture = PiRGBArray(camera, size=(h,v))

x1=h/2-Rect

x2=h/2+Rect

y1=v/2-Rect

y2=v/2+Rect


tweet="Encontre un "+formaa

M = cv2.getRotationMatrix2D(center, 180, 1.0)



#Configuramos los PWM


pwmi = gpio.PWM(38,50)

pwmd = gpio.PWM(37,50)

pwmi.start(0)
pwmd.start(0)

cv2.waitKey(0)
time.sleep(0.1)
stp=1




# Empieza la captura


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
if stp==1:
        
        
        
image = frame.array
        

#Rotamos si lo indicamos al iniciar el programa
      
  if args.rot==1:
            
image = cv2.warpAffine(image, M, (h,v))
     
   
#Buscamos los colores en el rango definido
      
  shapeMask = cv2.inRange(image, lower, upper)
       
 
        cv2.imshow("Mask", shapeMask)
  
      
       
 #Buscamos sus contornos
     
   (cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    
    
        lower, upper,Pscale= libs.updateRanges()
  
      
        
        Pscalef=abs(Pscale/float(1000))
   
    
 #Dibujamos el rectangulo del centro de la pantalla
        
cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
     
   cv2.circle(image,(320,240),5,(0,0,255))
     
   cv2.imshow("Image", image)
  

      #Analizamos los datos del contorno, buscando la forma especificada
     

   for c in cnts:
          
  if cv2.contourArea(c)>5000 :
     
           approx = cv2.approxPolyDP(c,(Pscalef)*cv2.arcLength(c,True),True)
   
             if len(approx)==lados[formaa]:
       
             moments = cv2.moments(c)
    
                centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
    
                lenc=len(centres)
    
                centro= centres[lenc-1]
    

                #Calculamos su centro
       

             cv2.circle(image,centro,7,(0,255,255),-1)
  
                  centrox=centro[0]
           
         centroy=centro[1]
          
          cv2.drawContours(image,[approx],-1,(0,0,255),3)
   
                 cv2.rectangle(image, (x1, y1), (x2, y2), (0,255,0), 2)
  

                  #Comprobamos si el centro esta en el rectangulo central
     
               if centrox>x1 and centrox<x2 and centroy>y1 and centroy<y2:
    
                    cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0), 2)
    
                    if cv2.contourArea(c)<40000 :
                  
          pwmi.ChangeDutyCycle(25)
                
            pwmd.ChangeDutyCycle(30)
            

                #Hacemos que el robot avance hacia el objetivo
       
                     gpio.output(7,gpio.LOW)
              
              gpio.output(11,gpio.HIGH)
         
                   gpio.output(15,gpio.HIGH)
    
                        gpio.output(13,gpio.LOW)
      
                      time.sleep(0.3)
            
                pwmi.ChangeDutyCycle(18)
      
                      pwmd.ChangeDutyCycle(23)
   
                         time.sleep(1)
           
             
                            gpio.output(7,gpio.LOW)
 
                           gpio.output(11,gpio.LOW)
           
                 gpio.output(13,gpio.LOW)

                            gpio.output(15,gpio.LOW)
   
                         if args.twitter=="Y":

                                if only==1:

                                    #Tweeteamos la foto del objetivo
 
                                   libs.tweetPhoto(tweet,image)
     
                               only=0
                 
           stp=0
                      
      			print "Deberia pararse"
   
                         cv2.imshow("Image", image)

  
  

    if (cv2.waitKey(1) & 0xFF == ord('q')) or stp==0:

   
     break
    
   
 rawCapture.truncate(0)

gpio.cleanup()
cv2.destroyAllWindows()








