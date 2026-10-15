from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from parser.pipeline import generar_traza
from parser.validacion import NodoNoPermitidoError

app = FastAPI(title="Parser AST del Depurador Visual Interactivo")


class SolicitudTraza(BaseModel):
    codigo: str


def error_422(tipo: str, mensaje: str) -> HTTPException:
    return HTTPException(status_code=422, detail={"tipo": tipo, "mensaje": mensaje})


@app.post("/traza")
def crear_traza(solicitud: SolicitudTraza) -> dict:
    try:
        return generar_traza(solicitud.codigo)
    except NodoNoPermitidoError as e:
        raise error_422("NodoNoPermitido", str(e)) from e
