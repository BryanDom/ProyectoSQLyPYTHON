#Proyecto "Hospital"
#Hecho por Brayan Domínguez Saucedo
#Fecha de entrega: 4 de diciembre del 2020

from tkinter import * #importar todo lo de tkinter
import sqlite3
import tkinter.messagebox
conn = sqlite3.connect("aqui ingresar la ubicación de SQL") #En este apartado hago conección con sqlite ingresando la ubicación de mi archivo
c = conn.cursor() #nombro a "c" como el cursor para hacer las respectivas consultas


ventana = tkinter.Tk()
ventana.title ("Hospital Brayan") #Este es el titulo de la ventana
ventana.geometry("1920x1080") #Las dimenciones que tendra la ventana
imagen = PhotoImage(file="hospital.png")
fondo = Label (ventana,image=imagen).place(x=0,y=0)
#Todo es un objeto, incluyendo los tipos y clases.
#Permite herencia múltiple.
#No existen métodos ni atributos privados.
#Los atributos pueden ser modificados directamente.
#Asi que utilice programacion orientada a objetos

#Esta clase sirve para agregar un paciente pidiendo datos necesarios.
class Agregar_Paciente:
    def __init__(self, nuevaVentana=None): #_init_ Este método se llama cuando se crea un objeto a partir de una clase y permite que la clase inicialice los atributos de la clase. (Se llama constructor en terminología orientada a objetos)
        self.nuevaVentana = nuevaVentana = tkinter.Toplevel(ventana) #La palabra "self" se utiliza para representar la instancia de una clase. Al usar la palabra clave "self" accedemos a los atributos y métodos de la clase en Python.
        self.nuevaVentana.geometry("800x500")
        self.nuevaVentana.configure(background="steelblue") #Color azul en el fondo
        self.nuevaVentana.resizable(False,False) #Sirve para que el usuario no pueda modificar la ventana, es decir que no modifique su tamaño
        self.nuevaVentana.title ("Consulta de pacientes")
        
        # Las etiquetas de las ventanas
        self.heading = Label(self.nuevaVentana, text="Hospital General (Agregar pacientes)",  fg='black', font=('arial 15 bold'), bg='steelblue')
        self.heading.place(x=150, y=0)
       
        # Rut del paciente
        self.Rut = Label(self.nuevaVentana, text="Rut del paciente", font=('arial 10 bold'), fg='black')
        self.Rut.place(x=0, y=100)

        # Nombre
        self.Nombre = Label(self.nuevaVentana, text="Nombre del paciente", font=('arial 10 bold'), fg='black')
        self.Nombre.place(x=0, y=140)

        # Edad
        self.Edad = Label(self.nuevaVentana, text="Edad del paciente", font=('arial 10 bold'), fg='black')
        self.Edad.place(x=0, y=180)


        #Entrada de las etiquetas
        self.Rut_ent = Entry(self.nuevaVentana, width=30)
        self.Rut_ent.place(x=250, y=100)

        self.Nombre_ent = Entry(self.nuevaVentana, width=30)
        self.Nombre_ent.place(x=250, y=140)
    
        self.Edad_ent = Entry(self.nuevaVentana, width=30)
        self.Edad_ent.place(x=250, y=180)

        # botón para ejecutar un comando
        self.submit = Button(self.nuevaVentana, text="Agregar Paciente", width=20, height=2, bg='red', command= self.add_appointment)
        self.submit.place(x=300, y=340)
    
    #funcióon para para agregar paciente a la base de datos
    def add_appointment(self):
        # obtenemos con "get" las entradas del usuario
        self.val1 = self.Rut_ent.get()
        self.val2 = self.Nombre_ent.get() #Obtenemos lo que ingreso el usuario con "get"
        self.val3 = self.Edad_ent.get()

        # comprobar si la entrada del usuario está vacía
        if self.val1 == '' or self.val2 == '' or self.val3 == '':
            tkinter.messagebox.showinfo("ADVERTENCIA", "Porfavor llene todas las casillas")
        else:
            #entonces si esta todo correcto, ahora agregamos a la base de datos
            sql = "INSERT INTO 'Pacientes' (Rut, Nombre, Edad) VALUES(?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3))
            # Guardamos los cambios haciendo un commit
            conn.commit()
            #Despliega una alerta de completado
            tkinter.messagebox.showinfo("Completado", "Cita para " +str(self.val2) + " ha sido creada." )
            self.nuevaVentana.destroy() #Se completa todo y destruye esa ventana
            
