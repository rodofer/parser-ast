import ast

def evaluar(nodo, memoria):
    match nodo:
        case ast.Constant():
            return nodo.value
        case ast.Name():
            return memoria[nodo.id]
        case _:
            raise NotImplementedError(f"evaluar no implementa el nodo {type(nodo).__name__}")

if __name__ == "__main__":
    nodo = ast.parse('5', mode='eval').body
    print(evaluar(nodo, {}))

    nodo = ast.parse('contador', mode='eval').body
    print(evaluar(nodo, {'contador': 2}))

    nodo = ast.parse('contador < 3', mode='eval').body
    try:
        evaluar(nodo, {'contador': 0})
    except NotImplementedError as e:
        print(f"Error esperado: {e}")
