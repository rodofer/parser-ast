# parser-ast

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

Los errores responden `{"detail": {"tipo": "...", "mensaje": "..."}}`.
