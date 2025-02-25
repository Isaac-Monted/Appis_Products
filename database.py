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
        
    def execute_query(self, query: str):
        """Ejecuta consultas SQL en una base de datos MySQL.

        Esta función permite ejecutar consultas de tipo `INSERT`, `SELECT`, `UPDATE` o `DELETE`. Es importante asegurarse de que la consulta esté correctamente escrita, ya que, de lo contrario, se generará un error.

        Args:
            query (str): Consulta SQL a ejecutar. Puede ser una instrucción para insertar, seleccionar, actualizar o eliminar datos en la base de datos.

        Returns:
            list: En caso de una consulta `SELECT`, devuelve una lista de tuplas, donde cada tupla representa una fila de resultados con sus respectivos valores:
            ```
                [
                    (dato1, valor1),
                    (dato2, valor2),
                    ...
                ]
            ```
            En caso de consultas `INSERT`, `UPDATE` o `DELETE`, la función no retorna ningún valor.

        Examples:
            -"SELECT * FROM tabla;"
            
            -"INSERT INTO tabla (columna1, columna2) VALUES (valor1, valor2);"
        """
        try:
            self.cursor.execute(query)

            # Si la consulta es de tipo SELECT, obtenemos los resultados
            if query.strip().upper().startswith('SELECT'):
                count = self.cursor.fetchall()
                return count

            # Si es una consulta de tipo INSERT, UPDATE o DELETE, ejecutamos y retornamos el número de filas afectadas
            self.conn.commit()
            return self.cursor.rowcount  # Número de filas afectadas

        except Exception as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None
        finally:
            self.cerrar()
            
        