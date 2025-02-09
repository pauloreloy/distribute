
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

    
    def load_holidays(self, caminho_json):
        with open(caminho_json, "r", encoding="utf-8") as file:
            holidays_str = json.load(file)
        return {date.fromisoformat(d) for d in holidays_str}


    def calculate_business_days(self, initial_date, business_days, caminho_json = "feriados.json"):
        holidays        = self.load_holidays(caminho_json)
        initial_date    = date.fromisoformat(initial_date)
        counter         = 0
        new_date        = initial_date
        while counter   < business_days:
            new_date    += timedelta(days=1)  # Avança um dia
            if new_date.weekday() < 5 and new_date not in holidays:  # Seg-Sex e não feriado
                counter += 1
        return new_date.strftime("%Y-%m-%d")