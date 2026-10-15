CONTEXTO = "https://example.org/ontologia.jsonld"
VERSION_FORMATO = "1.0"


def generar_traza(pasos: list) -> dict:
    grafo = []
    for numero, paso in enumerate(pasos, start=1):
        nodo = {
            '@type': 'PasoDeEjecucion',
            'numeroPaso': numero,
            'linea': paso['linea'],
            'bloque': paso['bloque'],
            'iteracion': paso['iteracion'],
            'instruccion': paso['instruccion'],
        }
        if paso['tipo'] == 'modifica':
            nodo['modifica'] = {
                '@type': 'EstadoDeMemoria',
                'variable': paso['variable'],
                'ambito': 'global',
                'valorAnterior': paso['valor_anterior'],
                'valorNuevo': paso['valor_nuevo'],
            }
        elif paso['tipo'] == 'evalua':
            nodo['resultado'] = paso['resultado']
            nodo['evalua'] = {
                '@type': 'Condicion',
                '@id': f"condicion_linea{paso['linea']}",
                'expresion': paso['expresion'],
                'dependeDe': paso['depende_de'],
            }
        grafo.append(nodo)
    return {
        "@context": CONTEXTO,
        "versionFormato": VERSION_FORMATO,
        "@graph": grafo,
    }
