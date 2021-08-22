 
from cv2 import FORMATTER_FMT_MATLAB
from mysql.connector import cursor
from pymysql import cursors
from CRUD.db import Database
from tkinter import *
from tkinter import messagebox

from modelos import read_text
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from tkinter import ttk
from imutils import paths
from modelos import person
from datetime import datetime, timedelta,date
import time
rutaFotos = sorted(list(paths.list_images("images/")))
index  =  0
car = read_text.process_image()
persona = person.Person()
widthCenter = "610"


def next_photo():
    if len(rutaFotos)>0:
        global index
        
        image =car.get_processed_image(ruta=rutaFotos[index])
        # Para visualizar la imagen en lblOutputImage en la GUI
        im = Image.fromarray(image)
        img = ImageTk.PhotoImage(image=im)
        lblCar.configure(image=img)
        lblCar.image = img
        placa.set("Placa: "+ car.text)
        info_owner = persona.get_info_owner(car.text)   
        if info_owner is not None:
            propitario.set("Propietario: "+str(info_owner[0]))
            marca.set("Marca: "+str(info_owner[2]))
            modelo.set("Modelo: "+str(info_owner[3]))
            color.set("Color: "+info_owner[4])
            cantidadejes.set("Cantidad ejes: "+str(info_owner[8]))
            precio.set("Precio: "+ str(info_owner[6]))
            #se extraen todos los reportes del vehiculo
            reportes =persona.get_reports_vehicle(str(info_owner[5]))
            DibujarLista(frameReportes,reportes)
            if car.text != "Nos0000":
                #Se conparan las fechas
                now = str(date.today());
                vencimiento=str(info_owner[7])
                fecha_vencimiento = time.strptime(vencimiento, "%Y-%m-%d")
                fecha_actual = time.strptime(now, "%Y-%m-%d")
                if fecha_actual > fecha_vencimiento:
                    messagebox.showinfo("Fecha de facturación vencidad","La fecha de pago de facturas esta vencida, se agregara a la tabla de reportes")
                    persona.InsertItems([str(info_owner[5]),2])
        if index >= len(rutaFotos)-1:
            index=0
        else:
            index+=1
def DibujarLista(frame,reportes=None):

    lista = ttk.Treeview(frame, columns=(1),show="headings", height="9")
    # estilo
    estilo = ttk.Style()
    estilo.theme_use("clam")
    
    estilo.configure("Treeview.Heading", background="#0051C8", relief="flat", foreground="white")
    lista.heading(1, text="Reportes del vehiculo")
    lista.column(1, anchor=CENTER, width="100")

    if len(reportes)>0:
        lblReporte.config(fg="red")
        alertaReport.set("ALERTA! Vehiculo con reporte")
        for reporte  in reportes:
            lista.insert('','end', values=reporte)
    else:
        lblReporte.config(fg="green")
        alertaReport.set("Sin reportes")
 
        
    lista.place(x=0, y=30,width=widthCenter)         


principal = Tk()
placa = StringVar(value="Placa: ")
propitario=StringVar(value="Propietario: ")
cantidadejes =StringVar(value="Cantidad ejes: ") 
precio = StringVar(value="Precio: ")

marca=StringVar(value="Marca: ")
modelo=StringVar(value="Modelo: ")
color=StringVar(value="Color: ")
alertaReport = StringVar(value="Sin reporte")
principal.title("Placas")
principal.configure(bg="blanched almond")
frameSecundario = Frame()
frameSecundario.place(x=335, y=50)
frameSecundario.config(bg="white")
frameSecundario.config(width=widthCenter, height="450")
frameSecundario.config(bd=25)
frameSecundario.config(bd=2, relief="ridge")

frameReportes = Frame()
frameReportes.place(x=335, y=490)
frameReportes.config(bg="white")
frameReportes.config(width=widthCenter, height="150")
frameReportes.config(bd=25)
frameReportes.config(bd=2, relief="ridge")
btnFactura = Button(frameReportes, text="PENDIENTE")
btnFactura.place(x=35, y=100)



lblCar = Label(frameSecundario, text="vehiculo", font=(18))
lblCar.config(bg="blanched almond")
lblCar.config(font="Arial")
lblCar.place(x=0, y=0)
#next_photo()#Se llama a la funcion next foto para que cargue un carro por defecto


btnSiguiente = Button(frameSecundario, text="Siguiente",command=next_photo)
btnSiguiente.config(width=10, height=2, font=(16))
btnSiguiente.place(x=500, y=380)

lblInfo = Label(principal, textvariable=placa, font=(16))
lblInfo.config(bg="blanched almond")
lblInfo.config(font="Arial")
lblInfo.place(x=80, y=20)

lblImagenPlaca = Label(principal, text="Imagen del Vehículo", font=(16))
lblImagenPlaca.config(bg="blanched almond")
lblImagenPlaca.config(font="Arial")
lblImagenPlaca.place(x=570, y=20)

lblFactura = Label(principal, text="Ticket de Pago", font=(16))
lblFactura.config(bg="blanched almond")
lblFactura.config(font="Arial")
lblFactura.place(x=1050, y=20)

frameDatos = Frame()
frameDatos.place(x=50, y=50)
frameDatos.config(bg="white")
frameDatos.config(width="250", height="550")
#(width="450", height="350")
frameDatos.config(bd=2, relief="ridge")
lblDuenio = Label(frameDatos, textvariable=propitario)
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=10)
lblDuenio = Label(frameDatos, textvariable=placa)
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=70)
lblDuenio = Label(frameDatos, textvariable=marca)
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=130)
lblDuenio = Label(frameDatos, textvariable=modelo)
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=190)
lblDuenio = Label(frameDatos, textvariable=color)
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=250)

btn1 = Button(principal, text="PENDIENTE")
btn1.place(x=75, y=625)
btn1.config(height=2, width=25)
#btn2 = Button(principal, text="PENDIENTE")
#btn2.place(x=325, y=625)
#btn2.config(height=2, width=25)
#btn3 = Button(principal, text="PENDIENTE")
#btn3.place(x=630, y=625)
#btn3.config(height=2, width=25)
btn4 = Button(principal, text="PENDIENTE")
btn4.place(x=1020, y=625)
btn4.config(height=2, width=25)

frameFactura = Frame() 
frameFactura.place(x=980, y=50)
frameFactura.config(bg="white")
frameFactura.config(width="250", height="550")
frameFactura.config(bd=2, relief="ridge")

lblFactura = Label(frameFactura, text="PEAJE PUERTO CORTES")
lblFactura.config(font="Arial", bg="White", pady=10)
lblFactura.place(x=25, y=10)
lblFactura = Label(frameFactura, textvariable=cantidadejes)
lblFactura.config(font="Arial", bg="White", pady=10)
lblFactura.place(x=5, y=70)
lblFactura = Label(frameFactura, textvariable=precio)
lblFactura.config(font="Arial", bg="White", pady=10)
lblFactura.place(x=5, y=130)
lblFactura = Label(frameFactura, text="Código de Peaje: ")
lblFactura.config(font="Arial", bg="White", pady=10)
lblFactura.place(x=5, y=190)
lblFactura = Label(frameFactura, text="Feliz Viaje!!!")
lblFactura.config(font="Arial", bg="White", pady=10)
lblFactura.place(x=80, y=250)


lblReporte = Label(frameReportes, textvariable=alertaReport)
lblReporte.config(bg="white")
lblReporte.config(font=("Arial",18,"bold"))
lblReporte.config(foreground="#0EAA10")
lblReporte.place(x=0, y=0)


principal.geometry("1280x680")

principal.resizable(0,0)
principal.mainloop()