import unittest
import json
from Rules import Rules


class RulesManager:
    def load_json_from_file(self, file_name):
        file_name += ".json"
        file = open(file_name)
        return json.load(file)

    def write_json_into_file(self, file_name, json_data):
        file_name += ".json"
        file = open(file_name, "w")
        file.write(json.dumps(json_data, indent=4))
        pass


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Rules):
            return super(MyEncoder, self).default(obj)
        return obj.__dict__

class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.__rule_manager = RulesManager()

    def test_open_a_json_file(self):
        json_data = self.__rule_manager.load_json_from_file("test_read")
        assert json_data == [{"toto":["titi"]}]
        pass

    def test_write_json(self):
        json_data = {"titi":"toto"}
        self.__rule_manager.write_json_into_file("test_write", json_data)
        read_data = self.__rule_manager.load_json_from_file("test_write")
        assert read_data == json_data
        pass

    def test_add_rule(self):
        rules = Rules()
        rules.add_rule("truc")
        rules_serialized = json.dumps(rules, cls=MyEncoder)
        rules_serialized = json.loads(rules_serialized)
        self.__rule_manager.write_json_into_file("test_write", rules_serialized)
        read_data = self.__rule_manager.load_json_from_file("test_write")
        assert read_data == rules_serialized
        pass

if __name__ == '__main__':
    unittest.main()
