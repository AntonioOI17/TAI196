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
        "titulo": "Estudiar para el examen de matemáticas",
        "descripcion": "Repasar los apuntes de álgebra y cálculo",
        "vencimiento": "14-02-24",
        "estado": "completada"
    },
    {
        "id": 2,
        "titulo": "Hacer ejercicio en el gimnasio",
        "descripcion": "Hacer 30 minutos de cardio y 20 minutos de pesas",
        "vencimiento": "15-02-24",
        "estado": "no completada"
    },
    {
        "id": 3,
        "titulo": "Leer un libro de ciencia ficción",
        "descripcion": "Leer 20 páginas de 'Dune'",
        "vencimiento": "16-02-24",
        "estado": "no completada"
    },
    {
        "id": 4,
        "titulo": "Comprar víveres para la semana",
        "descripcion": "Comprar leche, pan, huevos y verduras",
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

#Endpoint para actualizar tareas
@app.put('/tareas/{id}', tags=['Actualizar tarea'])
def actualizar_tarea(id: int, tarea_actualizada: dict):
    for tarea in tareas:
        if tarea["id"] == id:
            tarea.update(tarea_actualizada)
            return tarea
    raise HTTPException(status_code=404, detail="La tarea no  fue encontrada")

#endpoint para borrar una tarea
@app.delete('/tareas/{id}', tags=['Eliminar tarea'])
def eliminar_tarea(id: int):
    for tarea in tareas:
        if tarea["id"] == id:
            tareas.remove(tarea)
            return {"mensaje": "La tarea fue eliminada correctamente"}
    raise HTTPException(status_code=404, detail=" La tarea no fue encontrada")