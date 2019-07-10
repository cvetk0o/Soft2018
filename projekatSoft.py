# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 21:15:43 2019

@author: dragon
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 16:19:36 2019

@author: dragon
"""

import cv2
import numpy as np
import math


video = cv2.VideoCapture('video-9.avi')
brojac=0
firstFrame = None

ret,orig_frame = video.read()


class Broj:
    
    def __init__ (self,x,y,slika):
        #print('dodajem novi')
        self.x = x
        self.y = y 
        self.slike = []
        self.slike.append(slika)
        self.pozicije = []
        self.nestao = 0
        
        

    def dodaj(self,x,y,slika):
        #print('dodajem',x,'  ', y)
        self.pozicije.append((self.x,self.y))
        self.x=x
        self.y=y
        self.slike.append(slika)
        self.nestao = 0
    
    def nestaje(self):
        self.nestao +=1





def pronadjiLinije():
    global plavaLinija,zelenaLinija
    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv= cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
   

    #plava
    mask1 = cv2.inRange(hsv, (100,150, 20), (140, 255,255))
    edges = cv2.Canny(mask1,75,150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

    plavaLinija = lines[0][0]
    
    
    mask2= cv2.inRange(hsv,(36,25,25),(70,255,255))
    edges = cv2.Canny(mask2,75,150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)
    
    zelenaLinija = lines[0][0]
    




#lista pracenih objekata
brojevi = []
nestaliBrojevi = []





pronadjiLinije()




brojacFrame=0
while True :
    
    ret,frame =video.read()
    
    if ret == False:
        break

    if brojacFrame == 10 :
            
        
        r = frame.copy()
        # set blue and green channels to 0
        r[:, :, 0] = 0
        r[:, :, 1] = 0
        
        gray = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
        
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        
        thresh = cv2.threshold(gray, 11, 255, cv2.THRESH_BINARY)[1]
        
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        
        
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for index,c in enumerate(contours):
            area = cv2.contourArea(c)
            if area < 100:
                del contours[index]
        
        
        
        if not brojevi:
            for c in contours:
                (x, y, w, h) = cv2.boundingRect(c)
                broj = Broj (x/2,y/2,frame[y:y+28,x:x+28])
                brojevi.append(broj)
        
        
        else:
            
            for indexBroja,b in enumerate(brojevi):
                print('broj : ' ,b.x,'   ', b.y)
                indexKonture = 0
                najblizi = 50
                for index,c in enumerate(contours):
                    
                    (x,y,w,h) = cv2.boundingRect(c)
                    distanca = math.sqrt((b.x-x)**2+(b.y-y)**2)
                    #print(distanca)
                    if distanca < najblizi:
                        najblizi = distanca
                        indexKonture =index
                
                if najblizi < 20:
                    print('manje od 30 : ' , b.x,'  ', b.y)
                    print('distancaaa manjaa od 30::::::',najblizi)
                    kontura = contours[indexKonture]
                    (x,y,w,h) = cv2.boundingRect(kontura)
                    b.dodaj(x/2,y/2,frame[y:y+28, x:x+28])
                    del contours[indexKonture]
                
                else:
                    b.nestaje()
                    print(b.x, '    ' , b.y)
                    if b.nestao > 10:
                        print('izbacujem ga ')
                        '''
                        cv2.imshow('nestali',b.slike[0])
                        cv2.waitKey(1000)
                        '''
                        nestaliBrojevi.append(b)
                        print('broj slika     ',len(b.slike))
                        del brojevi[indexBroja]
        
            if contours:
                for c in contours:
                    (x, y, w, h) = cv2.boundingRect(c)
                    broj = Broj (x/2,y/2,frame[y:y+28, x:x+28])
                    brojevi.append(broj)
                    
        
        
        
        
        
        
        
        
        
        
        
            
            
        for b1 in brojevi:
            (x, y, w, h) = cv2.boundingRect(c)
             
            cv2.rectangle(frame, (round(b1.x*2), round(b1.y*2)), (round(b1.x*2) + 28, round(b1.y*2) + 28), (255, 255,255), 2)
        
        cv2.imshow('blur',frame)
        cv2.waitKey(100)
        brojacFrame=0
       
    

    brojacFrame = brojacFrame +1
    print(brojacFrame)


video.release()


 

cv2.destroyAllWindows()



