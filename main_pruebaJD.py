from fastapi import FastAPI, Query

app = FastAPI()

# http://127.0.0.1:8000  # ruta del sevidor de uvicorn

@app.get("/")                   # funcion que se ejecuta en el inicio
def index():
    return {"message" : "Hola Mundo"}

@app.get("/libros/{id}")            # el /libros es para crear ruta de libro, parametros variables van entre llaves
def mostrar_libro(id : int):              # se crea una funcion que retorna el id ingresado, especificando el tipo de dato a ingresar
    return {"data": id}