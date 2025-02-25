const express = require('express');
const app = express();
const port = 5000;

// Middleware para analizar el cuerpo de las solicitudes en formato JSON
app.use(express.json());

// Definir una ruta para la API
app.get('/', (req, res) => {
  res.send('¡Hola, mundo! Esta es mi API.');
});

// Crear una ruta para obtener datos (GET)
app.get('/api/data', (req, res) => {
  const data = {
    mensaje: 'Este es un ejemplo de datos de la API',
    fecha: new Date(),
  };
  res.json(data);
});

// Crear una ruta para recibir datos (POST)
app.post('/api/data', (req, res) => {
  const newData = req.body;
  console.log('Datos recibidos:', newData);
  res.status(201).json({
    mensaje: 'Datos recibidos correctamente.',
    data: newData,
  });
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
