import cv2
import numpy as np
import os
import random
class Utilidades:
    def __init__(self) -> None:
        pass
    def points_template_matching(image, template):
        points = []
        threshold = 0.9
        res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        candidates = np.where(res >= threshold)
        candidates = np.column_stack([candidates[1], candidates[0]])
        i = 0
        while len(candidates) > 0:
            if i == 0: points.append(candidates[0])
            else:
                to_delete = []
                for j in range(0, len(candidates)):
                    diff = points[i-1] - candidates[j]
                    if abs(diff[0]) < 10 and abs(diff[1]) < 10:
                        to_delete.append(j)
                candidates = np.delete(candidates, to_delete, axis=0)
                if len(candidates) == 0: break
                points.append(candidates[0])
            i += 1
        return points
    def redimencionar(image,scale):
        width = int(image.shape[1] * scale / 100)
        height = int(image.shape[0] * scale / 100)
        dimension = (width, height)
        return cv2.resize(image, dimension)

    def get_imagenes(ruta):
        contenido = os.listdir(ruta)
        imagenes=[]
        for fichero in contenido:
            if os.path.isfile(os.path.join(ruta,fichero)) and (fichero.endswith('.jpg') or fichero.endswith('.png')):
                #leemos las imagenes y las guardamos en un arreglo para retornarlas
                temp=cv2.imread(os.path.join(ruta,fichero),cv2.COLOR_BGR2GRAY)
                imagenes.append(temp)
        return  imagenes
    '''    
    #Se declarran dos arreglos que contendran los dos tanto los gatos como los perros
    image_gray = cv2.imread("CatsAndDogs.jpg",cv2.COLOR_BGR2GRAY)

    carpetas=[["temp_cats/","Gatos "], ["temp_dogs/","Perros "]]
    h,w=40,0
    for directorio in carpetas:#primero se obtienen todas las cartpetas de donde se quiere obtener datos
        #y se obtienen todas las imagenes que estan dentro
        w=w+600
        b=random.randrange(0, 255, 3)#se genera una variacion del color azul para que varie el color en cada tiro
        g=random.randrange(0, 255, 2)
        r=random.randrange(0, 255, 5)
        templates= get_imagenes(directorio[0])
        num_coincidencias=0
        for template in templates:#Se recorren todas las imagenes contendidas en el fichero
            #Se concatena todos los puntos que coinciden con la imagen actual, ademas se almacena las dimenciones del template para 
            #dibujar el recuadro
            points =points_template_matching(image_gray, template)
            for point in points:
                x1, y1 =point[0],point[1]
                x2, y2 =point[0] + template.shape[1],point[1] + template.shape[0]
                cv2.rectangle(image_gray, (x1, y1), (x2, y2), (b,g,r), 2)
                num_coincidencias+=1
        #msg="Número de ",directorio[0]," : ",(len(points))
        cv2.putText(image_gray,f"{directorio[1]} : {num_coincidencias}", (w, h),cv2.FONT_HERSHEY_PLAIN, 2 ,(b, g,r),2)

    cv2.imshow("Image",redimencionar(image_gray,55))
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''