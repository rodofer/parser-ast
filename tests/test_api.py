import json

from fastapi.testclient import TestClient

from api.main import app
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
