import re
import copy 


def find_actc_errors_decorator(func):
    def wrapper(self, header, actc_type, group, content):
        actc_data       = copy.deepcopy(content)
        if actc_errors := self.find_actc_errors(content):
            if len(actc_errors) > 0:
                content["Actc_Erros"] = actc_errors
        return func(self, header, actc_type, group, content, actc_data)
    return wrapper


def filter_actc_keys(func):
    def wrapper(self, data):
        o7doc           = data.get("O7DOC", {})
        header_pattern  = re.compile(r"HeaderCTC.*$")
        actc_pattern    = re.compile(r"ACTC\d{3}.*$")
        header          = dict({key: value for key, value in o7doc.items() if header_pattern.match(key)})
        actc_data       = {key: value for key, value in o7doc.items() if actc_pattern.match(key)}
        return func(self, actc_data, header)
    return wrapper


def count_processing(func):
    def wrapper(self, context, actc_data):
        self.total_run += 1
        result = func(self, context, actc_data)
        if result:
            self.total_processed += 1
        return result
    return wrapper