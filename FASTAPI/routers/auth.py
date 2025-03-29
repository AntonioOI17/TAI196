from fastapi.responses import JSONResponse
from modelsPydantic import modelUsuario, modelAuth
from tokenGen import createToken
from fastapi import APIRouter


routerAuth=APIRouter()

#endpoint autenticacion 
@routerAuth.post('/auth',tags=['Autenticacion']) 
def login(autorizado:modelAuth):
    if autorizado.correo =='juan@example.com' and autorizado.passw == '123456789':
         token:str = createToken(autorizado.model_dump())
         print(token)
         return JSONResponse(content= token)
    else:
         return {"Aviso ":"Usuario no encontrado"}