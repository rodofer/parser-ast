import ast

def leer_archivo(ruta):
    with open(ruta, encoding='utf-8') as archivo:
        codigo = archivo.read()
    return codigo

def generar_arbol(codigo):
    return ast.parse(codigo)
