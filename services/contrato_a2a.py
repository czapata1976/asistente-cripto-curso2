from typing import Literal

from pydantic import BaseModel, Field


class FragmentoRecuperado(BaseModel):
    fuente: str
    extracto: str
    similitud: float


class RespuestaEspecialista(BaseModel):
    respuesta: str = Field(min_length=1)
    fuentes: list[str] = Field(default_factory=list)
    fragmentos: list[FragmentoRecuperado] = Field(default_factory=list)
    estado: Literal["respondido", "sin_evidencia", "no_disponible"]
