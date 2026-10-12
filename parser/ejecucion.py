import ast
import operator

COMPARACIONES = {
    ast.Lt: operator.lt
}


def evaluar(nodo, memoria):
    match nodo:
        case ast.Constant():
            return nodo.value
        case ast.Name():
            return memoria[nodo.id]
        case ast.Compare():
            if len(nodo.ops) > 1:
                raise NotImplementedError("evaluar no implementa comparaciones encadenadas")
            izquierda = evaluar(nodo.left, memoria)
            derecha = evaluar(nodo.comparators[0], memoria)
            comparar = COMPARACIONES[type(nodo.ops[0])]
            return comparar(izquierda, derecha)
        case _:
            raise NotImplementedError(f"evaluar no implementa el nodo {type(nodo).__name__}")


if __name__ == "__main__":
    nodo = ast.parse('5', mode='eval').body
    print(evaluar(nodo, {}))

    nodo = ast.parse('contador', mode='eval').body
    print(evaluar(nodo, {'contador': 2}))

    nodo = ast.parse('contador < 3', mode='eval').body
    print(evaluar(nodo, {'contador': 0}))
    print(evaluar(nodo, {'contador': 3}))

    for expresion in ['contador + 1', '0 < contador < 3']:
        nodo = ast.parse(expresion, mode='eval').body
        try:
            evaluar(nodo, {'contador': 0})
        except NotImplementedError as e:
            print(f"Error esperado: {e}")
