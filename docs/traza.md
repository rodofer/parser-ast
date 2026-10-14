# Formato de la traza de ejecución

La traza es un documento JSON-LD con un `@context` y un `@graph`. El `@graph` es la
lista ordenada de pasos (`PasoDeEjecucion`) que el Parser genera al ejecutar el
programa. Cada paso corresponde a **una** instrucción ejecutada o a **una**
evaluación de la condición de un ciclo.

Referencia: `ejemplos/contador_suma.json`.

## Campos comunes a todos los pasos

| Campo | Tipo | Regla |
|---|---|---|
| `@type` | texto | Siempre `"PasoDeEjecucion"`. |
| `numeroPaso` | entero | Correlativo, desde 1, en orden de ejecución. |
| `linea` | entero | Línea del código fuente (desde 1) de la instrucción o del `while` cuya condición se evalúa. |
| `bloque` | texto o `null` | `null` si el paso está en el nivel superior del programa. Si está dentro de un ciclo, o evalúa su condición, es `"while_linea<N>"`, donde `<N>` es la línea del `while` más interno que lo contiene. |
| `iteracion` | entero o `null` | `null` fuera de los ciclos. Se interpreta siempre respecto del `bloque`: ver reglas abajo. |
| `instruccion` | texto | Texto de la instrucción tal como aparece en el código (`"contador += 1"`). En las evaluaciones: `"evaluar "` + la condición (`"evaluar contador < 3"`). |

### Regla de `iteracion`

- **Pasos del cuerpo del ciclo:** número de la vuelta en curso, desde 1.
- **Pasos que evalúan la condición:** número de vueltas **completadas** al momento de evaluar,
  desde 0. Así, la primera evaluación tiene `0` y la que termina el ciclo tiene el total
  de vueltas realizadas.

## Pasos que modifican la memoria (`modifica`)

Corresponden a asignaciones (`x = ...`) y asignaciones compuestas (`x += ...`).

| Campo | Regla |
|---|---|
| `modifica.@type` | `"EstadoDeMemoria"` |
| `modifica.variable` | Nombre de la variable asignada. |
| `modifica.ambito` | `"global"`. El subconjunto no admite funciones, y en Python un `while` no crea un ámbito nuevo. |
| `modifica.valorAnterior` | Valor antes de la instrucción; `null` si la variable aún no existía. |
| `modifica.valorNuevo` | Valor después de la instrucción. |

## Pasos que evalúan una condición (`evalua`)

| Campo | Regla |
|---|---|
| `resultado` | `true` o `false`: resultado de **esta** evaluación. Está en el paso, no en la condición, porque una misma condición se evalúa varias veces. |
| `evalua.@type` | `"Condicion"` |
| `evalua.@id` | `"condicion_linea<N>"`, con `<N>` la línea del `while`. Es el **mismo** en todas las evaluaciones de ese ciclo: la condición persiste a través de las iteraciones (Tabla 3.1 de la propuesta). |
| `evalua.expresion` | Texto de la condición (`"contador < 3"`). |
| `evalua.dependeDe` | Variables que se leen en la condición, sin repetir, en orden de aparición. |

Cada ciclo genera tantas evaluaciones como vueltas más una: la última, con
`resultado: false`, es la que termina el ciclo.
