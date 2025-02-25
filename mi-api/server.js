// Cargar las variables del archivo .env
require('dotenv').config({ path: './settings.env' }); // Especifica la ruta al archivo

const express = require('express');
const mysql = require('mysql2');
const app = express();
const port = 3000;

// Middleware para manejar datos en formato JSON
app.use(express.json());

// Configuración de la conexión a la base de datos MySQL utilizando las variables de entorno
const connection = mysql.createConnection({
  host: process.env.DB_HOST,     // Obtiene la variable DB_HOST del archivo .env
  user: process.env.DB_USER,     // Obtiene la variable DB_USER del archivo .env
  password: process.env.DB_PASSWORD, // Obtiene la variable DB_PASSWORD del archivo .env
  database: process.env.DB_DATABASE, // Obtiene la variable DB_DATABASE del archivo .env
});

// Conectar a la base de datos
connection.connect((err) => {
  if (err) {
    console.error('Error al conectar a la base de datos:', err);
    return;
  }
  console.log('Conectado a la base de datos MySQL.');
});

// Ruta GET para obtener datos
app.get('/api/data', (req, res) => {
  const query = 'SELECT * FROM tabla_de_datos';  // Cambia esto por el nombre de tu tabla

  connection.query(query, (err, results) => {
    if (err) {
      console.error('Error al ejecutar la consulta:', err);
      return res.status(500).json({ error: 'Error al obtener datos.' });
    }
    res.json(results);
  });
});

// Ruta POST para insertar datos
app.post('/api/data', (req, res) => {
  const { nombre, edad } = req.body;  // Asegúrate de recibir datos en el formato correcto

  const query = 'INSERT INTO tabla_de_datos (nombre, edad) VALUES (?, ?)';
  
  connection.query(query, [nombre, edad], (err, results) => {
    if (err) {
      console.error('Error al insertar datos:', err);
      return res.status(500).json({ error: 'Error al insertar datos.' });
    }
    res.status(201).json({
      mensaje: 'Datos insertados correctamente.',
      id: results.insertId,  // ID del nuevo registro insertado
    });
  });
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});

