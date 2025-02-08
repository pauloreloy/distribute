import json


class Mapper:


    def __init__(self, data, mapper_file):
        self.data = data
        with open(mapper_file, 'r') as f:
            self.mapper = json.load(f)
    

    def map_keys(self):
        return self._map_recursive(self.data)
    

    def _map_recursive(self, data):
        if isinstance(data, dict):
            mapped_data = {}
            for key, value in data.items():
                if(len(value) > 0):
                    new_key = self.mapper.get(key, f"notmapped:{key}")
                    mapped_data[new_key] = self._map_recursive(value)
            return mapped_data
        elif isinstance(data, list):
            return [self._map_recursive(item) for item in data]
        else:
            return data