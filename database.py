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
                database=config('DB_NAME'),
                autocommit=False
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
            
            
    def execute_multiple_queries(self, queries: list, params_list: list = None):
        """Ejecuta múltiples consultas SQL de manera secuencial en una transacción.

        Args:
            queries (list): Lista de consultas SQL a ejecutar.
            params_list (list): Lista de tuplas de parámetros correspondientes a cada consulta.

        Returns:
            bool: True si todas las consultas se ejecutaron correctamente, False en caso de error.
        """
        if len(queries) != len(params_list) if params_list else len(queries):
            print("Error: La cantidad de consultas no coincide con la cantidad de parámetros proporcionados.")
            return False
        
        try:
            # Deshabilitar el autoguardado
            if self.conn.autocommit:
                self.conn.autocommit = False
            
            print(f"Estado de la conexion inicial: {self.conn.is_connected()}")
            # Iniciar la transacción
            self.conn.start_transaction()

            # Ejecutar cada consulta
            for i, query in enumerate(queries):
                # Verificación de la conexión antes de cada consulta
                if not self.conn.is_connected():
                    print(f"Conexión perdida antes de ejecutar la consulta {i + 1}. Intentando reconectar.")
                    self.conn.ping(reconnect=True)  # Intenta reconectar si la conexión está perdida
                    if not self.conn.is_connected():
                        print("No se pudo reconectar con la base de datos.")
                        return False
                
                print(f"Estado de la conexion en el inicio del ciclo: {self.conn.is_connected()}")
                params = params_list[i] if params_list else None
                try:
                    print(query, params)
                    # Ejecutar la consulta
                    if params == None:
                        self.execute_query(query) # Llamar a execute_query para cada consulta
                    else:
                        self.execute_query(query, params)  # Llamar a execute_query para cada consulta

                    # Si la consulta es de tipo SELECT, obtenemos los resultados
                    if query.strip().upper().startswith('SELECT'):
                        result = self.cursor.fetchall()
                        return result  # Devuelve las filas seleccionadas
                    print(f"Estado de la conexion en el fin del ciclo: {self.conn.is_connected()}")
                    
                    if not self.conn.is_connected():
                        print(f"Conexión perdida antes de ejecutar la consulta {i + 1}. Intentando reconectar.")
                        self.conn.ping(reconnect=True)  # Intenta reconectar si la conexión está perdida
                        if not self.conn.is_connected():
                            print("No se pudo reconectar con la base de datos.")
                            return False
                except Exception as e:
                    print(f"Error en la consulta {i + 1}: {e}")
                    self.conn.rollback()  # Revertir en caso de error en la consulta
                    return False

            # Confirmar la transacción si todas las consultas son exitosas
            self.conn.commit()
            return True

        except Exception as e:
            print(f"Error general al ejecutar múltiples consultas: {e}")
            self.conn.rollback()  # Revertir en caso de error en la transacción completa
            return False

        finally:
            self.cerrar()  # Cerrar la conexión y el cursor

