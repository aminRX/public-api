from http.client import HTTPException
import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import psycopg2
import requests

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
GITHUB_USER = os.getenv("GITHUB_USER", "myusername")
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de productos"}

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
    

class RepoCreateRequest(BaseModel):
    name: str
    description: str = ""
    private: bool = True

@app.post("/create-repo")
def create_repo(repo: RepoCreateRequest):
    if not GITHUB_TOKEN:
        raise HTTPException(status_code=500, detail="GitHub token not configured.")

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "name": repo.name,
        "description": repo.description,
        "private": repo.private,
        "auto_init": True  # Crear el repo con un README inicial
    }

    response = requests.post(f"{GITHUB_API_URL}/user/repos", headers=headers, json=payload)

    if response.status_code == 201:
        return {"status": "success", "message": f"Repository '{repo.name}' created successfully."}
    else:
        return {"status": "error", "message": response.json()}

class RepoDeleteRequest(BaseModel):
    name: str  # Nombre del repositorio a eliminar

@app.delete("/delete-repo")
def delete_repo(repo: RepoDeleteRequest):
    print("Starting delete_repo endpoint")

    if not GITHUB_TOKEN:
        print("Error: GitHub token not configured")
        raise HTTPException(status_code=500, detail="GitHub token not configured.")
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    print(f"Headers prepared: {headers}")

    url = f"{GITHUB_API_URL}/repos/{GITHUB_USER}/{repo.name}"
    print(f"Request URL: {url}")

    response = requests.delete(url, headers=headers)
    print(f"GitHub response status code: {response.status_code}")

    if response.status_code == 204:
        print(f"Repository '{repo.name}' deleted successfully.")
        return {"status": "success", "message": f"Repository '{repo.name}' deleted successfully."}
    else:
        try:
            error_message = response.json()
            print(f"Error deleting repository: {error_message}")
        except Exception as e:
            error_message = {"message": str(e)}
            print(f"Error parsing error response: {e}")
        
        return {"status": "error", "message": error_message}
