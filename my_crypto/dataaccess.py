#modulo para las clases de la base de datos
from config import DATABASE

import sqlite3

class DBmanager():
    def __init__(self, ruta_baseDatos):
        self.database_path = ruta_baseDatos


    def __toDict__(self, cur): 
        claves = cur.description
        filas = cur.fetchall()

        resultado = []
        for fila in filas:
            d = {}
            for tclave, valor in zip(claves, fila):
                d[tclave[0]] = valor
            resultado.append(d)
        return resultado

    def consultaMuchasSQL(self, query, parametros=[]):
        conexion = sqlite3.connect(self.database_path)
        cur = conexion.cursor()

        cur.execute(query, parametros)
        resultado = self.__toDict__(cur)
        conexion.close()
        return resultado

    def consultaUnaSQL(self, query, parametros=[]):
        resultado = self.consultaMuchasSQL(query, parametros)
        if len(resultado) > 0:
            return resultado[0]

    def modificaTablaSQL(self, query, parametros=[]):
        conexion = sqlite3.connect(self.database_path)
        cur = conexion.cursor()
        cur.execute(query, parametros)
        conexion.commit()
        conexion.close()