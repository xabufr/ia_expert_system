import unittest


class Expert:
    def __init__(self, rules_manager, facts_manager):
        self.__rulesManager = rules_manager
        self.__factsManager = facts_manager

    def is_rule_valid(self, rule):
        for condition in rule.conditions:
            if not self.__factsManager.is_condition_valid(condition):
                return False
        return True

    def is_rule_already_valid(self, rule):
        return self.__factsManager.is_condition_valid(rule.conclusion)

    def infer_forward(self):
        last_conclusion = None
        while True:
            modified = False
            for rule in self.__rulesManager.rules:
                if not self.is_rule_already_valid(rule) and self.is_rule_valid(rule):
                    self.__factsManager.set_fact_value(rule.conclusion, True)
                    modified = True
                    last_conclusion = rule
            if not modified:
                break
        return last_conclusion


class RuleManager:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)


class FactsManager:
    def __init__(self):
        self.facts = []

    def is_condition_valid(self, condition):
        for fact in self.facts:
            if fact.value and fact.condition == condition:
                return True
        return False

    def set_fact_value(self, condition, value):
        fact = self.find_fact(condition)
        if fact is None:
            fact = Fact(condition, value)
            self.facts.append(fact)
        else:
            fact.value = value

    def find_fact(self, condition):
        for fact in self.facts:
            if fact.condition == condition:
                return fact
        return None


class Rule:
    def __init__(self, conclusion, conditions):
        self.conclusion = conclusion
        self.conditions = conditions


class Fact:
    def __init__(self, condition, value):
        self.condition = condition
        self.value = value


class ExpertTest(unittest.TestCase):
    def setUp(self):
        self.rules = RuleManager()
        self.facts = FactsManager()
        self.expert = Expert(self.rules, self.facts)
        self.rules.add_rule(Rule("C", ["A", "B"]))
        self.rules.add_rule(Rule("E", ["C", "D", "F"]))
        self.rules.add_rule(Rule("D", ["C"]))

    def test_one_iteration(self):
        last_rule = self._return_result_for(["A", "B"])
        assert last_rule.conclusion == "D"

    def test_two_iteration(self):
        last_rule = self._return_result_for(["A", "B", "F"])
        assert last_rule.conclusion == "E"

    def test_zero_iteration(self):
        last_rule = self._return_result_for(["A", "F"])
        assert last_rule

    def _return_result_for(self, enabled):
        for condition in enabled:
            self.facts.set_fact_value(condition, True)
        return self.expert.infer_forward()


if __name__ == "__main__":
    unittest.main()