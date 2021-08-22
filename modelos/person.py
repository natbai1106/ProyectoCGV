from CRUD.db import Database
class Person:
    connection = None
    def __init__(self) -> None:
        self.connection=Database()
        pass
    def get_info_owner(self,placa):
        sql="select tbl_personas.nombre, tbl_vehiculos.placa, tbl_marcas.nombre, tbl_vehiculos.modelo, tbl_vehiculos.color, tbl_vehiculos.vehiculo_id,(select precio from tbl_precio_peaje where num_eje = tbl_vehiculos.num_ejes) as Precio_Peaje,tbl_personas.fecha_max_pago, tbl_vehiculos.num_ejes from tbl_vehiculos inner join tbl_personas on tbl_vehiculos.persona_id = tbl_personas.persona_id inner join tbl_marcas on tbl_vehiculos.marca_id = tbl_marcas.marca_id where tbl_vehiculos.placa =LOWER('"+str(placa)+"')"
        #print(sql)
        self.connection.cursor.execute(sql)     
        resultado = self.connection.cursor.fetchall()
        infoOwner=None
        for datos in resultado:
            infoOwner=datos
        return infoOwner

    def get_reports_vehicle(self,idVehiculo):
        sql = "select tbl_tipo_reporte.reportePor as Reporte_Por from tbl_tipo_reporte inner join tbl_vehiculos_con_reportes on tbl_tipo_reporte.tipo_reporte_id = tbl_vehiculos_con_reportes.tipo_reporte_id where tbl_vehiculos_con_reportes.vehiculo_id='"+idVehiculo+"'"
        self.connection.cursor.execute(sql)     
        resultado = self.connection.cursor.fetchall()
        reports=[]
        for datos in resultado:
            reports.append(datos)
        return reports
    def InsertItems(self, element):
            #Declaramos la sentencia SQL para hacer la inserción de datos a la tabla
            sql = "INSERT INTO tbl_vehiculos_con_reportes (vehiculo_id, tipo_reporte_id) VALUES({}, {}) ON DUPLICATE KEY UPDATE vehiculo_id={}, tipo_reporte_id={}".format(element[0],element[1],element[0],element[1])
            #Ejecutamos la sentencia
            print(sql)
            self.connection.cursor.execute(sql)
            #Guardamos cambios
            self.connection.conn.commit()
    