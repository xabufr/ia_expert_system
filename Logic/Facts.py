class Facts:
    def __init__(self):
        self.facts = {}

    def is_condition_valid(self, condition):
        return self.facts[condition] if condition in self.facts else False

    def set_fact_value(self, condition, value):
        self.facts[condition] = value

    def is_fact_set(self, fact_name):
        return fact_name in self.facts

    def reset(self):
        self.facts = {}