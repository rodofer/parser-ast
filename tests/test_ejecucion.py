import ast

from parser.construccion import leer_archivo, generar_arbol
from parser.ejecucion import MAX_ITERACIONES, ejecutar_programa, evaluar_expresion


def test_contador_suma_memoria_final():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    memoria = ejecutar_programa(arbol)
    assert memoria == {'contador': 3, 'suma': 6}


def test_comparacion_verdadera_y_falsa():
    nodo = ast.parse('contador < 3', mode='eval').body
    assert evaluar_expresion(nodo, {'contador': 2}) is True
    assert evaluar_expresion(nodo, {'contador': 3}) is False
