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
