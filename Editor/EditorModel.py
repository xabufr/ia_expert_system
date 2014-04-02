class EditorModel():
    def __init__(self):
        self.model = {}

    def add_fact(self, fact):
        if fact not in self.model.keys():
            self.model[fact] = []

    def del_fact(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        if positionner.fact in self.model.keys():
            del self.model[positionner.fact]

    def add_rule_to_fact(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        rules = self.model[positionner.fact]
        premises = []
        rules.append(premises)
        return premises

    def get_fact_rules(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        if positionner.fact in self.model.keys():
            return self.model[positionner.fact]
        return None

    def add_condition_to_rule(self, condition, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        rule = self.get_rule_by_index(positionner)
        rule.append(condition)

    def del_rule_by_index(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        rules = self.model[positionner.fact]
        if rules:
            del rules[positionner.rule_index]
            positionner.rule_index = None

    def get_rule_by_index(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        rules = self.model[positionner.fact]
        if positionner.rule_index is not None:
            return rules[positionner.rule_index]
        return None

    def get_facts(self):
        return self.model.keys()

    def get_initial_premises(self):
        labels = self.get_all_conditions()
        return [label for label in labels if label not in self.model.keys()]

    def get_final_conclusions(self):
        conditions = self.get_all_conditions()
        return [conclusion for conclusion in self.model.keys() if conclusion not in conditions]

    def get_labels(self):
        labels = self.get_all_conditions()
        [labels.append(label) for label in self.model.keys() if label not in labels]
        return labels

    def get_intermediate_conclusions(self):
        initial = self.get_initial_premises()
        conclusion = self.get_final_conclusions()
        return [label for label in self.get_labels() if label not in initial and label not in conclusion]

    def get_all_conditions(self):
        conditions = []
        for fact in self.model.keys():
            rules = self.model[fact]
            for rule in rules:
                for condition in rule:
                    if condition not in conditions:
                        conditions.append(condition)
        return conditions


class EditorModelPositionner():
    def __init__(self):
        self.__fact_index = None
        self.__rule_index = None

    @property
    def fact(self):
        return self.__fact_index

    @fact.setter
    def fact(self, value):
        self.__fact_index = value
        self.__rule_index = None

    @property
    def rule_index(self):
        return self.__rule_index

    @rule_index.setter
    def rule_index(self, value):
        if value is not None:
            assert int(value) >= 0
            self.__rule_index = int(value)
        else:
            self.__rule_index = None


