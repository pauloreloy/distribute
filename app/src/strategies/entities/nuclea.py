import xmltodict
import re
from typing                             import Any 
from src.strategies.entities.entity     import Entity
from src.utils.mapper                   import Mapper
from src.utils.utils                    import Utils

class Nuclea(Entity):


    def __init__(self):
        self.name = "Nuclea"
        super().__init__(self.name)


    def set_data(self, data: Any) -> None:
        self.data = data


    def process_ret(self, actc_type: str, group: str, content: Any) -> Any:
        pass


    def extract_actc_data(self, data) -> Any:
        for key, value in data.get("O7DOC", {}).items():
            if re.match(r"ACTC\d{3}.*$", key):
                actc_type = key
                groups = {sub_key: sub_value for sub_key, sub_value in value.items() if sub_key.startswith(f"Grupo_{actc_type}_")}
                for group in groups:
                    if isinstance(groups[group], list):
                        for group_ in groups[group]:
                            yield actc_type, group, group_
                    else:
                        yield actc_type, group, groups[group]


    def find_actc_errors(self, content: Any, previous_key: str = None) -> Any:
        errors = []
        for key, value in list(content.items()):
            if isinstance(value, dict):
                errors.extend(self.find_actc_errors(value, key))
            if key.startswith("@CodErro"):
                _value = content.get("#text", "Unknown")
                errors.append({
                    "Campo":    previous_key,
                    "Valor":    content.pop("#text", "Unknown"),
                    "Erro":     content.pop(key, "Unknown")
                })
                content[previous_key] = _value
        return errors
    

    def convert_actc_content(self, content: Any) -> Any:
        _actc = content.copy()
        if(actc_errors := self.find_actc_errors(content)):
            if(len(actc_errors) > 0):
                content["Actc_Erros"] = actc_errors
        content = Utils().transform_json(content)
        return {
            'actc':         _actc,
            'integracao':   Mapper(content, "mapper.json").map_keys(),
            'fisico':       Mapper(content, "mapper.json").map_keys()
        }


    def process_actc(self, actc_type: str, group: str, actc_proc: Any, total_groups) -> Any:
        return True
    
    
    def log_output(self, total_groups: int, total_process: int) -> Any:
        print(f"Total de portabilidades: {total_groups}, Processadas: {total_process}, Error: {total_groups - total_process}")


    def run(self, aws_client: object) -> Any:
        self.aws_client     = aws_client
        if self.data:
            data            = xmltodict.parse(self.data)
            total_process   = 0
            total_groups    = 0
            for actc_type, group, content in self.extract_actc_data(data):
                total_groups += 1
                actc_proc = self.convert_actc_content(content)
                if re.match(r"^ACTC.*(RET|4)$", actc_type):
                    self.process_ret(actc_type, group, actc_proc)
                if self.process_actc(actc_type, group, actc_proc, total_groups):
                    total_process += 1
            self.log_output(total_groups, total_process)
            return
