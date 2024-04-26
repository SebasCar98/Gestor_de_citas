from dotenv import load_dotenv
load_dotenv()  # Toma el camino al .env como argumento si no está en el directorio raíz

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)