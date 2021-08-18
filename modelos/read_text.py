
import cv2
from imutils.object_detection import non_max_suppression
from cv2 import data
from pymysql.connections import Connection
import pymysql
import pytesseract
import re
from modelos.utils import Utilidades

from pytesseract.pytesseract import TesseractError
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

class process_image:
  text=""
  placa=[]
  
  def __init__(self):
    pass
 
  def get_processed_image(self,ruta=""):
    
    image = cv2.imread("ProyectoCGV/images/carro-1.jpg")
    print("[INFO] dimensiones {}".format(image.shape[:2]))
    image = Utilidades.redimencionar(image,30)
    print("[INFO] redimension {}".format(image.shape[:2]))
    orig = image.copy()
   

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))#elimina el contenido de alta frecuencia por ejemplo: ruido, bordes.
    blurred =cv2.GaussianBlur(gray,(5,5),0)
    cv2.imshow("Blurred", blurred)
    wide = cv2.Canny(blurred, 10, 200)
    mid = cv2.Canny(blurred, 30, 150)
    tight = cv2.Canny(blurred, 240, 250)
    # show the output Canny edge maps
    cv2.imshow("Wide Edge Map", wide)
    cv2.imshow("Mid Edge Map", mid)
    cv2.imshow("Tight Edge Map", tight)
    cv2.imshow("BLUR",gray);
    #canny = cv2.Canny(gray,150,200)#Por medio de canny obtenemos una imagen binarizada
    #cv2.imshow("canny",canny)
    _, thresh1 = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    cnts,_ = cv2.findContours(thresh1,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        area = cv2.contourArea(c)#Obtiene el area de cada recuadro
        
        x,y,w,h = cv2.boundingRect(c)#Obteine las cordenadas para poder dibujar saber donde leer
        epsilon = 0.04*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        
        #if len(approx)==4 and area>9000:
        if len(approx)==4 and area>4000:
          #print('area=',area)
          
          aspect_ratio = float(w)/h
        
          if aspect_ratio>2:
            placa = gray[y:y+h,x:x+w]
            self.__class__.text = pytesseract.image_to_string(placa,config="-l eng --oem 1 --psm 9")
            #text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
            #print("[INFO] text ",text.strip())
          
          else:
            self.__class__.text="Noedectecto"

    #print('Vuelta ',contar)
    if len(self.text)>0:
      text = re.sub(r"[\W_]+","",self.text)
      #text=""
      print('PLACA: ',text)
    if len(self.placa)>0:
      cv2.imshow('PLACA',placa)
    #cv2.moveWindow('PLACA',780,10)
    #cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)
    cv2.putText(image,self.text.strip(),(10,90),1,2.2,(0,255,0),3)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

  