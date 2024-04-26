# Gestor de citas medicas

Este proyecto es un sistema de gestión de citas médicas desarrollado usando Flask, 
un micro-framework de Python. El sistema permite a los usuarios gestionar doctores, pacientes, 
citas y tipos de citas médicas, facilitando la interacción con la base de datos a través de una API RESTful.

## Instalación

### Requisitos Previos

- Python 3.8+
- pip
- virtualenv (opcional)

### Configuración del Entorno

1. Instalar `virtualenv` si aún no está instalado:

   ```bash
   pip install virtualenv
   ```
2. Crear y activar un entorno virtual:
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate

   # En macOS y Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instrucciones paso a paso de la instalacion despues del entorno.

   ```bash
      git clone https://github.com/SebasCar98/Gestor_de_citas.git
      cd Gestor_de_citas
      pip install -r requirements.txt
   ```

### Configuración de la Base de Datos y Migraciones

Después de instalar las dependencias y antes de ejecutar la aplicación, asegúrate de configurar y preparar la base de datos:

1. **Inicializa la base de datos:**
   ```bash
   flask db init
   ```
4. **Crear y aplicar migraciones:**
   ```bash
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
### Ejecutar la Aplicación

Inicia el servidor de desarrollo de Flask para correr la aplicación:

   ```bash
   flask run
   ```

## Stack Tecnologico

- Flask
- SQLAlchemy
- SQLite
- Flask-RESTful.
- Flask-Migrate

El sistema está diseñado para ser simple pero funcional, 
proporcionando una base robusta para cualquier expansión futura o 
personalización necesaria para adaptarse a diferentes requisitos o entornos de trabajo médicos.

## Evidencia de Funcionamiento

A continuación, se muestran algunas capturas de pantalla que demuestran el funcionamiento del sistema 
a través de Postman.



### Estructura de Postman para las pruebas.

![](images/menu_postman.png)


### Solicitud de Creación de Doctor

![](images/image1doc_create.png)

### Solicitud get de Doctores

![](images/image3doc_get.png)

### Solicitud de Creación de Paciente

![](images/image5Paciente_post.png)

### Solicitud de get de Pacientes Creados.

![](images/image4paciente_get.png)

### Solicitud de Creación de una cita

![](images/image7Cita_post.png)

### Solicitud de get de Citas Creadas.

![](images/image6Cita_get.png)




