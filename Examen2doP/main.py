from fastapi import FastAPI, HTTPException
from modelspydantic import Envio  
from typing import List

app = FastAPI(
    title='Examen 2 parcial',
    description='Juan Antonio Ochoa Irineo',
    version='1.0.1'
)

Envios = [
    {"codigo_postal": 12345, "Destino": "Calle ecualiptos", "peso": 10},
    {"codigo_postal": 12655, "Destino": "Calle ecualiptos", "peso": 10},
    {"codigo_postal": 55555, "Destino": "Calle ecualiptos", "peso": 20}
]

@app.get('/')
def main():
    return {"hola": "Juan Antonio Ochoa Irineo"}

# Endpoint para consultar un envío por el código postal
@app.get('/Envios/{codigo_postal}', response_model=Envio, tags=['Obtener envio por código postal'])
def obtener_envio(codigo_postal: int):
    for envio in Envios:
        if envio["codigo_postal"] == codigo_postal:
            return envio
    raise HTTPException(status_code=404, detail="El envío no fue encontrado")

# Endpoint para actualizar un envío por código postal
@app.put('/Envios/{codigo_postal}', response_model=Envio, tags=['Actualizar envio'])
def actualizar_envio(codigo_postal: int, envio_actualizado: Envio):
    for index, envio in enumerate(Envios):
        if envio["codigo_postal"] == codigo_postal:

            Envios[index] = envio_actualizado.dict() 
            return Envios[index]
    raise HTTPException(status_code=404, detail="El envío no fue encontrado")
