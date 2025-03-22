from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from middlewares import BearerJWT
from DB.conexion import Session, engine, Base
from models.modelsDB import User


app = FastAPI(
    title='API de gestion de tareas',
    description='Juan Antonio Ochoa Irineo',
    version='1.0.1'
)
Base.metadata.create_all(bind=engine) #levanta las tablas en la base de datos




usuarios=[
    {"id":1, "nombre":"Juan", "edad":21, "correo":"juan@axample.com"},
    {"id":2, "nombre":"Ivan", "edad":22, "correo":"Ivan@axample.com"},
    {"id":3, "nombre":"Jose", "edad":13, "correo":"jose@axample.com"},
    {"id":4, "nombre":"Alberto", "edad":15, "correo":"albert@axample.com"}
]

@app.get('/', tags=['inicio'])
def main():
    return {'hola FastAPI': 'JuanAntonio'}

#endpoint autenticacion 
@app.post('/auth',tags=['Autenticacion']) 
def login(autorizado:modelAuth):
    if autorizado.correo =='juan@example.com' and autorizado.passw == '123456789':
        token:str = createToken(autorizado.model_dump())
        print(token)
        return JSONResponse(content= token)
    else:
        return {"Aviso ":"Usuario no encontrado"}
    

#endpoint Consultar todos
@app.get('/Usuarios', dependencies=[Depends(BearerJWT())] , response_model= List[modelUsuario] ,tags=['Operaciones CRUD']) # list devuelve una lista del modelo 
def ConsultarTodos():
    return usuarios

#endpoint Para Agregar usuarios
@app.post('/Usuarios/', response_model=modelUsuario ,tags=['Operaciones CRUD'])
def agregar_usuario(usuario: modelUsuario):
    db = Session()
    try:
        db.add(User(**usuario.model_dump()))
        db.commit()
        return JSONResponse(status_code=201, content= {"mensaje": "Usuario guardado", "usuario": usuario.model_dump()})
    except Exception as e:
        db.rollback()
        return JSONResponse(status_code=500, content= {"mensaje": "Usuario no se guardado", "Excepcion": str(e)})
    
    finally:    
        db.close()
    

    

 #endpoint Para Agregar usuarios
@app.put('/usuarios/{id}', response_model=modelUsuario , tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modelUsuario):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index]= usuario_actualizado.model_dump()
            return usuarios[index]
    raise HTTPException(status_code=404, detail="El usuario no  fue encontrado")


#endpoint para borrar usuario
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail=" El Usuario no fue encontrado")
