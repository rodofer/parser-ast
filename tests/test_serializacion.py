import json

from parser.construccion import leer_archivo, generar_arbol
from parser.ejecucion import ejecutar_programa
from parser.serializacion import generar_traza


def test_traza_contador_suma_coincide_con_referencia():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    _, pasos = ejecutar_programa(arbol)
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        referencia = json.load(archivo)
    assert generar_traza(pasos) == referencia
