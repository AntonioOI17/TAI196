from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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
# @app.post('/auth',tags=['Autenticacion']) 
# def login(autorizado:modelAuth):
#     if autorizado.correo =='juan@example.com' and autorizado.passw == '123456789':
#         token:str = createToken(autorizado.model_dump())
#         print(token)
#         return JSONResponse(content= token)
#     else:
#         return {"Aviso ":"Usuario no encontrado"}

#response_model= List[modelUsuario] 
#dependencies=[Depends(BearerJWT())] 
#endpoint Consultar todos
@app.get('/Usuarios',tags=['Operaciones CRUD']) # list devuelve una lista del modelo 
def ConsultarTodos():
    db = Session()
    try:
        consulta = db.query(User).all()
        return JSONResponse(content= jsonable_encoder(consulta))
    except Exception as x:
        return JSONResponse(status_code=500, content= {"mensaje": "No fue posible consultar", "Excepcion": str(x)})
    finally:
        db.close()

#consiltar uno
@app.get('/Usuarios/{id}',tags=['Operaciones CRUD']) # list devuelve una lista del modelo 
def ConsultarUno(id:int):
    db = Session()
    try:
        consulta = db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code=404, content= {"mensaje": "Usuario no encontrado"})
        
        return JSONResponse(content= jsonable_encoder(consulta))
    except Exception as x:
        return JSONResponse(status_code=500, content= {"mensaje": "No fue posible consultar", "Excepcion": str(x)})
    finally:
        db.close()


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
    


#endpoint para actualizar usuario
@app.put('/Usuarios/{id}', response_model=modelUsuario ,tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modelUsuario):
    db = Session()
    try:
        consulta = db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code=404, content= {"mensaje": "Usuario no encontrado"})
        for key, value in usuario_actualizado.model_dump().items():
            setattr(consulta, key, value)
        db.commit()
        return JSONResponse(content= {"mensaje": "Usuario actualizado correctamente", "usuario": usuario_actualizado.model_dump()})
    except Exception as x:
        db.rollback()
        return JSONResponse(status_code=500, content= {"mensaje": "No se pudo actualizar", "Excepcion": str(x)})
    finally:
        db.close()


#endpoint para borrar usuario
@app.delete('/Usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    db = Session()
    try:
        consulta = db.query(User).filter(User.id == id).first()
        if not consulta:
            return JSONResponse(status_code=404, content= {"mensaje": "Usuario no encontrado"})
        db.delete(consulta)
        db.commit()
        return JSONResponse(content= {"mensaje": "Usuario eliminado correctamente"})
    except Exception as x:
        db.rollback()
        return JSONResponse(status_code=500, content= {"mensaje": "No se pudo eliminar", "Excepcion": str(x)})
    finally:
        db.close()

 #endpoint Para Agregar usuarios
""" @app.put('/usuarios/{id}', response_model=modelUsuario , tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: modelUsuario):
# for index, usr in enumerate(usuarios):
 #       if usr["id"] == id:
  #          usuarios[index]= usuario_actualizado.model_dump()
   #         return usuarios[index]
   # raise HTTPException(status_code=404, detail="El usuario no  fue encontrado")


#endpoint para borrar usuario
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    # for usuario in usuarios:
    #     if usuario["id"] == id:
    #         usuarios.remove(usuario)
    #         return {"mensaje": "Usuario eliminado correctamente"}
    # raise HTTPException(status_code=404, detail=" El Usuario no fue encontrado") """



