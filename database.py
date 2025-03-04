import mysql.connector as mysql
from dotenv import load_dotenv
from decouple import config
from pathlib import Path
import flet as ft

class DataBase:
    def __init__(self):
        env_path = Path(__file__).resolve().parent / 'settings.env'
        load_dotenv(env_path)
        try:
            self.conn = mysql.connect(
                host=config('DB_HOST'),
                port=config('DB_PORT', default=3306, cast=int),
                user=config('DB_USER'),
                password=config('DB_PASSWORD'),
                database=config('DB_NAME')
            )
            
            self.cursor = self.conn.cursor()
        except Exception as err:
            print(err)
            
    def cerrar(self):
        """Cerrar la coneccion con la base de datos"""
        self.conn.close()
        
    def execute_query(self, query: str, params: tuple = None):
        """Ejecuta consultas SQL en una base de datos MySQL.

        Esta función permite ejecutar consultas de tipo `INSERT`, `SELECT`, `UPDATE` o `DELETE`. Se recomienda usar parámetros para evitar problemas de inyección SQL.

        Args:
            query (str): Consulta SQL a ejecutar.
            params (tuple): Parámetros a insertar en la consulta (si es necesario). Default es `None`.

        Returns:
            list: Si la consulta es un `SELECT`, devuelve una lista de tuplas.
            int: En el caso de consultas `INSERT`, `UPDATE` o `DELETE`, devuelve el número de filas afectadas.
            None: Si ocurre un error durante la ejecución.
        """
        try:
            # Ejecutar la consulta con parámetros, si los hay
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)

            # Si la consulta es de tipo SELECT, obtenemos los resultados
            if query.strip().upper().startswith('SELECT'):
                result = self.cursor.fetchall()
                return result  # Devuelve las filas seleccionadas

            # Si es una consulta de tipo INSERT, UPDATE o DELETE, hacer commit y devolver el número de filas afectadas
            self.conn.commit()
            return self.cursor.rowcount  # Número de filas afectadas por la consulta

        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

        finally:
            self.cerrar()  # Cerrar la conexión y el cursor
            