import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://react.local:30807"],
 # ⚠️ Para desarrollo. En producción define el dominio exacto.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mydatabase")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword")

# Modelo de producto
class Product(BaseModel):
    id: int
    name: str
    price: float

# Lista de productos de ejemplo
products = [
    {"id": 1, "name": "Laptop", "price": 999.99},
    {"id": 2, "name": "Smartphone", "price": 499.99},
    {"id": 3, "name": "Headphones", "price": 99.99},
    {"id": 4, "name": "Tablet", "price": 299.99},
]

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de productos"}

@app.get("/products", response_model=List[Product])
def get_products():
    return products

@app.get("/db-check")
def db_check():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=5
        )
        conn.close()
        return {"status": "success", "message": "Connected to the database!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
