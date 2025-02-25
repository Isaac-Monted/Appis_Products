import database as sql

class Model:
    def __init__(self):
        """Logica de la aplicacion"""
        pass
    
    def Execute_Query (self, Query: str):
        """Ejecuta un Query de MySQL si es un `SELECT` retornara una lista"""
        cursor = sql.DataBase()
        values = cursor.execute_query(Query)
        return values