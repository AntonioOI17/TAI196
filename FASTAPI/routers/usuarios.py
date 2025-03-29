from fastapi import HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from modelsPydantic import modelUsuario
from middlewares import BearerJWT
from DB.conexion import Session
from models.modelsDB import User
from fastapi import APIRouter


routerUsuario=APIRouter()

#dependencies=[Depends(BearerJWT())]

@routerUsuario.get('/Usuarios',tags=['Operaciones CRUD']) # list devuelve una lista del modelo 
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
@routerUsuario.get('/Usuarios/{id}',tags=['Operaciones CRUD']) # list devuelve una lista del modelo 
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
@routerUsuario.post('/Usuarios/', response_model=modelUsuario ,tags=['Operaciones CRUD'])
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
@routerUsuario.put('/Usuarios/{id}', response_model=modelUsuario ,tags=['Operaciones CRUD'])
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
@routerUsuario.delete('/Usuarios/{id}', tags=['Operaciones CRUD'])
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
