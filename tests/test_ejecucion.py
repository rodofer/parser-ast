import ast

import pytest

from parser.construccion import leer_archivo, generar_arbol
from parser.ejecucion import MAX_ITERACIONES, ejecutar_programa, evaluar_expresion, ejecutar_instruccion


def test_contador_suma_memoria_final():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    memoria = ejecutar_programa(arbol)
    assert memoria == {'contador': 3, 'suma': 6}


def test_comparacion_verdadera_y_falsa():
    nodo = ast.parse('contador < 3', mode='eval').body
    assert evaluar_expresion(nodo, {'contador': 2}) is True
    assert evaluar_expresion(nodo, {'contador': 3}) is False


def test_asignacion_compuesta_usa_valor_anterior():
    memoria = {'contador': 4}
    nodo = ast.parse('contador += 1').body[0]
    ejecutar_instruccion(nodo, memoria)
    assert memoria == {'contador': 5}


def test_ciclo_en_limite_termina():
    codigo = f"""x = 0
while x < {MAX_ITERACIONES}:
    x += 1
"""
    memoria = ejecutar_programa(generar_arbol(codigo))
    assert memoria == {'x': MAX_ITERACIONES}


def test_ciclo_supera_limite_se_detiene():
    codigo = f"""x = 0
while x < {MAX_ITERACIONES + 1}:
    x += 1
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(RuntimeError, match='posible ciclo infinito'):
        ejecutar_programa(arbol)
