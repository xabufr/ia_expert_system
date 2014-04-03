import json
from Logic.Rules import Rules


def save_rules(file_name, rules):
    write_json_into_file(file_name, rules.serialize())


def charge_rules(file_name):
    return Rules.deserialize(Rules, load_json_from_file(file_name))


def load_json_from_file(file_name):
    file = open(file_name)
    return json.load(file)


def write_json_into_file(file_name, json_data):
    file = open(file_name, "w")
    file.write(json.dumps(json_data, indent=4))
    pass