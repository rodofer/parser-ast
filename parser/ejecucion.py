import ast
import operator

COMPARACIONES = {
    ast.Lt: operator.lt,
}

OPERACIONES = {
    ast.Add: operator.add,
}

MAX_ITERACIONES = 1000


class LimiteIteracionesError(RuntimeError):
    pass


def evaluar_expresion(nodo: ast.expr, memoria: dict):
    match nodo:
        case ast.Constant():
            return nodo.value
        case ast.Name():
            return memoria[nodo.id]
        case ast.Compare():
            if len(nodo.ops) > 1:
                raise NotImplementedError("evaluar_expresion no implementa comparaciones encadenadas")
            izquierda = evaluar_expresion(nodo.left, memoria)
            derecha = evaluar_expresion(nodo.comparators[0], memoria)
            comparar = COMPARACIONES[type(nodo.ops[0])]
            return comparar(izquierda, derecha)
        case _:
            raise NotImplementedError(f"evaluar_expresion no implementa el nodo {type(nodo).__name__}")


def variables_leidas(expresion: ast.expr):
    nombres = [n for n in ast.walk(expresion) if isinstance(n, ast.Name)]
    nombres.sort(key=lambda n: (n.lineno, n.col_offset))
    return list(dict.fromkeys(n.id for n in nombres))


def ejecutar_instruccion(nodo: ast.stmt, memoria: dict, pasos: list,
                         bloque: str | None = None, iteracion: int | None = None):
    match nodo:
        case ast.Assign():
            nombre = nodo.targets[0].id
            anterior = memoria.get(nombre)
            memoria[nombre] = evaluar_expresion(nodo.value, memoria)
            pasos.append({
                'tipo': 'modifica',
                'linea': nodo.lineno,
                'bloque': bloque,
                'iteracion': iteracion,
                'instruccion': ast.unparse(nodo),
                'variable': nombre,
                'valor_anterior': anterior,
                'valor_nuevo': memoria[nombre],
            })
        case ast.AugAssign():
            nombre = nodo.target.id
            anterior = memoria[nombre]
            derecha = evaluar_expresion(nodo.value, memoria)
            operar = OPERACIONES[type(nodo.op)]
            memoria[nombre] = operar(anterior, derecha)
            pasos.append({
                'tipo': 'modifica',
                'linea': nodo.lineno,
                'bloque': bloque,
                'iteracion': iteracion,
                'instruccion': ast.unparse(nodo),
                'variable': nombre,
                'valor_anterior': anterior,
                'valor_nuevo': memoria[nombre],
            })
        case ast.While():
            bloque_ciclo = f"while_linea{nodo.lineno}"
            completadas = 0
            while True:
                resultado = evaluar_expresion(nodo.test, memoria)
                pasos.append({
                    'tipo': 'evalua',
                    'linea': nodo.lineno,
                    'bloque': bloque_ciclo,
                    'iteracion': completadas,
                    'instruccion': f"evaluar {ast.unparse(nodo.test)}",
                    'expresion': ast.unparse(nodo.test),
                    'depende_de': variables_leidas(nodo.test),
                    'resultado': resultado,
                })
                if not resultado:
                    break
                if completadas >= MAX_ITERACIONES:
                    raise LimiteIteracionesError(f"El ciclo superó {MAX_ITERACIONES} iteraciones, posible ciclo infinito")
                completadas += 1
                for instruccion in nodo.body:
                    ejecutar_instruccion(instruccion, memoria, pasos, bloque_ciclo, completadas)
        case _:
            raise NotImplementedError(f"ejecutar_instruccion no implementa el nodo {type(nodo).__name__}")


def ejecutar_programa(arbol: ast.Module):
    memoria = {}
    pasos = []
    for instruccion in arbol.body:
        ejecutar_instruccion(instruccion, memoria, pasos)
    return memoria, pasos
