import json

import pytest

from parser.construccion import leer_archivo
from parser.pipeline import generar_traza
from parser.validacion import NodoNoPermitidoError


def test_pipeline_contador_suma_produce_referencia():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        referencia = json.load(archivo)
    assert generar_traza(codigo) == referencia


def test_pipeline_rechaza_codigo_no_permitido():
    codigo = """x = 0
for i in x:
    x += 1
"""
    with pytest.raises(NodoNoPermitidoError, match='For'):
        generar_traza(codigo)


def test_pipeline_propaga_error_de_sintaxis():
    with pytest.raises(SyntaxError):
        generar_traza('contador 2')
