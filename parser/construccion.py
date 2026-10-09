import ast

def leer_archivo(ruta):
    with open(ruta, encoding='utf-8') as archivo:
        codigo = archivo.read()
    return codigo

def generar_arbol(codigo):
    return ast.parse(codigo)

if __name__ == "__main__":
    codigo = leer_archivo('ejemplos/contador_suma.py')
    try:
        arbol = generar_arbol(codigo)
    except SyntaxError as e:
        print(f"Error de sintaxis en la línea {e.lineno}, columna {e.offset}: {e.msg}")
    else:
        print(ast.dump(arbol, indent=2))