#Esta clase sirve para consultar un paciente y asi poder modificar, borrar dicho paciente.
class Consultar_Paciente:
    def __init__(self,nuevaVentana=None):
        self.nuevaVentana = nuevaVentana = tkinter.Toplevel(ventana)
        self.nuevaVentana.geometry("800x500")
        self.nuevaVentana.configure(background="steelblue") #Color naranja en el fondo
        self.nuevaVentana.resizable(False,False) #Sirve para que el usuario no pueda modificar la ventana, es decir que no modifique su tamaño
        self.nuevaVentana.title ("Consulta de pacientes")
        
        self.heading = Label(self.nuevaVentana, text="Bienvenido a consulta de pacientes",  fg='black', font=('arial 15 bold'), bg='steelblue')
        self.heading.place(x=150, y=0)
        # search criteria -->name 
        self.name = Label(self.nuevaVentana, text="Ingresa rut o Nombre del paciente")
        self.name.place(x=0, y=60)

        # ingresar rut del paciente
        self.namenet = Entry(self.nuevaVentana, width=30)
        self.namenet.place(x=280, y=62)

        # boton de buscar
        self.search = Button(self.nuevaVentana, text="Buscar..", width=12, height=1, bg='red', command=self.search_db)
        self.search.place(x=350, y=102)
        
    # función para buscar el paciente
    def search_db(self):
        self.input = self.namenet.get()
        
        #Seleccionar todo de la tabla pacientes donde rut sea igual a lo que ingreso el usuario
        buscar = c.execute("SELECT * FROM Pacientes WHERE Rut = '%s'"%(self.input))
        fila = buscar.fetchone()#Para obtener los resultados, podemos ahora llamar al método fetchone()
        #Ya que si hay más resultados que la memoria que tenemos disponible o si sólo queremos ir leyéndolos para hacer algo con ellos e ir descartando de memoria (por ejemplo, ir copiando los resultados a un fichero), podemos usar fetchone().

        
        # ejecutar sql con el cursor
        nombre = c.execute("SELECT * FROM Pacientes WHERE Nombre = '%s'"%(self.input))
        fila2 = nombre.fetchone()
 
        if ((fila != None) or (fila2 != None)):
            if fila !=None:
                sql = "SELECT * FROM Pacientes WHERE Rut LIKE ?"
                self.res = c.execute(sql, (self.input,))
                for self.row in self.res:
                    self.Rut = self.row[0]
                    self.Nombre = self.row[1]
                    self.Edad = self.row[2]
                
                # creamos el formulario de actualización
                self.uRut = Label(self.nuevaVentana, text="Rut del paciente")
                self.uRut.place(x=0, y=140)

                self.uNombre = Label(self.nuevaVentana, text="Nombre")
                self.uNombre.place(x=0, y=180)

                self.uEdad = Label(self.nuevaVentana, text="Edad")
                self.uEdad.place(x=0, y=220)

                # de entradas para cada etiqueta =========================================== =============
                # =================== llenando el resultado de la búsqueda en el cuadro de entrada para actualizar
                self.ent1 = Entry(self.nuevaVentana, width=30)
                self.ent1.place(x=300, y=140)
                self.ent1.insert(END, str(self.Rut))

                self.ent2 = Entry(self.nuevaVentana, width=30)
                self.ent2.place(x=300, y=180)
                self.ent2.insert(END, str(self.Nombre))

                self.ent3 = Entry(self.nuevaVentana, width=30)
                self.ent3.place(x=300, y=220)
                self.ent3.insert(END, str(self.Edad))

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # botón para ejecutar la actualización
                self.update = Button(self.nuevaVentana, text="Actualizar", width=20, height=2, bg='lightblue', command=lambda: [self.update_db(), self.nuevaVentana.destroy()])
                self.update.place(x=400, y=380)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # boton para borrar
                self.delete = Button(self.nuevaVentana, text="Borrar", width=20, height=2, bg='red', command=lambda: [self.delete_db(), self.nuevaVentana.destroy()])
                self.delete.place(x=150, y=380)
                
            elif fila2 != None:
                sql = "SELECT * FROM Pacientes WHERE Nombre LIKE ?" #Se busca por el nombre introducido por el usuario.
                
                #Se ejecuta el cursor
                self.res = c.execute(sql, (self.input,))
                for self.row in self.res:
                    self.Rut = self.row[0]
                    self.Nombre = self.row[1]
                    self.Edad = self.row[2]
                
                # creating the update form
                self.uRut = Label(self.nuevaVentana, text="Rut del paciente")
                self.uRut.place(x=0, y=140)

                self.uNombre = Label(self.nuevaVentana, text="Nombre")
                self.uNombre.place(x=0, y=180)

                self.uEdad = Label(self.nuevaVentana, text="Edad")
                self.uEdad.place(x=0, y=220)

               
                # de entradas para cada etiqueta =========================================== =============
                # =================== llenando el resultado de la búsqueda en el cuadro de entrada para actualizar
                self.ent1 = Entry(self.nuevaVentana, width=30)
                self.ent1.place(x=300, y=140)
                self.ent1.insert(END, str(self.Rut))

                self.ent2 = Entry(self.nuevaVentana, width=30)
                self.ent2.place(x=300, y=180)
                self.ent2.insert(END, str(self.Nombre))

                self.ent3 = Entry(self.nuevaVentana, width=30)
                self.ent3.place(x=300, y=220)
                self.ent3.insert(END, str(self.Edad))

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # botón para ejecutar la actualización
                self.update = Button(self.nuevaVentana, text="Actualizar", width=20, height=2, bg='lightblue', command=lambda: [self.update_db(), self.nuevaVentana.destroy()])
                self.update.place(x=400, y=380)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # boton de borrar
                self.delete = Button(self.nuevaVentana, text="Borrar", width=20, height=2, bg='red', command=lambda: [self.delete_db(), self.nuevaVentana.destroy()])
                self.delete.place(x=150, y=380)
        else:
            self.name = Label(self.nuevaVentana, text="Lo siento, el Rut/Nombre ingresado no se encuentra, ¿Desea Agendar una cita?",  fg='black', font=('arial 10 bold'), bg='steelblue')
            self.name.place(x=0, y=250)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="SI", width=12, height=1, bg='blue', command=lambda: [Agregar_Paciente(), self.nuevaVentana.destroy()])
            self.search.place(x=0, y=300)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="NO", width=12, height=1, bg='red', command=lambda: [despedida(), self.nuevaVentana.destroy()])
            self.search.place(x=250, y=300)
            
    #Funcion que actualiza la modificación que hizo el usuario en la base de datos
    def update_db(self):
        # declarando las variables para actualizar
        self.var1 = self.ent1.get() #modifica el Rut
        self.var2 = self.ent2.get() #modifica el nombre
        self.var3 = self.ent3.get() #modifica la edad
        #Si se ingreso nombre desde un principio
        query = "UPDATE Pacientes SET Rut=?, Nombre=?, Edad=? WHERE Nombre LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.namenet.get(),))
        conn.commit()
        
        #Si se ingreso un rut desde un principio
        query = "UPDATE Pacientes SET Rut=?, Nombre=?, Edad=? WHERE Rut LIKE ?"
        c.execute(query, (self.var1, self.var2, self.var3, self.namenet.get(),))
        conn.commit()
        tkinter.messagebox.showinfo("Actualizado", "Actualizado Exitosamente.")
        
    #Función que borra el paciente de la base de datos.
    def delete_db(self):
        #Este es para borrar si ingresamos con un nombre
        sql2 = "DELETE FROM Pacientes WHERE Nombre LIKE ?"
        c.execute(sql2, (self.namenet.get(),))
        # Guardamos los cambios haciendo un commit
        conn.commit()
        self.ent1.destroy()
        self.ent2.destroy()
        self.ent3.destroy()

        # Este es para borrar si ingresamos con un rut
        sql2 = "DELETE FROM Pacientes WHERE Rut LIKE ?"
        c.execute(sql2, (self.namenet.get(),))
        # Guardamos los cambios haciendo un commit
        conn.commit()
        tkinter.messagebox.showinfo("Éxito", "Borrado exitosamente")
        self.ent1.destroy()
        self.ent2.destroy()
        self.ent3.destroy()
        
