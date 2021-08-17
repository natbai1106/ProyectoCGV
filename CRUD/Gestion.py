from tkinter import *
from tkinter import ttk 
from db import *

class Gestion:
    def __init__(self, master):
        self.ventana = master
        self.DibujarLabel()
        self.DibujarEntry()
        self.DibujarBoton()
        self.DibujarLista()
    
    def DibujarLabel(self):
        #self.lbl_id = Label(self.ventana, foreground="white", background="#314252", text="Id:", font=(8)).place(x=50, y=110)
        self.lbl_name = Label(self.ventana, foreground="white", background="#314252", text="Nombre:", font=(8)).place(x=50, y=110)
        self.lbl_identidad = Label(self.ventana, foreground="white", background="#314252", text="Identidad:", font=(8)).place(x=50, y=160)
        self.lbl_direccion = Label(self.ventana, foreground="white", background="#314252", text="Dirección:", font=(8)).place(x=50, y=210)
        self.lbl_telefono = Label(self.ventana, foreground="white", background="#314252", text="Teléfono:", font=(8)).place(x=50, y=260)
        self.lbl_tipo_persona = Label(self.ventana, foreground="white", background="#314252", text="Tipo Persona:", font=(8)).place(x=50, y=310)

    def DibujarEntry(self):
        #self.id = StringVar()
        self.nombre = StringVar()
        self.identidad = StringVar()
        self.direccion = StringVar()
        self.telefono = StringVar()
        self.tipoPersona = StringVar()
        #self.txtId = Entry(self.ventana, font = ('Arial',12),textvariable = self.id).place(x=160, y=110)
        self.txtNombre = Entry(self.ventana, font = ('Arial',12),textvariable = self.nombre).place(x=160, y=110)
        self.txtIdentidad = Entry(self.ventana, font = ('Arial',12),textvariable = self.identidad).place(x=160, y=160)
        self.txtDireccion = Entry(self.ventana, font = ('Arial',12),textvariable = self.direccion).place(x=160, y=210)
        self.txtTelefono = Entry(self.ventana, font = ('Arial',12),textvariable = self.telefono).place(x=160, y=260)
        self.txtTipoPersona = Entry(self.ventana, font = ('Arial',12),textvariable = self.tipoPersona).place(x=160, y=310)

    def DibujarBoton(self):
        self.btnGuardar = Button(self.ventana, text="Guardar", relief="flat", background="#0051C8", cursor = "hand2", foreground ="white", command = lambda: self.guardar()).place(x=750, y=340, width="90")
        self.btnCancelar = Button(self.ventana, 
                        text="Cancelar", 
                        relief="flat", 
                        background="red", 
                        cursor = "hand2", 
                        foreground ="white"
                        ).place(x=850, y=340, width="90")

    def guardar(self):
        arr = [self.nombre.get(), self.identidad.get(), self.direccion.get(), self.telefono.get(),self.tipoPersona.get()]
        d = Database()
        d.InsertItems(arr)
        #self.id.set("")
        self.nombre.set("")
        self.identidad.set("")
        self.direccion.set("")
        self.telefono.set("")
        self.tipoPersona.set("")
        self.LimpiarLista()
        self.DibujarLista()

    def LimpiarLista(self):
        self.lista.delete(*self.lista.get_children())


    def DibujarLista(self):
        self.lista = ttk.Treeview(self.ventana, columns=(1,2,3,4,5,6),show="headings", height="9")
        # estilo
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Treeview.Heading", background="#0051C8", relief="flat", foreground="white")
        self.lista.heading(1, text="Id")
        self.lista.heading(2, text="Nombre")
        self.lista.heading(3, text="Identidad")
        self.lista.heading(4, text="Dirección")
        self.lista.heading(5, text="Teléfono")
        self.lista.heading(6, text="Tipo Persona")
        self.lista.column(1, anchor=CENTER, width="50")
        self.lista.column(2, anchor=CENTER, width="200")
        self.lista.column(3, anchor=CENTER, width="100")
        self.lista.column(4, anchor=CENTER, width="300")
        self.lista.column(5, anchor=CENTER, width="100")
        self.lista.column(6, anchor=CENTER, width="100")

        d = Database()
        elements = d.returnAllElements()
        for i in elements:
            self.lista.insert('','end', values=i)
        self.lista.place(x=430, y=110)
        
root = Tk()
root.title("CRUD de Gestión") 
root.geometry("1366x768")
root.config(background="#314252")
aplication = Gestion(root)
root.mainloop()