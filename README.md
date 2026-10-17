# parser-ast

Servicio que genera la traza de ejecución (JSON-LD) del Depurador Visual Interactivo a partir de código Python.

## Instalación

Requiere Python 3.10 o superior

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## Integración

- El formato de la traza está especificado en `docs/traza.md`.
- Integrar solo vía API; no importar módulos internos.
- Reportar dudas o problemas como issues.

## API

Levantar el servidor:

```bash
uvicorn api.main:app --reload
```

Documentación interactiva: http://127.0.0.1:8000/docs

### POST /traza

Solicitud: `{"codigo": "<código Python>"}`

| situación | HTTP | `detail.tipo` |
|---|---|---|
| código válido | 200 | (traza JSON-LD, ver `docs/traza.md`) |
| error de sintaxis | 422 | `ErrorDeSintaxis` |
| construcción no soportada | 422 | `NodoNoPermitido` |
| ciclo supera 1000 iteraciones | 422 | `LimiteDeIteraciones` |
| solicitud mal formada (falta `codigo` o supera 5000 caracteres) | 422 | `SolicitudInvalida` |

Los errores responden `{"detail": {"tipo": "...", "mensaje": "..."}}`.
