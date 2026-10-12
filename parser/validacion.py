import ast

NODOS_PERMITIDOS = (
    ast.Module,
    ast.Assign,
    ast.Name,
    ast.Store,
    ast.Constant,
    ast.While,
    ast.Compare,
    ast.Load,
    ast.Lt,
    ast.AugAssign,
    ast.Add,
)


class NodoNoPermitidoError(Exception):
    pass


def revisar_reglas(nodo):
    match nodo:
        case ast.While() if nodo.orelse:
            return "while ... else no está permitido"
        case ast.Constant() if type(nodo.value) is not int:
            return f"solo se permiten constantes enteras (se encontró {nodo.value!r})"
        case ast.Compare() if len(nodo.ops) > 1:
            return "las comparaciones encadenadas no están permitidas"
    return None


def revisar_nodos(arbol):
    for nodo in ast.walk(arbol):
        for hijo in ast.iter_child_nodes(nodo):
            linea = getattr(hijo, 'lineno', None)
            if linea is None:
                linea = getattr(nodo, 'lineno', None)
            if type(hijo) not in NODOS_PERMITIDOS:
                nombre = type(hijo).__name__
                raise NodoNoPermitidoError(f"El nodo {nombre} (línea {linea}) no está permitido.")
            problema = revisar_reglas(hijo)
            if problema:
                raise NodoNoPermitidoError(f"{problema} (línea {linea}).")


if __name__ == "__main__":
    from parser.construccion import leer_archivo, generar_arbol
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    try:
        revisar_nodos(arbol)
    except NodoNoPermitidoError as e:
        print(f"Error: {e}")
    else:
        print("Código válido.")
