import ast
import operator

COMPARACIONES = {
    ast.Lt: operator.lt
}

OPERACIONES = {
    ast.Add: operator.add,
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


def ejecutar(nodo, memoria):
    match nodo:
        case ast.Assign():
            nombre = nodo.targets[0].id
            valor = evaluar(nodo.value, memoria)
            memoria[nombre] = valor
        case ast.AugAssign():
            nombre = nodo.target.id
            actual = memoria[nombre]
            derecha = evaluar(nodo.value, memoria)
            operar = OPERACIONES[type(nodo.op)]
            memoria[nombre] = operar(actual, derecha)
        case _:
            raise NotImplementedError(f"ejecutar no implementa en nodo {type(nodo).__name__}")


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

    memoria = {}
    for instruccion in ['contador = 0', 'suma = 0', 'contador += 1', 'suma += contador']:
        nodo = ast.parse(instruccion).body[0]
        ejecutar(nodo, memoria)
        print(f"{instruccion:<20} -> {memoria}")
