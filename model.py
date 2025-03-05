import PIL.Image
import database as sql
import base64
import io
import PIL

class Model:
    def __init__(self):
        """Logica de la aplicacion"""
        pass
    
    def Execute_Query (self, Query: str, params: tuple = None):
        """Ejecuta un Query de MySQL si es un `SELECT` retornara una lista"""
        cursor = sql.DataBase()
        values = cursor.execute_query(Query, params)
        return values
    
    def Encode_Imagen(self, Ruta: str):
        """Convertir imagen a binario"""
        
        with open(Ruta, "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()) .decode("utf-8")
            
        return image_base64
        
    def Decode_imagen(self, Imagen_Binario: str):
        """Convertir binario a imagen"""
        
        image_data = base64.b64decode(Imagen_Binario)
        image = PIL.Image.open(io.BytesIO(image_data))
        
        return image
        
    def UFT_8_Decode_image(self, Blob: bytes) -> str:
        Imagen = Blob.decode('utf-8')
        
        return Imagen
        
        