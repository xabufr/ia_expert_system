import unittest


class Expert:
    def __init__(self, rules_manager, facts_manager):
        self.__rules = rules_manager
        self.__facts = facts_manager

    def is_rule_valid(self, rule):
        for condition in rule.conditions:
            if not self.__facts.is_condition_valid(condition):
                return False
        return True

    def is_rule_already_valid(self, rule):
        return self.__facts.is_condition_valid(rule.conclusion)

    def infer_forward(self):
        last_conclusion = None
        while True:
            modified = False
            for rule in self.__rules.rules:
                if not self.is_rule_already_valid(rule) and self.is_rule_valid(rule):
                    self.__facts.set_fact_value(rule.conclusion, True)
                    modified = True
                    last_conclusion = rule
            if not modified:
                break
        return last_conclusion

    def infer_backward(self):
        final_conclusions = self.__rules.find_conclusions()
        for conclusion in final_conclusions:
            if not self.__facts.is_fact_set(conclusion.conclusion):
                pass


class Rules:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def find_conclusions(self):
        conclusions = []
        for rule in self.rules:
            if self.is_final_conclusion(rule):
                conclusions.append(rule)
        return conclusions

    def is_final_conclusion(self, rule_to_test):
        for rule in self.rules:
            if rule_to_test.conclusion in rule.conditions:
                return False
        return True

    def is_initial_premice(self, premice):
        for rule in self.rules:
            if premice in rule.conclusion:
                return False
        return True

    def find_by_conclusion(self, conclusion):
        previous_rules = []
        for rule in self.rules:
            if rule.conclusion == conclusion:
                previous_rules.append(rule)
        return previous_rules


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

    def is_fact_set(self, fact_name):
        for fact in self.facts:
            if fact_name == fact.condition:
                return True
        return False

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

    def test_is_a_initial_premice(self):
        assert self.rules.is_initial_premice("A")
        assert self.rules.is_initial_premice("B")
        assert self.rules.is_initial_premice("F")
        assert not self.rules.is_initial_premice("C")
        assert not self.rules.is_initial_premice("D")
        assert not self.rules.is_initial_premice("E")

    def test_can_find_by_conclusion(self):
        previous_rules = self.rules.find_by_conclusion("E")
        for rule in previous_rules:
            assert rule.conclusion == "E"

    def test_is_all_premicies_false(self):
        previous_rules = self.rules.find_by_conclusion("E")
        for rule in previous_rules:
            premicies = rule.conditions
            for condition in premicies:
                assert not self.facts.is_condition_valid(condition)

    def test_some_rules_are_true(self):
        self.facts.set_fact_value("C", True)
        self.facts.set_fact_value("F", True)
        previous_rules = self.rules.find_by_conclusion("E")

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

    def test_backward(self):
        question = self.expert.infer_backward()
        assert question == "A"

    def _isconclusion_in_rules(self, conclusion, rules):
        for rule in rules:
            if conclusion == rule.conclusion:
                return True
        return False

if __name__ == "__main__":
    unittest.main()