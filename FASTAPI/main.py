from fastapi import FastAPI
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

@app.get('/promedio', tags=['calificacion'])
def promedio():
    return {'promedio': 9}

#endPoint Parametro Obligatorio
@app.get('/usuario/{id}', tags=['Parametro obligatorio'])
def consultaUsuario(id:int):
    #conectamosBD
    #hacemos consulta y retornamos resultset
    return{"Se encontro el usuario": id}

#endPoint parametro Opcional
@app.get('/usuariox/', tags=['Parametro opcional'])
def consultaUsuario2(id :Optional[int]=None):
    # verifica si trae algo el id y si trae algo puede proceder a realizar un accion
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id:
                return {"mensaje": "Usuario encontrado", "usuario":usuario}
        return{"mensaje":f"No se encontro el id: {id}"}
    else: 
        return{"mensaje": "No se proporciono un Id"}    

#endpoint con varios parametro opcionales
@app.get("/usuarios/", tags=["3 parámetros opcionales"])
async def consulta_usuarios(
    usuario_id: Optional[int] = None,
    nombre: Optional[str] = None,
    edad: Optional[int] = None
):
    resultados = []

    for usuario in usuarios:
        if (
            (usuario_id is None or usuario["id"] == usuario_id) and
            (nombre is None or usuario["nombre"].lower() == nombre.lower()) and
            (edad is None or usuario["edad"] == edad)
        ):
            resultados.append(usuario)

    if resultados:
        return {"usuarios_encontrados": resultados}
    else:
        return {"mensaje": "No se encontraron usuarios que coincidan con los parámetros proporcionados."}