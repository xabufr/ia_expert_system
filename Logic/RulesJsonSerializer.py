import json
from Rules import Rules


class RulesJsonSerializer:
    def __init__(self):
        self.rules = Rules()

    def save_rules(self, file_name, rules):
        self.__write_json_into_file(file_name, rules.serialize())

    def charge_rules(self, file_name):
        return Rules.deserialize(Rules, self.__load_json_from_file(file_name))

    def __load_json_from_file(self, file_name):
        file_name += ".json"
        file = open(file_name)
        return json.load(file)

    def __write_json_into_file(self, file_name, json_data):
        file_name += ".json"
        file = open(file_name, "w")
        file.write(json.dumps(json_data, indent=4))
        pass