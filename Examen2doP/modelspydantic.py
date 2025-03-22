from pydantic import BaseModel, Field

class Envio(BaseModel):
    codigo_postal: int = Field(...,gt=0, description="codigo postal")
    Destino: str = Field(...,min_length=3, max_length=30, description="Destino")
    peso: float = Field(...,gt=0, description="peso del envio")