#Función que despliega 
def despedida():
     tkinter.messagebox.showinfo("Mensaje", "Bien, Gracias por utilizar este apartado")

#Función para consultar Todos los pacientes registrados
def consulta():
    nuevaVentana = tkinter.Toplevel(ventana)
    nuevaVentana.title ("Pacientes registrados") #Este es el titulo de la ventana
    nuevaVentana.geometry("700x900") #Las dimenciones que tendra la ventana
    nuevaVentana.configure(background="blue") #Color naranja en el fondo
    c.execute("SELECT * FROM Pacientes")
    i=0 
    for Pacientes in c:
        for j in range(len(Pacientes)):
            e = Entry(nuevaVentana, width=20, fg='black') 
            e.grid(row=i, column=j)  #Usamos la variable i como índice para cada fila y la variable j como cada columna de datos.
            #El método grid es uno de los más empleados y fáciles de utilizar a la hora de empaquetar y posicionar objetos. Ya que recibe como parámetros row y column, es decir filas y columnas.
            #convirtiendo los widgets en una tabla bidimensional.
            #objeto.grid(row= ‘valor’, column= ‘valor’)
            e.insert(END, Pacientes[j])
        i=i+1
        

#Esta parte corresponde a un cuadro de texto que indica Escribir tu mensaje, bg es el color del cuadro y fg el de la fuente de escritura
cajatexto = tkinter.Label(ventana,text="Bienvenido al Hospital General De Brayan",font = ("arial 10 bold"), fg="black")
#Esta parte corresponde a la dimencion del cuadro del texto 
cajatexto.pack(padx=5,pady=4,ipadx=5,ipady=5,fill=tkinter.X)
#Es para agregar un boton y al momento de presionarlo, hace el proceso de la función y toma el dato de la "cajatexto"
boton_addpaciente = tkinter.Button(ventana,text="Agregar Paciente",fg="blue",command=Agregar_Paciente).place(x=500,y=200, width=400, height=80)
boton_consultar = tkinter.Button(ventana,text="Consultar Paciente",fg="blue",command=Consultar_Paciente).place(x=500,y=400, width=400, height=80)
boton_Pacientes = tkinter.Button(ventana,text="Consultar todos los pacientes",fg="blue",command=consulta).place(x=500,y=600, width=400, height=80)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

