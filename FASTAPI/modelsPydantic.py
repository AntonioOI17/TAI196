from pydantic import BaseModel, Field, EmailStr

class modelUsuario(BaseModel):
   
    name: str = Field(..., min_length=3, max_length=15, description="Nombre debe contener solo letras y espacios")
    age: int = Field(..., gt=0, lt=130, description="No está en el rango de edad")
    email: EmailStr = Field(..., description="El correo no se ingresó correctamente", example="juan@example.com")


class modelAuth(BaseModel):
    correo:EmailStr
    passw:str = Field(...,main_length=8,strip_whitespaces=True, description="Contraseña minimo 8 caracteres")