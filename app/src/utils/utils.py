
import json
from typing     import  Any
from datetime   import date, timedelta


class Utils:


    def _flatten_json(self, data):
        result = {}
        def flatten(value, parent_key=''):
            if isinstance(value, dict):
                for k, v in value.items():
                    new_key = f"{parent_key}_{k}" if parent_key else k
                    if isinstance(v, dict):
                        if len(v) == 1 and list(v.keys())[0] == k:
                            result[new_key] = list(v.values())[0]
                        else:
                            flatten(v, new_key)
                    else:
                        result[new_key] = v
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    flatten(item, f"{parent_key}_{index}" if parent_key else str(index))
            else:
                result[parent_key] = value
        flatten(data)
        return result


    def flatten_json(self, data):
        transformed = {}
        for key, value in data.items():
            if isinstance(value, dict):
                transformed[key] = self._flatten_json(value)
            else:
                transformed[key] = value
        return transformed
    

    def log_output(self, message: dict) -> Any:
        print(json.dumps(message, indent=4))

    
    def carregar_feriados(self, caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as file:
            feriados_str = json.load(file)
        return {date.fromisoformat(d) for d in feriados_str}


    def calcular_data_uteis(self, data_inicial, dias_uteis, caminho_json):
        feriados = self.carregar_feriados(caminho_json)
        data_inicial = date.fromisoformat(data_inicial)
        contador = 0
        nova_data = data_inicial
        while contador < dias_uteis:
            nova_data += timedelta(days=1)  # Avança um dia
            if nova_data.weekday() < 5 and nova_data not in feriados:  # Seg-Sex e não feriado
                contador += 1
        return nova_data.strftime("%Y-%m-%d")