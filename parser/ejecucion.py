import ast
import operator

COMPARACIONES = {
    ast.Lt: operator.lt,
}

OPERACIONES = {
    ast.Add: operator.add,
}

MAX_ITERACIONES = 1000


def evaluar_expresion(nodo, memoria):
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


def ejecutar_instruccion(nodo, memoria):
    match nodo:
        case ast.Assign():
            nombre = nodo.targets[0].id
            valor = evaluar_expresion(nodo.value, memoria)
            memoria[nombre] = valor
        case ast.AugAssign():
            nombre = nodo.target.id
            actual = memoria[nombre]
            derecha = evaluar_expresion(nodo.value, memoria)
            operar = OPERACIONES[type(nodo.op)]
            memoria[nombre] = operar(actual, derecha)
        case ast.While():
            contador_iteraciones = 0
            while evaluar_expresion(nodo.test, memoria):
                if contador_iteraciones >= MAX_ITERACIONES:
                    raise RuntimeError(f"El ciclo superó {MAX_ITERACIONES} iteraciones, posible ciclo infinito")
                contador_iteraciones += 1
                for instruccion in nodo.body:
                    ejecutar_instruccion(instruccion, memoria)
        case _:
            raise NotImplementedError(f"ejecutar_instruccion no implementa el nodo {type(nodo).__name__}")


def ejecutar_programa(arbol):
    memoria = {}
    for instruccion in arbol.body:
        ejecutar_instruccion(instruccion, memoria)
    return memoria


if __name__ == "__main__":
    nodo = ast.parse('5', mode='eval').body
    print(evaluar_expresion(nodo, {}))

    nodo = ast.parse('contador', mode='eval').body
    print(evaluar_expresion(nodo, {'contador': 2}))

    nodo = ast.parse('contador < 3', mode='eval').body
    print(evaluar_expresion(nodo, {'contador': 0}))
    print(evaluar_expresion(nodo, {'contador': 3}))

    for expresion in ['contador + 1', '0 < contador < 3']:
        nodo = ast.parse(expresion, mode='eval').body
        try:
            evaluar_expresion(nodo, {'contador': 0})
        except NotImplementedError as e:
            print(f"Error esperado: {e}")

    memoria = {}
    for instruccion in ['contador = 0', 'suma = 0', 'contador += 1', 'suma += contador']:
        nodo = ast.parse(instruccion).body[0]
        ejecutar_instruccion(nodo, memoria)
        print(f"{instruccion:<20} -> {memoria}")

    from parser.construccion import leer_archivo, generar_arbol
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    print(ejecutar_programa(arbol))
