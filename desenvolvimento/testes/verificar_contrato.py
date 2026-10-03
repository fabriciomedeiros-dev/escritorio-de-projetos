"""Checagem estrutural de JSON e referências; não substitui validador OpenAPI completo."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1] / 'contratos'
api = json.loads((root / 'openapi.json').read_text())
examples = json.loads((root / 'exemplos.json').read_text())
assert api['openapi'] == '3.1.0'
ids = []

def walk(value):
    if isinstance(value, dict):
        if '$ref' in value:
            assert value['$ref'].startswith('#/')
            target = api
            for segment in value['$ref'][2:].split('/'):
                target = target[segment]
        if isinstance(value.get('required'), list):
            assert len(value['required']) == len(set(value['required']))
            if 'properties' in value:
                assert set(value['required']) <= set(value['properties'])
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)

walk(api)
for item in api['paths'].values():
    for method in ('get', 'post'):
        if method in item:
            ids.append(item[method]['operationId'])
assert len(ids) == len(set(ids))
for example in examples:
    schema = api['components']['schemas'][example['comando']]
    assert set(example) == set(schema['properties'])
    data = schema['properties']['dados']
    assert set(data['required']) <= set(example['dados']) <= set(data['properties'])
print('PASSOU: JSON, referências internas, campos requeridos, IDs de rotas e estrutura dos exemplos.')
print('Esta checagem não executa validador OpenAPI integral; verificar_servico.py valida JSON Schema e HTTP.')
