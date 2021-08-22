
from tkinter import Text
import cv2
import imutils
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
  placa=None
  
  def __init__(self):
    pass
 
  def get_processed_image(self,ruta=""):
    self.__class__.text="No se encontro"
    #self.placa = None
    image = cv2.imread(ruta)
    image = imutils.resize(image,width=560)
  
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.blur(gray,(3,3))#elimina el contenido de alta frecuencia por ejemplo: ruido, bordes.
    canny = cv2.Canny(gray, 10, 200)
  
    cnts,_ = cv2.findContours(canny,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        area = cv2.contourArea(c)#Obtiene el area de cada recuadro
        
        x,y,w,h = cv2.boundingRect(c)#Obteine las cordenadas para poder dibujar saber donde leer
        epsilon = 0.04*cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,epsilon,True)
        
        if len(approx)==4 and area>4000 and area<9000:
          aspect_ratio = float(w)/h
        
          if aspect_ratio>2:
            self.__class__.placa = gray[y:y+h,x:x+w]
            cv2.rectangle(image,(x,y),(x+w,h+y),(0,255,0),3)
            self.__class__.text = pytesseract.image_to_string(self.placa,config="-l eng --oem 1 --psm 9")
            self.__class__.text = re.sub(r"[\W_]+","",self.text)
            self.__class__.text = self.validate_placa(self.text)
            cv2.putText(image,self.text,(x,y-10),1,2.2,(0,255,0),2)
          else:
            self.__class__.text="No se encontro"
 


    #print('Vuelta ',contar)

    self.__class__.text = re.sub(r"[\W_]+","",self.text)
    self.__class__.text = self.validate_placa(self.text)
  
      #text=""
    #if self.placa is not None and len(self.placa)>0:
    #  cv2.imshow('PLACA',self.placa)
  
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

  def get_roi(self,imag):#se realizan todos los calculos para iniciar determinar una region de interes
    (heigth, width) = imag.shape[:2]
    halfWidth = (width/2)#obtiene la mitad del ancho de la imagen
    quaterWidth = (width/4)#obtiene a cuanto equivale un cuarto del ancho de la imagen
    halfHeighth = (heigth/2)#obtiene la mitad del alto de la imagen
    quaterHeigth = (heigth/4)#obtiene a cuanto equivale un cuarto de la altura de la imagen
    
    x1=halfWidth-quaterWidth#para obtener el punto de inicio al total del ancho le restamos un cuarto 
    y1=halfHeighth-quaterHeigth
    #Obtenemos luego los puntos donde terminara la region de origen
    h=x1+(quaterHeigth*2)#obtenemos el punto final en y
    w=y1+(quaterWidth*2)
    return int(x1),int(y1),int(w),int(h)
  def validate_placa(self,placaformat):
    placa=str(placaformat)
  
    numbers = placa[-4:]
    numbers = re.sub(r"[a-zA-Z]", "0", numbers)
    
    placa = placa[:3]+numbers;
    
    return placa
         