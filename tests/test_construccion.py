import ast
import pytest
from parser.construccion import leer_archivo, generar_arbol

def test_generacion_arbol():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    arbol = generar_arbol(codigo)
    assert isinstance(arbol, ast.Module)

def test_error_sintaxis_lanza_syntaxerror():
    codigo = "contador 2"
    with pytest.raises(SyntaxError):
        generar_arbol(codigo)