#Esta clase consulta la deuda que debe el paciente
class Consultar_Pago:
    #Función constructor para crear una nueva ventana
    def __init__(self,nuevaVentana=None):
        self.nuevaVentana = nuevaVentana = tkinter.Toplevel(ventana)
        self.nuevaVentana.geometry("1050x500")
        self.nuevaVentana.configure(background="steelblue") #Color naranja en el fondo
        self.nuevaVentana.resizable(False,False) #Sirve para que el usuario no pueda modificar la ventana, es decir que no modifique su tamaño
        self.nuevaVentana.title ("Consulta de pacientes")
        
        self.heading = Label(self.nuevaVentana, text="Bienvenido a consulta de pago",  fg='black', font=('arial 15 bold'), bg='steelblue')
        self.heading.place(x=550, y=0)
        # search criteria -->name 
        self.name = Label(self.nuevaVentana, text="Ingresa rut del paciente")
        self.name.place(x=500, y=60)

        # ingresar rut del paciente
        self.namenet = Entry(self.nuevaVentana, width=30)
        self.namenet.place(x=700, y=62)

        # boton de buscar
        self.search = Button(self.nuevaVentana, text="Buscar..", width=12, height=1, bg='red', command=self.search_db)
        self.search.place(x=800, y=102)
        
    # funcion para buscar el paciente ingresado por el usuario
    def search_db(self):
        self.input = self.namenet.get() #Se obtiene lo que ingreso el usuario con "get"
        
        buscar = c.execute("SELECT * FROM atenciones WHERE Rut = '%s'"%(self.input))
        fila = buscar.fetchone() #Para obtener los resultados, podemos ahora llamar al método fetchone()
        #Ya que si hay más resultados que la memoria que tenemos disponible o si sólo queremos ir leyéndolos para hacer algo con ellos e ir descartando de memoria (por ejemplo, ir copiando los resultados a un fichero), podemos usar fetchone().
 
        if fila !=None:
            sql = c.execute("SELECT Fecha FROM atenciones WHERE Rut = '%s'"%(self.input))
            i=0 
            for Rut in sql:
                for j in range(len(Rut)):
                    e = Entry(self.nuevaVentana, width=20, fg='black')
                    e.grid(row=i, column=j, padx=(10,50),pady=(45,0))#Usamos la variable i como índice para cada fila y la variable j como cada columna de datos.
                    #El método grid es uno de los más empleados y fáciles de utilizar a la hora de empaquetar y posicionar objetos. Ya que recibe como parámetros row y column, es decir filas y columnas.
                    #convirtiendo los widgets en una tabla bidimensional.
                    #objeto.grid(row= ‘valor’, column= ‘valor’)
                    e.insert(END, Rut[j])
                i=i+1
            self.heading = Label(self.nuevaVentana, text="Fechas de consulta",  fg='black', font=('arial 10 bold'), bg='steelblue')
            self.heading.place(x=0, y=0)
            
            
            sql = c.execute("SELECT Fecha, sum(Costo) FROM atenciones WHERE Rut = '%s'"%(self.input))
            i=0 
            for Rut in sql:
                for j in range(len(Rut)):
                    e = Entry(self.nuevaVentana, width=20, fg='black')
                    e.grid(row=i, column=j, padx=(10,50),pady=(45,0))#Usamos la variable i como índice para cada fila y la variable j como cada columna de datos.
                    #El método grid es uno de los más empleados y fáciles de utilizar a la hora de empaquetar y posicionar objetos. Ya que recibe como parámetros row y column, es decir filas y columnas.
                    #convirtiendo los widgets en una tabla bidimensional.
                    #objeto.grid(row= ‘valor’, column= ‘valor’)
                    e.insert(END, Rut[j])
                i=i+1
            self.heading = Label(self.nuevaVentana, text="DEUDA",  fg='red', font=('arial 10 bold'), bg='steelblue')
            self.heading.place(x=300, y=0)
    
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            # boton para borrar
            self.delete = Button(self.nuevaVentana, text="Pagar Deuda", width=15, height=2, bg='red', command=lambda: [self.ganancias(), self.delete_db(), self.nuevaVentana.destroy()])
            self.delete.place(x=280, y=100)
                
        else:
            self.name = Label(self.nuevaVentana, text="Lo siento, el Rut/Nombre ingresado no se encuentra, ¿Desea Agendar una cita?",  fg='black', font=('arial 10 bold'), bg='steelblue')
            self.name.place(x=0, y=250)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="SI", width=12, height=1, bg='blue', command=lambda: [Agregar_Paciente(), self.nuevaVentana.destroy()])
            self.search.place(x=0, y=300)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="NO", width=12, height=1, bg='red', command=lambda: [despedida(), self.nuevaVentana.destroy()])
            self.search.place(x=250, y=300)
            
    #Funcion para borrar el paciente cuando ya pago su deuda         
    def delete_db(self):
        # Este es para borrar si ingresamos con un rut
        sql2 = c.execute("DELETE FROM atenciones WHERE Rut = '%s'"%(self.input))
        # Guardamos los cambios haciendo un commit
        conn.commit()
        tkinter.messagebox.showinfo("Éxito", "Pagado Correctamente")
        
    #Función para agregar lo que se pago del paciente a la tabla de "Ganancias"
    def ganancias(self):
        #SELECT FORMAT(nombre_campo,'yyyy-MM-dd') as fecha FROM nombre_tabla;
        c.execute("SELECT sum(Costo) FROM atenciones WHERE Rut = '%s'"%(self.input))
        Costofinal = c.fetchone()
        temp = Costofinal[0]
        
        #INSERT INTO Table_Name (Column1_Name, Column2_Name,...) VALUES ('Column1_Value1', 'Column2_Value2',...),
        sql = ("INSERT INTO 'Ganancias' (Costos) VALUES(?)")
        c.execute(sql, (temp,))
        conn.commit()
        self.nuevaVentana.destroy() #Se completa todo y destruye esa ventana

        
