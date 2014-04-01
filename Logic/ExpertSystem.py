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
        premises = self.__rules.find_premises()
        for premise in premises:
            if not self.__facts.is_fact_set(premise):
                return premise
        return None


class Rules:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def is_initial_premise(self, premise):
        for rule in self.rules:
            if premise in rule.conclusion:
                return False
        return True

    def find_premises(self):
        premises = []
        # version grande classe!
        # [premises.append(premise) for rule in self.rules for premise in rule.conditions if self.is_initial_premise(premise) and premise not in premises]
        # return premises
        for rule in self.rules:
            for premise in rule.conditions:
                if self.is_initial_premise(premise) and premise not in premises:
                    premises.append(premise)
        return premises


class Facts:
    def __init__(self):
        self.facts = {}

    def is_condition_valid(self, condition):
        return self.facts[condition] if condition in self.facts else False

    def set_fact_value(self, condition, value):
        self.facts[condition] = value

    def is_fact_set(self, fact_name):
        return fact_name in self.facts


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
        assert last_rule is None

    def test_is_a_initial_premise(self):
        assert self.rules.is_initial_premise("A")
        assert self.rules.is_initial_premise("B")
        assert self.rules.is_initial_premise("F")
        assert not self.rules.is_initial_premise("C")
        assert not self.rules.is_initial_premise("D")
        assert not self.rules.is_initial_premise("E")

    def test_if_fact_is_not_set(self):
        for fact in ["A", "B", "C"]:
            assert not self.facts.is_fact_set(fact)

    def test_if_fact_set(self):
        assert not self.facts.is_fact_set("A")
        self.facts.set_fact_value("A", True)
        assert self.facts.is_fact_set("A")
        self.facts.set_fact_value("A", False)
        assert self.facts.is_fact_set("A")

        assert not self.facts.is_fact_set("B")
        self.facts.set_fact_value("B", False)
        assert self.facts.is_fact_set("B")
        self.facts.set_fact_value("B", True)
        assert self.facts.is_fact_set("B")

    def _return_result_for(self, enabled):
        for condition in enabled:
            self.facts.set_fact_value(condition, True)
        return self.expert.infer_forward()

    def test_backward(self):
        question = self.expert.infer_backward()
        assert question == "A"

    def test_can_retrieve_initial_premises(self):
        premises = self.rules.find_premises()
        assert len(premises) == 3
        for premise in ["A", "B", "F"]:
            assert premise in premises

    def _is_conclusion_in_rules(self, conclusion, rules):
        for rule in rules:
            if conclusion == rule.conclusion:
                return True
        return False

if __name__ == "__main__":
    unittest.main()