import unittest
from ExpertSystem import Expert
from Facts import Facts
from Rules import Rules, Rule
from Logic.Facts import Facts


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

    def test_skip_non_util_question(self):
        self.facts = Facts()
        self.rules = Rules()

        self.rules.add_rule(Rule("C1", ["A", "B"]))
        self.rules.add_rule(Rule("C1", ["A", "D"]))

        self.facts.set_fact_value("A", False)

        self.expert = Expert(self.rules, self.facts)

        assert self.expert.infer_backward() is None

    def test_skip_non_util_question_multiple_rules(self):
        self.facts = Facts()
        self.rules = Rules()

        self.rules.add_rule(Rule("C1", ["A", "B"]))
        self.rules.add_rule(Rule("C1", ["A", "D"]))
        self.rules.add_rule(Rule("C2", ["A1", "E1"]))
        self.rules.add_rule(Rule("C2", ["A1", "E2"]))
        self.rules.add_rule(Rule("C2", ["A2", "F"]))

        self.facts.set_fact_value("A", False)
        self.facts.set_fact_value("E1", False)
        self.facts.set_fact_value("E2", False)
        self.facts.set_fact_value("A2", True)

        self.expert = Expert(self.rules, self.facts)

        assert self.expert.infer_backward() is "F"


if __name__ == "__main__":
    unittest.main()