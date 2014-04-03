import unittest
from Rules import Rules, Rule
import RulesJsonSerializer


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.rules = Rules()

    def test_save_rules(self):
        self.rules.add_rule(Rule("truc", ["1", "2", "3"]))
        RulesJsonSerializer.save_rules("test_write.json", self.rules)
        read_data = RulesJsonSerializer.charge_rules("test_write.json")
        assert isinstance(read_data, Rules)
        assert read_data.__eq__(self.rules)
        pass

if __name__ == '__main__':
    unittest.main()