boton_atenciones = tkinter.Button(ventana,text="Consultas de pago",fg="blue",command=Consultar_Pago).place(x=1000,y=200, width=400, height=80)

#Esta clase sirve para agregar una nueva consulta con un paciente
class Atencion_Paciente:
    #Función constructor que sirve para crear una ventana y poner sus etiquetas correspondientes
    def __init__(self,nuevaVentana=None):
        self.nuevaVentana = nuevaVentana = tkinter.Toplevel(ventana)
        self.nuevaVentana.geometry("800x500")
        self.nuevaVentana.configure(background="steelblue") #Color naranja en el fondo
        self.nuevaVentana.resizable(False,False) #Sirve para que el usuario no pueda modificar la ventana, es decir que no modifique su tamaño
        self.nuevaVentana.title ("Consulta de pacientes")
        
        self.heading = Label(self.nuevaVentana, text="Bienvenido a consulta",  fg='black', font=('arial 15 bold'), bg='steelblue')
        self.heading.place(x=150, y=0)
        
        self.name = Label(self.nuevaVentana, text="Ingresa rut o nombre del paciente")
        self.name.place(x=0, y=60)

        # ingresar rut del paciente
        self.namenet = Entry(self.nuevaVentana, width=30)
        self.namenet.place(x=280, y=62)

        # boton de buscar
        self.search = Button(self.nuevaVentana, text="Buscar..", width=12, height=1, bg='red', command=self.search_db)
        self.search.place(x=350, y=102)
        
    # función para buscar el paciente que se ingreso
    def search_db(self):
        self.input = self.namenet.get()
        
        buscar = c.execute("SELECT * FROM Pacientes WHERE Rut = '%s'"%(self.input))
        fila = buscar.fetchone()
        
        nombre = c.execute("SELECT * FROM Pacientes WHERE Nombre = '%s'"%(self.input))
        fila2 = nombre.fetchone()
 
        if ((fila != None) or (fila2 != None)):
            if fila !=None:
                sql = "SELECT * FROM Pacientes WHERE Rut LIKE ?"
                self.res = c.execute(sql, (self.input,))
                for self.row in self.res:
                    self.Rut = self.row[0]
                    self.Nombre = self.row[1]
                    self.Edad = self.row[2]
       
               # Rut del paciente
                self.uRut = Label(self.nuevaVentana, text="Rut del paciente", font=('arial 10 bold'), fg='black')
                self.uRut.place(x=0, y=140)

                # Fecha
                self.uFecha = Label(self.nuevaVentana, text="Fecha de consulta", font=('arial 10 bold'), fg='black')
                self.uFecha.place(x=0, y=180)

                # Costo
                self.uCosto = Label(self.nuevaVentana, text="Costo de la consulta", font=('arial 10 bold'), fg='black')
                self.uCosto.place(x=0, y=220)


                # Caja de texto
                self.ent1 = Entry(self.nuevaVentana, width=30)
                self.ent1.place(x=300, y=140)
                self.ent1.insert(END, str(self.Rut))
 
                self.ent2 = Entry(self.nuevaVentana, width=30)
                self.ent2.place(x=300, y=180)
    
                self.ent3 = Entry(self.nuevaVentana, width=30)
                self.ent3.place(x=300, y=220)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # botón para ejecutar la actualización
                self.update = Button(self.nuevaVentana, text="Agregar a consulta", width=20, height=2, bg='lightblue', command=lambda: [self.add_atencion(), self.nuevaVentana.destroy()])
                self.update.place(x=400, y=380)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # boton para borrar
                self.delete = Button(self.nuevaVentana, text="Salir", width=20, height=2, bg='red', command=lambda: [despedida(), self.nuevaVentana.destroy()])
                self.delete.place(x=150, y=380)
                
            elif fila2 != None:
                sql = "SELECT * FROM Pacientes WHERE Nombre LIKE ?"
                self.res = c.execute(sql, (self.input,))
                for self.row in self.res:
                    self.Rut = self.row[0]
                    self.Nombre = self.row[1]
                    self.Edad = self.row[2]
                
                # Rut del paciente
                self.uRut = Label(self.nuevaVentana, text="Rut del paciente", font=('arial 10 bold'), fg='black')
                self.uRut.place(x=0, y=140)

                # Fecha
                self.uFecha = Label(self.nuevaVentana, text="Fecha de consulta", font=('arial 10 bold'), fg='black')
                self.uFecha.place(x=0, y=180)

                # Costo
                self.uCosto = Label(self.nuevaVentana, text="Costo de la consulta", font=('arial 10 bold'), fg='black')
                self.uCosto.place(x=0, y=220)


                # Entries for all labels============================================================
                self.ent1 = Entry(self.nuevaVentana, width=30)
                self.ent1.place(x=300, y=140)
                self.ent1.insert(END, str(self.Rut))
 
                self.ent2 = Entry(self.nuevaVentana, width=30)
                self.ent2.place(x=300, y=180)
    
                self.ent3 = Entry(self.nuevaVentana, width=30)
                self.ent3.place(x=300, y=220)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # botón para ejecutar la actualización
                self.update = Button(self.nuevaVentana, text="Agregar a consulta", width=20, height=2, bg='lightblue', command=lambda: [self.add_atencion(), self.nuevaVentana.destroy()])
                self.update.place(x=400, y=380)

                #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
                # boton de borrar
                self.delete = Button(self.nuevaVentana, text="Salir", width=20, height=2, bg='red', command=lambda: [despedida(), self.nuevaVentana.destroy()])
                self.delete.place(x=150, y=380)
        else:
            self.name = Label(self.nuevaVentana, text="Lo siento, el Rut/Nombre ingresado no se encuentra, ¿Desea Agendar una cita?",  fg='black', font=('arial 10 bold'), bg='steelblue')
            self.name.place(x=0, y=250)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="SI", width=12, height=1, bg='blue', command=lambda: [Agregar_Paciente(), self.nuevaVentana.destroy()])
            self.search.place(x=0, y=300)
            #Podríamos usar lambda para combinar múltiples comandos como se muestra a continuación.
            self.search = Button(self.nuevaVentana, text="NO", width=12, height=1, bg='red', command=lambda: [despedida(), self.nuevaVentana.destroy()])
            self.search.place(x=250, y=300)
            
    #Función para agregar un paciente de acuerdo al boton elegido
    def add_atencion(self):
        # obtenemos con "get" las entradas del usuario
        self.val1 = self.ent1.get()
        self.val2 = self.ent2.get()
        self.val3 = self.ent3.get()

        # comprobar si la entrada del usuario está vacía
        if self.val1 == '' or self.val2 == '' or self.val3 == '':
            tkinter.messagebox.showinfo("ADVERTENCIA", "Porfavor llene todas las casillas")
        else:
            #entonces si esta todo correcto, ahora agregamos a la base de datos
            sql = "INSERT INTO 'atenciones' (Rut, Fecha, Costo) VALUES(?, ?, ?)"
            c.execute(sql, (self.val1, self.val2, self.val3))
            conn.commit()
            tkinter.messagebox.showinfo("Completado", "Cita para " +str(self.val1) + " ha sido creada." )
            self.nuevaVentana.destroy() #Se completa todo y destruye esa ventana
            
