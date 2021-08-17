from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import cv2
import imutils
import numpy as np

def elegir_imagen():
    # Especificar los tipos de archivos, para elegir solo a las imágenes
    path_image = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])

    if len(path_image) > 0:
        global image

        # Leer la imagen de entrada y la redimensionamos
        image = cv2.imread(path_image)
        image= imutils.resize(image, height=380)
        # Para visualizar la imagen de entrada en la GUI
        imageToShow= imutils.resize(image, width=180)
        imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow )
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        
        # Label IMAGEN DE ENTRADA
        lblInfo1 = Label(ventana, text="IMAGEN DE ENTRADA:")
        lblInfo1.grid(column=0, row=1, padx=5, pady=5)
        # Al momento que leemos la imagen de entrada, vaciamos
        # la iamgen de salida y se limpia la selección de los
        # radiobutton
        #lblOutputImage.image = ""
        #selected.set(0)

#image = None

ventana = Tk()
ventana.title("Principal")

#LABEL DONDE SE MOSTRARA LA IMAGEN DE ENTRADA
lblInputImage = Label(ventana)
lblInputImage.grid(column=0, row=2)
#ventana.geometry("1366x768")
botonCargar = Button(ventana, text="Elegir una imagen", width=25, command=elegir_imagen)
botonCargar.grid(column=0, row=0, padx=5, pady=5)

#frame1 = Frame(ventana,bg="blue")
#frame1.grid(column=0, row=2, padx=5, pady=5)

#frame2 = Frame(ventana,bg="yellow")
#frame2.pack(expand=True, fill='both')
#frame2.config(cursor='hand1')

#redButton = Button(frame1,text="Red", fg="red")
#greenButton = Button(frame1,text="Green", fg="green")
#blueButton = Button(frame1,text="Blue", fg="blue")

#redButton.place(relx=.05,rely=.05, relwidth=.25,relheight=.9)
#greenButton.place(relx=.35,rely=.05, relwidth=.25,relheight=.9)
#blueButton.place(relx=.65,rely=.05, relwidth=.25,relheight=.9)

#blackButton = Button(frame2, text="Black", fg="black")
#blackButton.pack()

ventana.mainloop()
