import pytest

from parser.construccion import leer_archivo, generar_arbol
from parser.validacion import NodoNoPermitidoError, revisar_nodos

def test_ejemplo_valido():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    revisar_nodos(arbol) # no debe lanzar excepción

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
