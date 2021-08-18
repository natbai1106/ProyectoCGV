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
frameSecundario.place(x=350, y=100)
frameSecundario.config(bg="white")
frameSecundario.config(width="650", height="350")
frameSecundario.config(bd=25)
frameSecundario.config(bd=2, relief="ridge")

lblCar = Label(frameSecundario, text="vehiculo", font=(18))
lblCar.config(bg="blanched almond")
lblCar.config(font="Arial")
car = read_text.process_image()
image =car.get_processed_image()
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
lblInfo.place(x=70, y=70)

frameDatos = Frame()
frameDatos.place(x=50, y=100)
frameDatos.config(bg="white")
frameDatos.config(width="250", height="400")
frameDatos.config(bd=2, relief="solid")
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

btn1 = Button(frameDatos, text="PENDIENTE")
btn1.place(x=35, y=350)
btn2 = Button(frameDatos, text="PENDIENTE")
btn2.place(x=140, y=350)

principal.geometry("1024x680")
principal.resizable(0,0)
principal.mainloop()