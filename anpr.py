
from skimage.segmentation import clear_border
import pytesseract
import numpy as np
import imutils
import cv2
from pytesseract.pytesseract import TesseractError
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
'''#se crea la Clase
class DetectANPR:
    def __init__(self,minAR=4, maxAR=5,debug=False):
        # almacenar la relación de aspecto rectangular mínima y máxima
        # establecemos si estamos en modo debug para mostrar todo lo que sucede
        self.minAR=minAR
        self.maxAR= maxAR
        self.debug=debug
    #definimos un metodo para mostrar los resultados de las operaciones, en especifico el debug
      def debug_imshow(self,title,image,waitKey=False):
        if self.debug:#si esta habilitado el debug entonces mostrara la imagen en el proceso
            cv2.imshow(title,image)
            if waitKey:#si waitkey es true espera una tecla para continuar
                cv2.waitKey(0)

    #creamos una funcion para optener las posibles placas en una imagen
    def locate_licence_plate_candidates(self,gray,keep=5): #gray= imagen en escala de grises, keep= numero de candidatos a retornar
        # realizar una operación morfológica de blackhat permite
        # revelar regiones oscuras ( texto) sobre fondos claros
        # (la propia matrícula) 
        rectKern = cv2.getStructuringElement(cv2.MORPH_RECT,(13,5))#13,5 es la medida de la placa
        blackHat= cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT,rectKern)
        self.debug_imshow("blackhat",blackHat)

        #se empiezan a buscar las regiones que sean claras 
        squareKern =cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        ligth = cv2.morphologyEx(gray,cv2.MORPH_BLACKHAT,squareKern)
        ligth = cv2.threshold(ligth,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        self.debug_imshow("Regiones claras",ligth)

        # calcular la representación de gradiente de Scharr del sombrero negro
        # imagen en la dirección xy luego escale el resultado a
        # el rango [0, 255]
        gradX=cv2.Sobel(blackHat, ddepth=cv2.CV_32F,dx=1,dy=0,ksize=-1)
        gradX = np.absolute(gradX)
        (minVal,maxVal)=np.min(gradX),np.max(gradX)
        gradX= 255*((gradX-minVal)/(maxVal-minVal))
        gradX = gradX.astype("uint8")
        self.debug_imshow("Scharr",gradX)
        
        # difuminar la representación del degradado, aplicando un cierre
        # con la operación umbral de la imagen usando el método de Otsu
        gradX =cv2.GaussianBlur(gradX,(5,5),0)
        gradX=cv2.morphologyEx(gradX,cv2.MORPH_CLOSE,rectKern)
        tresh=cv2.threshold(gradX,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
        self.debug_imshow("Tresh binario",tresh)

        # se realiza una serie de erosiones y dilataciones para limpiar el
        # el ruido de la image del umbral
        tresh = cv2.erode(tresh,None,iterations=2)
        tresh= cv2.dilate(tresh,None,iterations=2)
        self.debug_imshow("Gradiete dilatado/erosionado",tresh)

        #tomar el AND bit a bit entre el resultado
        #del umbral y las regiones claras de la imagen
        tresh = cv2.bitwise_and(tresh,tresh,mask=ligth)
        tresh = cv2.dilate(tresh,None,iterations=2  )
        tresh = cv2.erode(tresh,None,iterations=1)
        self.debug_imshow("Imagen final", tresh,waitKey=True)#esperamos una tecla para seguir

        #ahora se econtraran los contornos
        cnts=cv2.findContours(tresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts =imutils.grab_contours(cnts)
        cnts = sorted(cnts,key=cv2.contourArea,reverse=True)[:keep]#Nos retorna el numero que hayamos establecido
        
        return cnts#retorna todos los contornos

    def locate_plate_license(self,gray,candidates,clearBorder=False):
        lpCnt=None #contorno de la placa
        roi=None #region de interes

        #se evaluan los candidatos
        for c in candidates:
            (x,y,w,h)=cv2.boundingRect(c)
            ar=w/float(h)#se calcula la relacion de aspecto  y valida si esta dentro de los parametro establecidos
            if ar>=self.minAR and ar<=self.maxAR:
                lpCnt=c
                licenPlate = gray[y:y+h,x:x+w]
                roi = cv2.threshold(licenPlate,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)[1]
                #comprobar para ver si debemos borrar algún primer plano
                #píxeles tocando el borde de la imagen
                #(que normalmente, no siempre, indica ruido
                if clear_border:
                    roi= clear_border(roi)
                self.debug_imshow("licen plate",licenPlate)
                self.debug_imshow("roi",roi,waitKey=True)
        return (roi,lpCnt)

    def find_and_ocr(self,image,psm=7,clearBorder=False):
        lpText=None
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (x,y,w,h)=self.get_roi(gray)
        gray=gray[y:y+h,x:x+w]
        candidates =self.locate_licence_plate_candidates(gray)
        (lp,lpCnt)=self.locate_plate_license(gray,candidates,clearBorder==clearBorder)
        if lp is not None:#valida que la placa no este vacia
            options="-l eng --oem 1 --psm {}".format(psm)
            lpText=pytesseract.image_to_string(lp,config=options)
        return(lpText,lpCnt)
   
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
        return int(x1),int(y1),int(w),int(h)'''
