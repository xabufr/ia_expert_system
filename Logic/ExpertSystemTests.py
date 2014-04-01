import unittest
from Logic.ExpertSystem import Expert
from Logic.Facts import Facts
from Logic.Rules import Rules, Rule


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