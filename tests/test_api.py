import json

from fastapi.testclient import TestClient

from api.main import app, MAX_LARGO_CODIGO
from parser.construccion import leer_archivo

cliente = TestClient(app)


def test_traza_contador_suma():
    codigo = leer_archivo('ejemplos/contador_suma.py')
    with open('ejemplos/contador_suma.json', encoding='utf-8') as archivo:
        referencia = json.load(archivo)
    respuesta = cliente.post('/traza', json={'codigo': codigo})
    assert respuesta.status_code == 200
    assert respuesta.json() == referencia


def test_codigo_no_permitido_devuelve_422():
    codigo = "x = 0\nfor i in x:\n    x += 1\n"
    respuesta = cliente.post('/traza', json={'codigo': codigo})
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "NodoNoPermitido"
    assert 'For' in respuesta.json()['detail']['mensaje']


def test_error_de_sintaxis_devuelve_422():
    respuesta = cliente.post('/traza', json={'codigo': 'contador 2'})
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "ErrorDeSintaxis"


def test_ciclo_sin_fin_devuelve_422():
    codigo = "x = 0\nwhile x < 1:\n    x += 0\n"
    respuesta = cliente.post('/traza', json={'codigo': codigo})
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "LimiteDeIteraciones"


def test_peticion_sin_codigo_devuelve_422():
    respuesta = cliente.post('/traza', json={})
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "SolicitudInvalida"


def test_codigo_demasiado_largo_devuelve_422():
    codigo = "x = 0\n" * (MAX_LARGO_CODIGO // 6 + 1)
    respuesta = cliente.post('/traza', json={'codigo': codigo})
    assert respuesta.status_code == 422
    assert respuesta.json()['detail']['tipo'] == "SolicitudInvalida"
