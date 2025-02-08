from typing import Dict, Any
import json


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