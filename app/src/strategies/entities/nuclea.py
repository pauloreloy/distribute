import xmltodict
from typing                             import Dict, Any
from src.strategies.entities.entity     import Entity
from src.utils.mapper                   import Mapper
from src.utils.utils                    import Utils
from src.decorators.actc                import find_actc_errors_decorator, filter_actc_keys


class Nuclea(Entity):


    def __init__(self):
        super().__init__("NUCLEA")
        self.total_processed = 0
        self.total_run       = 0
        self.nome_arq        = None
        

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
        mapper = Mapper(actc_type, "mapper.json")
        return {
            'actc_type':    actc_type,
            'group':        group,
            'header':       header,
            'actc':         actc_data,
            'integracao':   mapper.map(content),
            'fisico':       mapper.map(content),
        }


    def run(self, context: object, aws_client: object, data: Dict[str, Any]) -> bool:
        if not data:
            return False
        context.set_strategy("ACTC")
        self.aws_client = aws_client
        data            = xmltodict.parse(data)
        for header, actc_type, group, content in self.extract_actc_data(data):
            if not self.nome_arq:
                self.nome_arq   = header.get("HeaderCTC", {}).get("NomeArq", None)
            self.total_run += 1
            actc_data       = self.convert_actc_content(header, actc_type, group, content)
            if context.run(context, self.aws_client, actc_data):
                self.total_processed += 1
        
        Utils().log_output({
            "Arquivo":      self.nome_arq,
            "Total":        self.total_run,
            "Processadas":  self.total_processed,
            "Erros":        self.total_run - self.total_processed
        })

        return True