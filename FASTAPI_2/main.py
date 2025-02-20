from fastapi import FastAPI, HTTPException
from typing import Optional



app = FastAPI(
    title='API de gestion de tareas',
    description='Juan Antonio Ochoa Irineo',
    version='1.0.1'
)

tareas = [
    {
        "id": 1,
        "titulo": "Estudiar para el examen",
        "descripcion": "Repasar los apuntes de TAI",
        "vencimiento": "14-02-24",
        "estado": "completada"
    },
    {
        "id": 2,
        "titulo": "Hacer ejercicio",
        "descripcion": "Correr 30 minutos",
        "vencimiento": "15-02-24",
        "estado": "no completada"
    },

     {
        "id": 3,
        "titulo": "Leer un libro",
        "descripcion": "Leer 20 páginas de un libro",
        "vencimiento": "16-02-24",
        "estado": "no completada"
    },
    {
        "id": 4,
        "titulo": "Comprar víveres",
        "descripcion": "Comprar leche, pan y huevos",
        "vencimiento": "17-02-24",
        "estado": "no completada"
    }

]


@app.get('/', tags=['inicio'])
def main():
    return {'hola FastAPI': 'JuanAntonio'}

#endpoint Consultar todas las tareas
@app.get('/tareas', tags=['Obtener todas las tareas'])
def ConsultarTodos():
    return {"Tareas Registradas": tareas}


# Endpoint para obtener una tarea por su ID
@app.get('/tareas/{tarea_id}', tags=['Obtener tarea por id'])
def obtener_tarea(tarea_id: int):
    for tarea in tareas:
        if tarea["id"] == tarea_id:
            return tarea
    raise HTTPException(status_code=404, detail="Tarea no fue encontrada")

#endpoint Para Agregar tareas
@app.post('/tareas/', tags=['Agregar una tarea'])
def AgregarTarea(tareanueva: dict):
    for tarea in tareas:
        if tarea["id"] == tareanueva.get("id"):
            #permite hacer un manejo de ecepciones (raise)
            raise HTTPException(status_code=400, detail="El id ya existe")
           
    tareas.append(tareanueva)
    return tareanueva 

