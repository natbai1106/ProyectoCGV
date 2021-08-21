from tkinter import *
from tkinter import messagebox
from modelos import read_text
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk

def next_photo_event():
    messagebox.showinfo(message="Mensaje", title="Título")
principal = Tk()
principal.title("Placas")
principal.configure(bg="blanched almond")
frameSecundario = Frame()
frameSecundario.place(x=335, y=50)
frameSecundario.config(bg="white")
frameSecundario.config(width="450", height="350")
frameSecundario.config(bd=25)
frameSecundario.config(bd=2, relief="ridge")

frameFactura = Frame()
frameFactura.place(x=335, y=450)
frameFactura.config(bg="white")
frameFactura.config(width="450", height="150")
frameFactura.config(bd=25)
frameFactura.config(bd=2, relief="ridge")
btnFactura = Button(frameFactura, text="PENDIENTE")
btnFactura.place(x=35, y=100)

lblFactura = Label(principal, text="F  A  C  T  U  R  A", font=(20))
lblFactura.config(bg="blanched almond")
lblFactura.config(font="Arial")
lblFactura.place(x=490, y=420)

lblCar = Label(frameSecundario, text="vehiculo", font=(18))
lblCar.config(bg="blanched almond")
lblCar.config(font="Arial")

car = read_text.process_image()
image =car.get_processed_image(ruta="ProyectoCGV/images/c2.jpg")
#image =car.placa;

placa = StringVar()
# Para visualizar la imagen en lblOutputImage en la GUI
im = Image.fromarray(image)
img = ImageTk.PhotoImage(image=im)
lblCar.configure(image=img)
lblCar.image = img
placa.set(car.text)
lblCar.place(x=0, y=0)
btnSiguiente = Button(frameSecundario, textvariable=placa,command=next_photo_event)

btnSiguiente.place(x=10, y=300)

lblInfo = Label(principal, text="Placa del Vehículo: " + str(placa), font=(16))
lblInfo.config(bg="blanched almond")
lblInfo.config(font="Arial")
lblInfo.place(x=70, y=20)

lblImagenPlaca = Label(principal, text="Imagen del Vehículo" + str(placa), font=(16))
lblImagenPlaca.config(bg="blanched almond")
lblImagenPlaca.config(font="Arial")
lblImagenPlaca.place(x=450, y=20)

lblReporte = Label(principal, text="Reporte" + str(placa), font=(16))
lblReporte.config(bg="blanched almond")
lblReporte.config(font="Arial")
lblReporte.place(x=875, y=20)

frameDatos = Frame()
frameDatos.place(x=50, y=50)
frameDatos.config(bg="white")
frameDatos.config(width="250", height="550")
#(width="450", height="350")
frameDatos.config(bd=2, relief="ridge")
lblDuenio = Label(frameDatos, text="Propietario:")
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=10)
lblDuenio = Label(frameDatos, text="Placa:")
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=70)
lblDuenio = Label(frameDatos, text="Marca:")
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=130)
lblDuenio = Label(frameDatos, text="Modelo:")
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=190)
lblDuenio = Label(frameDatos, text="Color:")
lblDuenio.config(font="Arial", bg="White", pady=10)
lblDuenio.place(x=5, y=250)

btn1 = Button(principal, text="PENDIENTE")
btn1.place(x=50, y=625)
btn1.config(height=2, width=25)
btn2 = Button(principal, text="PENDIENTE")
btn2.place(x=325, y=625)
btn2.config(height=2, width=25)
btn3 = Button(principal, text="PENDIENTE")
btn3.place(x=630, y=625)
btn3.config(height=2, width=25)
btn4 = Button(principal, text="PENDIENTE")
btn4.place(x=887, y=625)
btn4.config(height=2, width=25)

frameReportes = Frame()
frameReportes.place(x=820, y=50)
frameReportes.config(bg="white")
frameReportes.config(width="250", height="550")
frameReportes.config(bd=2, relief="ridge")

principal.geometry("1120x720")
principal.resizable(0,0)
principal.mainloop()