# API de Productos Simple

Una API simple construida con FastAPI que devuelve una lista de productos.

## Endpoints

- GET `/`: Mensaje de bienvenida
- GET `/products`: Lista de productos

## Ejecutar localmente

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar el servidor:
```bash
uvicorn main:app --reload
```

## Ejecutar con Docker

1. Construir la imagen:
```bash
docker build -t productos-api .
```

2. Ejecutar el contenedor:
```bash
docker run -p 8000:8000 productos-api
```

La API estará disponible en `http://localhost:8000`

Documentación de la API disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 