from ctypes import c_bool
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

    def infer_backward(self):
        pass


class Rules:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def find_conclusions(self):
        conclusions = []
        for onerule in self.rules:
            is_conclusion = True
            for otherrule in self.rules:
                if onerule.conclusion in otherrule.conditions:
                    is_conclusion = False
                    break

            if is_conclusion:
                conclusions.append(onerule)
        return conclusions


class Facts:
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
        self.rules = Rules()
        self.facts = Facts()
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
        assert last_rule == None

    def _return_result_for(self, enabled):
        for condition in enabled:
            self.facts.set_fact_value(condition, True)
        return self.expert.infer_forward()

    def test_find_one_conclusion(self):
        assert len(self.rules.find_conclusions()) == 1
        assert 'E' == self.rules.find_conclusions()[0].conclusion

    def test_find_no_conclusion(self):
        self.rules.add_rule(Rule("A", ["E"]))
        assert len(self.rules.find_conclusions()) == 0

    def test_find_multiple_conclusion(self):
        self.rules.add_rule(Rule("G", ["H"]))
        self.rules.add_rule(Rule("I", ["D"]))
        conclusions = self.rules.find_conclusions()
        assert len(conclusions) == 3
        assert self._isconclusion_in_rules("G", conclusions)
        assert self._isconclusion_in_rules("I", conclusions)
        assert self._isconclusion_in_rules("E", conclusions)



    def _isconclusion_in_rules(self, conclusion, rules):
        for rule in rules:
            if conclusion == rule.conclusion:
                return True
        return False

if __name__ == "__main__":
    unittest.main()