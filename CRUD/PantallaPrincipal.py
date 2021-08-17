from tkinter import *

ventana = Tk()
ventana.title("Principal")
ventana.geometry("1366x768")

frame1 = Frame(ventana,bg="blue")
frame1.pack(expand=True, fill='both')

frame2 = Frame(ventana,bg="yellow")
frame2.pack(expand=True, fill='both')
frame2.config(cursor='hand1')

redButton = Button(frame1,text="Red", fg="red")
greenButton = Button(frame1,text="Green", fg="green")
blueButton = Button(frame1,text="Blue", fg="blue")

redButton.place(relx=.05,rely=.05, relwidth=.25,relheight=.9)
greenButton.place(relx=.35,rely=.05, relwidth=.25,relheight=.9)
blueButton.place(relx=.65,rely=.05, relwidth=.25,relheight=.9)

blackButton = Button(frame2, text="Black", fg="black")
blackButton.pack()

ventana.mainloop()