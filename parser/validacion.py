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
    ast.Add
)

class NodoNoPermitidoError(Exception):
    pass

def revisar_nodos(arbol):
    for nodo in ast.walk(arbol):
        for hijo in ast.iter_child_nodes(nodo):
            if type(hijo) not in NODOS_PERMITIDOS:
                nombre = type(hijo).__name__
                linea = getattr(hijo, 'lineno', None)
                if linea is None:
                    linea = getattr(nodo, 'lineno', None)
                raise NodoNoPermitidoError(f"El nodo {nombre} (línea {linea}) no está permitido.")

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
