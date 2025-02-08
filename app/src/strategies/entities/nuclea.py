import xmltodict
import re
from typing                             import Any 
from src.strategies.entities.entity     import Entity
from src.utils.mapper                   import Mapper
from src.utils.utils                    import Utils
from src.decorators.exceptions          import exception_decorator
from src.decorators.actc                import find_actc_errors_decorator, filter_actc_keys, count_processing


class Nuclea(Entity):


    def __init__(self):
        self.name               = "Nuclea"
        self.total_processed    = 0
        super().__init__(self.name)


    def set_data(self, data: Any) -> None:
        self.actc_data = data


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


    @filter_actc_keys
    def extract_actc_data(self, data: dict, header: dict) -> Any:
        for actc_type, value in data.items():
            groups = {sub_key: sub_value for sub_key, sub_value in value.items() if sub_key.startswith(f"Grupo_{actc_type}_")}
            for group, group_value in groups.items():
                if isinstance(group_value, list):
                    yield from ((header,  actc_type, group, item) for item in group_value)
                else:
                    yield header, actc_type, group, group_value


    @find_actc_errors_decorator
    def convert_actc_content(self, header: dict, actc_type: str, group: str, content: Any, actc_data: Any) -> dict:
        content = Utils().flatten_json(content)
        return {
            'actc_type':    actc_type,
            'group':        group,
            'header':       header,
            'actc':         actc_data,
            'integracao':   Mapper(actc_type, "mapper.json").map(content),
            'fisico':       Mapper(actc_type, "mapper.json").map(content),
        }


    @count_processing
    @exception_decorator
    def process_ret(self, actc_proc: Any) -> Any:
        return True
    

    @count_processing
    @exception_decorator
    def process_actc(self, actc_proc: Any) -> Any:
        return True


    def run(self, aws_client: object) -> Any:
        self.aws_client     = aws_client
        if self.actc_data:
            data            = xmltodict.parse(self.actc_data)
            total_groups        = 0
            for header, actc_type, group, content in self.extract_actc_data(data):
                total_groups    += 1
                actc_proc       = self.convert_actc_content(header, actc_type, group, content)
                if re.match(r"^ACTC.*(RET|4)$", actc_type):
                    self.process_ret(actc_proc)
                else:
                    self.process_actc(actc_proc)
            Utils().log_output({
                "Arquivo":      header.get("HeaderCTC",{}).get("NomeArq", None),
                "Total":        total_groups,
                "Processadas":  self.total_processed,
                "Erros":        total_groups - self.total_processed
            })
            return
