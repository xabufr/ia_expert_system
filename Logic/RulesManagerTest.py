import unittest
from Rules import Rules, Rule
from RulesJsonSerializer import RulesJsonSerializer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()
        self.__rule_manager = RulesJsonSerializer()

    def test_save_rules(self):
        self.rules.add_rule(Rule("truc", ["1", "2", "3"]))
        self.__rule_manager.save_rules("test_write", self.rules)
        read_data = self.__rule_manager.charge_rules("test_write")
        assert isinstance(read_data, Rules)
        assert read_data.__eq__(self.rules)
        pass

if __name__ == '__main__':
    unittest.main()
