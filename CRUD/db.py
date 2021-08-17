import pymysql

class Database:
    def __init__(self):
        #Se establecen los parámetros de la conexión
        self.conn = pymysql.connect(
            host="173.249.21.6",
            user="movil2",
            passwd="carwash2021",
            db="proyectofinal"
        )
        self.cursor = self.conn.cursor()

    def InsertItems(self, element):
        #Declaramos la sentencia SQL para hacer la inserción de datos a la tabla
        sql = "insert into tbl_personas(nombre, identidad, direccion, telefono, tipo_persona_id) values('{}','{}','{}','{}','{}')".format(element[0],element[1],element[2],element[3],element[4])
        #Ejecutamos la sentencia
        self.cursor.execute(sql)
        #Guardamos cambios
        self.conn.commit()

    def ReturnOneItem(self, ref):
        #Declaramos la sentencia SQL para obtener un dato específico de la tabla
        sql = "select * from tbl_personas where nombre = '{}'".format(ref)
        #Ejecutamos la sentencia
        self.cursor.execute(sql)
        #Retornamos el dato solicitado
        return self.cursor.fetchone()

    def returnAllElements(self):
        sql = "select * from tbl_personas"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def Delete(self, ref):
        sql = "delete from tbl_personas where nombre = '{}'".format(ref)
        self.cursor.execute(sql)
        self.conn.commit()

    def UpdateItem(self, element, ref):
        #element contiene los valores y ref es el nombre del elemento que queremos cambiar‎‎
        sql = "update tbl_personas set persona_id = '{}', nombre = '{}', identidad = '{}', direccion = '{}', telefono = '{}', tipo_persona_id = '{}' where nombre = '{}'".format(element[0], element[1], element[2], element[3], element[4], element[5], element[6], ref)
        #Ejecutamos la sentencia
        self.cursor.execute(sql)
        #Guardamos cambios
        self.conn.commit()