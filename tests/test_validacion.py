from parser.construccion import leer_archivo, generar_arbol
from parser.validacion import revisar_nodos

def test_ejemplo_valido():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    revisar_nodos(arbol)
    # no debe lanzar excepción
