from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(
    title='Mi primer API 196',
    description='Juan Antonio Ochoa Irineo',
    version='1.0.1'
)

usuarios=[
    {"id":1, "nombre":"Juan", "edad":21},
    {"id":2, "nombre":"Ivan", "edad":22},
    {"id":3, "nombre":"Jose", "edad":13},
    {"id":4, "nombre":"Alberto", "edad":15}
]

@app.get('/', tags=['inicio'])
def main():
    return {'hola FastAPI': 'JuanAntonio'}

#endpoint Consultar todos
@app.get('/Usuarios', tags=['Operaciones CRUD'])
def ConsultarTodos():
    return{"Usuarios Registrados": usuarios}

#endpoint Para Agregar usuarios
@app.post('/Usuarios/', tags=['Operaciones CRUD'])
def AgregarUsuario(usuarionuevo: dict):
    for usr in usuarios:
        if usr["id"] == usuarionuevo.get("id"):
            #permite hacer un manejo de ecepciones (raise)
            raise HTTPException(status_code=400, detail="El id ya existe")

    usuarios.append(usuarionuevo)
    return usuarionuevo  

 #endpoint Para Agregar usuarios
@app.put('/usuarios/{id}', tags=['Operaciones CRUD'])
def actualizar_usuario(id: int, usuario_actualizado: dict):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuario.update(usuario_actualizado)
            return usuario
    raise HTTPException(status_code=404, detail="El usuario no  fue encontrado")


#endpoint para borrar usuario
@app.delete('/usuarios/{id}', tags=['Operaciones CRUD'])
def eliminar_usuario(id: int):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {"mensaje": "Usuario eliminado correctamente"}
    raise HTTPException(status_code=404, detail=" El Usuario no fue encontrado")