# import the necessary packages

class DetectANPR:
    def __init__(self, minAR=4, maxAR=5, debug=False):
        # store the minimum and maximum rectangular aspect ratio
        # values along with whether or not we are in debug mode
        self.minAR = minAR
        self.maxAR = maxAR
        self.debug = debug
    def debug_imshow(self, title, image, waitKey=False):
        # check to see if we are in debug mode, and if so, show the
        # image with the supplied title
        if self.debug:
            cv2.imshow(title, image)
            # check to see if we should wait for a keypress
            if waitKey:
                cv2.waitKey(0)
    def locate_license_plate_candidates(self, gray, keep=5):
        # perform a blackhat morphological operation that will allow
        # us to reveal dark regions (i.e., text) on light backgrounds
        # (i.e., the license plate itself)
        rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 13))
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKern)
        self.debug_imshow("Blackhat", blackhat)
        # next, find regions in the image that are light
        squareKern = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        light = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, squareKern)
        light = cv2.threshold(light, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.debug_imshow("Light Regions", light)
        # compute the Scharr gradient representation of the blackhat
        # image in the x-direction and then scale the result back to
        # the range [0, 255]
        gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F,
            dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
        gradX = gradX.astype("uint8")
        self.debug_imshow("Scharr", gradX)
        # blur the gradient representation, applying a closing
        # operation, and threshold the image using Otsu's method
        gradX = cv2.GaussianBlur(gradX, (5, 5), 0)
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKern)
        thresh = cv2.threshold(gradX, 0, 255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        self.debug_imshow("Grad Thresh", thresh)
        # perform a series of erosions and dilations to clean up the
        # thresholded image
        thresh = cv2.erode(thresh, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        self.debug_imshow("Grad Erode/Dilate", thresh)
        # take the bitwise AND between the threshold result and the
        # light regions of the image
        thresh = cv2.bitwise_and(thresh, thresh, mask=light)
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh = cv2.erode(thresh, None, iterations=1)
        self.debug_imshow("Final", thresh, waitKey=True)
        # find contours in the thresholded image and sort them by
        # their size in descending order, keeping only the largest
        # ones
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]
        # return the list of contours
        return cnts
    def locate_license_plate(self, gray, candidates,
        clearBorder=False):
        # initialize the license plate contour and ROI
        lpCnt = None
        roi = None
        # loop over the license plate candidate contours
        for c in candidates:
            # compute the bounding box of the contour and then use
            # the bounding box to derive the aspect ratio
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            # check to see if the aspect ratio is rectangular
            if ar >= self.minAR and ar <= self.maxAR:
                # store the license plate contour and extract the
                # license plate from the grayscale image and then
                # threshold it
                lpCnt = c
                licensePlate = gray[y:y + h, x:x + w]
                roi = cv2.threshold(licensePlate, 0, 255,
                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                # check to see if we should clear any foreground
                # pixels touching the border of the image
                # (which typically, not but always, indicates noise)
                if clearBorder:
                    roi = clear_border(roi)
                # display any debugging information and then break
                # from the loop early since we have found the license
                # plate region
                self.debug_imshow("License Plate", licensePlate)
                self.debug_imshow("ROI", roi, waitKey=True)
                break
        # return a 2-tuple of the license plate ROI and the contour
        # associated with it
        return (roi, lpCnt)
    def find_and_ocr(self, image, psm=7, clearBorder=False):
        # initialize the license plate text
        lpText = None
        # convert the input image to grayscale, locate all candidate
        # license plate regions in the image, and then process the
        # candidates, leaving us with the *actual* license plate
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        candidates = self.locate_license_plate_candidates(gray)
        (lp, lpCnt) = self.locate_license_plate(gray, candidates,
            clearBorder=clearBorder)
        # only OCR the license plate if the license plate ROI is not
        # empty
        if lp is not None:
            # OCR the license plate
            options = self.build_tesseract_options(psm=psm)
            lpText = pytesseract.image_to_string(lp, config=options)
            self.debug_imshow("License Plate", lp)
        # return a 2-tuple of the OCR'd license plate text along with
        # the contour associated with the license plate region
        return (lpText, lpCnt)        
        
  

