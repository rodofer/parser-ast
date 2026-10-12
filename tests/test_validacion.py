import pytest

from parser.construccion import leer_archivo, generar_arbol
from parser.validacion import NodoNoPermitidoError, revisar_nodos


def test_ejemplo_valido():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    revisar_nodos(arbol)  # no debe lanzar excepción


def test_operador_no_permitido():
    codigo = """contador = 0
suma -= contador
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(NodoNoPermitidoError, match='línea 2'):
        revisar_nodos(arbol)


def test_instruccion_no_permitida():
    codigo = """suma = 0
for i in range(5):
    suma += i
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(NodoNoPermitidoError, match='For'):
        revisar_nodos(arbol)


def test_while_else_no_permitido():
    codigo = """x = 0
while x < 3:
    x += 1
else:
    x = 0
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(NodoNoPermitidoError, match='while ... else'):
        revisar_nodos(arbol)


def test_constante_no_entera_no_permitida():
    codigo = """x = 0
nombre = "Ana"
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(NodoNoPermitidoError, match='constantes enteras'):
        revisar_nodos(arbol)


def test_comparacion_encadenada_no_permitida():
    codigo = """x = 0
while 0 < x < 3:
    x += 1
"""
    arbol = generar_arbol(codigo)
    with pytest.raises(NodoNoPermitidoError, match='encadenadas'):
        revisar_nodos(arbol)
