__author__ = 'lucasgago'
#En este archivo estan las funciones internas de actualizacion y tweeteo
import argparse
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#Funcion que envia el tweet
def tweetPhoto(tweet,image):
    import tweepy
    from subprocess import call
    from datetime import datetime
    i = datetime.now()
    now = i.strftime('%Y%m%d-%H%M%S')
    photo_name = now+ '.jpg'
    cv2.imwrite(photo_name,image)



    consumer_key='qyqyo7s64UmIiOfxAjPHIhErd'
    consumer_secret='gKhvExBAPfAzPm5y4JyqNo1K2m9ufCIxvUgtF1I3o9raC4ZVob'
    access_token='3213026471-HSZNU9K89m5yDiCLhzzNB7cYfAeHW2eK2PrOxRo'
    access_token_secret='nl1e8SqawoLPOjCcr6LgyXmBsQ80vxNNEd2F83SdX3wS7'


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)


    api = tweepy.API(auth)


    photo_path =  photo_name
    status = tweet
    api.update_with_media(photo_path, status=status)
    print "Tweeteado!"
    pass

#Funciones que actualizan rangos de deteccion
def nothing(*args):
    pass

def updateRanges():
    Hmin = cv2.getTrackbarPos("Hmin", "Adjustment")
    Hmax = cv2.getTrackbarPos("Hmax", "Adjustment")
    Smin = cv2.getTrackbarPos("Smin", "Adjustment")
    Smax = cv2.getTrackbarPos("Smax", "Adjustment")
    Vmin = cv2.getTrackbarPos("Vmin", "Adjustment")
    Vmax = cv2.getTrackbarPos("Vmax", "Adjustment")
    Pscale = cv2.getTrackbarPos("PoliScale", "Adjustment")
    
    lower = np.array([Hmin, Smin, Vmin], np.uint8)
    upper = np.array([Hmax, Smax, Vmax], np.uint8)
    return lower,upper,Pscale
#Funcion de inicializacion
def init():
    global consumer_key,consumer_secret,access_token,access_token_secret


    consumer_key='qyqyo7s64UmIiOfxAjPHIhErd'
    consumer_secret='gKhvExBAPfAzPm5y4JyqNo1K2m9ufCIxvUgtF1I3o9raC4ZVob'
    access_token='3213026471-HSZNU9K89m5yDiCLhzzNB7cYfAeHW2eK2PrOxRo'
    access_token_secret='nl1e8SqawoLPOjCcr6LgyXmBsQ80vxNNEd2F83SdX3wS7'
#Funcion de toma de datos iniciales
def check(args):
    global formaa
    print ""
    print "----------------*----------------"
    print ""

    if args.rot ==1:
        print "La camara estaba rotada, corrigiendo"

    if args.rot!=1:
        print "La camara no esta rotada"

    if args.form=="sq":
        print"Busco un cuadrado"
        formaa="cuadrado"
    if args.form=="tr":
        print"Busco un triangulo"
        formaa="triangulo"
    if args.form=="pn":
        print"Busco un pentagono"
        formaa="pentagono"

    if args.twitter=="Y":
        print"Voy a twittear mis resultados"
    else:
        print "No voy a usar twitter"

    print""
    print "----------------*----------------"
    return formaa

