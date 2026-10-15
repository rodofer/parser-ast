from parser.construccion import generar_arbol
from parser.validacion import revisar_nodos
from parser.ejecucion import ejecutar_programa
from parser.serializacion import serializar_traza


def generar_traza(codigo: str) -> dict:
    arbol = generar_arbol(codigo)
    revisar_nodos(arbol)
    _, pasos = ejecutar_programa(arbol)
    return serializar_traza(pasos)
