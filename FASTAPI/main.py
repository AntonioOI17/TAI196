from fastapi import FastAPI
from DB.conexion import Session, engine, Base
from routers.usuarios import routerUsuario
from routers.auth import routerAuth


app = FastAPI(
    title='API de gestion de tareas',
    description='Juan Antonio Ochoa Irineo',
    version='1.0.1'
)
Base.metadata.create_all(bind=engine) #levanta las tablas en la base de datos

app.include_router(routerUsuario)#incluye el router de usuarios
app.include_router(routerAuth)#incluye el router de autenticacion



@app.get('/', tags=['inicio'])
def main():
    return {'hola FastAPI': 'JuanAntonio'}



