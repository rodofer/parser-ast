from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from parser.ejecucion import LimiteIteracionesError
from parser.pipeline import generar_traza
from parser.validacion import NodoNoPermitidoError

MAX_LARGO_CODIGO = 5000

app = FastAPI(title="Parser AST del Depurador Visual Interactivo", version="0.3.2")


class SolicitudTraza(BaseModel):
    codigo: str = Field(max_length=MAX_LARGO_CODIGO)


def error_422(tipo: str, mensaje: str) -> HTTPException:
    return HTTPException(status_code=422, detail={"tipo": tipo, "mensaje": mensaje})


@app.exception_handler(RequestValidationError)
async def solicitud_invalida(request: Request, exc: RequestValidationError) -> JSONResponse:
    mensaje = "; ".join(f"{e['loc'][-1]}: {e['msg']}" for e in exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": {"tipo": "SolicitudInvalida", "mensaje": mensaje}},
    )


@app.post("/traza")
def crear_traza(solicitud: SolicitudTraza) -> dict:
    try:
        return generar_traza(solicitud.codigo)
    except NodoNoPermitidoError as e:
        raise error_422("NodoNoPermitido", str(e)) from e
    except SyntaxError as e:
        mensaje = f"Error de sintaxis en la línea {e.lineno}, columna {e.offset}: {e.msg}"
        raise error_422("ErrorDeSintaxis", mensaje) from e
    except LimiteIteracionesError as e:
        raise error_422("LimiteDeIteraciones", str(e)) from e
