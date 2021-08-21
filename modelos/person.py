from CRUD.db import Database
class Person:
    connection = None
    def __init__(self) -> None:
        self.connection=Database()
        pass
    def get_info_owner(self,placa):
        sql = "select tbl_personas.nombre, tbl_vehiculos.placa, tbl_marcas.nombre, tbl_vehiculos.modelo, tbl_vehiculos.color from tbl_vehiculos inner join tbl_personas on tbl_vehiculos.persona_id = tbl_personas.persona_id inner join tbl_marcas on tbl_vehiculos.marca_id = tbl_marcas.marca_id where tbl_vehiculos.placa =LOWER('"+str(placa)+"')"
        print(sql);
        self.connection.cursor.execute(sql)     
        resultado = self.connection.cursor.fetchall()
        infoOwner=None
        for datos in resultado:
            infoOwner= datos
        return infoOwner
       