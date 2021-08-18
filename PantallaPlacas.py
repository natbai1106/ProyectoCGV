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



lblInfo = Label(principal, textvariable=placa, font=(18))
lblInfo.config(bg="blanched almond")
lblInfo.config(font="Arial")
lblInfo.place(x=115, y=70)

frameDatos = Frame()
frameDatos.place(x=50, y=100)
frameDatos.config(bg="white")
frameDatos.config(width="250", height="400")
frameDatos.config(bd=2, relief="solid")

btn1 = Button(frameDatos, text="PENDIENTE")
btn1.place(x=10, y=300)
btn2 = Button(frameDatos, text="PENDIENTE")
btn2.place(x=120, y=300)

principal.geometry("1024x680")
principal.resizable(0,0)
principal.mainloop()

