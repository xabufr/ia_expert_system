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

    def is_terminal_rule(self, rule_to_test):
        for rule in self.rules:
            if rule is not rule_to_test and rule_to_test.conclusion in rule.conditions:
                return False
        return True


class Rule:
    def __init__(self, conclusion, conditions):
        self.conclusion = conclusion
        self.conditions = conditions