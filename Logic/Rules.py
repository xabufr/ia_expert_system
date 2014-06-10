from copy import copy
from uuid import uuid4


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

    def serialize(self):
        rules = []
        clone = copy(self)
        for rule in self.rules:
            rules.append(rule.serialize())

        clone.rules = rules
        return clone.__dict__

    def deserialize(self, json_object):
        rules = Rules()
        for rule in json_object["rules"]:
            rules.add_rule(Rule.deserialize(Rule, rule))
        return rules

    def __eq__(self, other):
        return self.rules == other.rules

    def is_terminal_rule(self, rule_to_test):
        for rule in self.rules:
            if rule is not rule_to_test and rule_to_test.conclusion in rule.conditions:
                return False
        return True

    def find_rules_with_condition(self, condition):
        return [rule for rule in self.rules if condition in rule.conditions]


class Rule:
    def __init__(self, conclusion, conditions):
        self.conclusion = conclusion
        self.conditions = conditions
        pass

    def serialize(self):
        return self.__dict__

    def deserialize(self, json_object):
        return Rule(json_object["conclusion"], json_object["conditions"])

    def __eq__(self, other):
        return self.conclusion == other.conclusion and self.conditions == other.conditions
