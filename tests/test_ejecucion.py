from parser.construccion import leer_archivo, generar_arbol
from parser.ejecucion import MAX_ITERACIONES, ejecutar_programa


def test_contador_suma_memoria_final():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    memoria = ejecutar_programa(arbol)
    assert memoria == {'contador': 3, 'suma': 6}