#Función para el boton de "Salir" es decir, detiene el programa con "quit"
def despedida_quit():
    tkinter.messagebox.showinfo("Mensaje", "Gracias por utilizar mi programa :)")
    quit()

#Esta clase sirve para calcular los ingresos del hospital
class ingresos:
    #Función constructor que crea una ventana con sus etiquetas
    def __init__(self,nuevaVentana=None):
        self.nuevaVentana = nuevaVentana = tkinter.Toplevel(ventana)
        self.nuevaVentana.geometry("800x500")
        self.nuevaVentana.configure(background="steelblue") #Color naranja en el fondo
        self.nuevaVentana.resizable(False,False) #Sirve para que el usuario no pueda modificar la ventana, es decir que no modifique su tamaño
        self.nuevaVentana.title ("Ingresos Del Hospital")
    
        self.search = Button(self.nuevaVentana, text="Obtener Ganancia", width=18, height=2, bg='red', command=self.ganancia)
        self.search.place(x=350, y=50)
    
    #Función que suma toda las ganancias que se tiene en la base de datos
    def ganancia (self):
        sql = "SELECT sum(Costos) FROM Ganancias"
        self.res = c.execute(sql)
        for self.row in self.res:
            self.Ganancias = self.row[0]
        
    
        self.uGanancias = Label(self.nuevaVentana, text="Ganancias Obtenidas", font=('arial 10 bold'), fg='black')
        self.uGanancias.place(x=0, y=140)
    
        self.Ganancias_1 = Entry(self.nuevaVentana, width=30)
        self.Ganancias_1.place(x=300, y=140)
        self.Ganancias_1.insert(END, str(self.Ganancias))
    
#botones de tkinter          
boton_atenciones = tkinter.Button(ventana,text="Atención al cliente",fg="blue",command=Atencion_Paciente).place(x=1000,y=400, width=400, height=80)
boton_ganancias = tkinter.Button(ventana,text="Ingresos",fg="blue",command=ingresos).place(x=1000,y=600, width=400, height=80)
boton_salir = tkinter.Button(ventana,text="Salir",fg="blue",command=despedida_quit).place(x=750,y=800, width=400, height=80)

ventana.mainloop() #la ventana principal se despliega