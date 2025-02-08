import xmltodict
import re
from typing                             import Dict, Any
from src.strategies.entities.entity     import Entity
from src.utils.mapper                   import Mapper
from src.utils.utils                    import Utils
from src.decorators.exceptions          import exception_decorator
from src.decorators.actc                import find_actc_errors_decorator, filter_actc_keys, count_processing


class Nuclea(Entity):


    def __init__(self):
        super().__init__("Nuclea")
        self.total_processed = 0


    def set_data(self, data: Dict[dict, Any]) -> None:
        self.data = xmltodict.parse(data)


    def find_actc_errors(self, content: dict, previous_key: str = None) -> list:
        errors = []
        for key, value in list(content.items()):
            if isinstance(value, dict):
                errors.extend(self.find_actc_errors(value, key))
            if str(key).startswith("@CodErro"):
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
            groups = {sub_key: sub_value for sub_key, sub_value in value.items() if str(sub_key).startswith(f"Grupo_{actc_type}_")}
            for group, group_value in groups.items():
                if isinstance(group_value, list):
                    yield from ((header,  actc_type, group, item) for item in group_value)
                else:
                    yield header, actc_type, group, group_value


    @find_actc_errors_decorator
    def convert_actc_content(self, header: dict, actc_type: str, group: str, content: Any, actc_data: dict) -> dict:
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
    def process_ret(self, actc_data: Dict[dict, list]) -> bool:
        return True
    

    @count_processing
    @exception_decorator
    def process_actc(self, actc_data: Dict[dict, list]) -> bool:
        return True


    def run(self, aws_client: object) -> bool:
        self.aws_client     = aws_client
        if not self.data:
            return False
        total_groups = 0
        for header, actc_type, group, content in self.extract_actc_data(self.data):
            total_groups    += 1
            actc_data       = self.convert_actc_content(header, actc_type, group, content)
            if re.match(r"^ACTC.*(RET|4)$", actc_type):
                self.process_ret(actc_data)
            else:
                self.process_actc(actc_data)
        Utils().log_output({
            "Arquivo":      header.get("HeaderCTC", {}).get("NomeArq", None),
            "Total":        total_groups,
            "Processadas":  self.total_processed,
            "Erros":        total_groups - self.total_processed
        })
        return True