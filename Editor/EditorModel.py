import unittest


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
            positionner.reset()

    def del_condition(self, positionner):
        """
        :param positionner:
        :type positionner: EditorModelPositionner
        """
        if positionner.condition_valid():
            conditions = self.model[positionner.fact][positionner.rule_index]
            conditions = [condition for condition in conditions if condition != positionner.condition]
            self.model[positionner.fact][positionner.rule_index] = conditions
            positionner.condition = None

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
        return []

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
        if positionner.fact is not None and positionner.rule_index is not None:
            return self.model[positionner.fact][positionner.rule_index]
        return []

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

    def rename(self, old_name, new_name):
        new_model = {}
        for index in self.model.keys():
            new_index = index if index != old_name else new_name
            if new_index not in new_model:
                new_model[new_index] = []
            for rule in self.model[index]:
                new_rule = []
                for condition in rule:
                    if condition == old_name:
                        condition = new_name
                    new_rule.append(condition)
                new_model[new_index].append(new_rule)
        self.model = new_model


class EditorModelPositionner():
    def __init__(self):
        self.__fact_index = None
        self.__rule_index = None
        self.__condition = None

    @property
    def fact(self):
        return self.__fact_index

    @fact.setter
    def fact(self, value):
        self.reset()
        self.__fact_index = value

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
        self.condition = None

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, value):
        self.__condition = value

    def reset(self):
        self.__fact_index = None
        self.__rule_index = None
        self.__condition = None

    def fact_valid(self):
        return self.fact is not None

    def rule_valid(self):
        return self.fact_valid() and self.rule_index is not None

    def condition_valid(self):
        return self.rule_valid() and self.condition is not None


class EditorModelTests(unittest.TestCase):
    def setUp(self):
        self.model = EditorModel()

    def test_add(self):
        positionner = EditorModelPositionner()
        fact = "coucou"
        positionner.fact = fact
        self.model.add_fact(fact)
        assert len(self.model.get_facts()) == 1
        assert fact in self.model.get_facts()

        self.model.add_rule_to_fact(positionner)
        positionner.rule_index = '0'
        self.model.add_condition_to_rule("hello", positionner)

        assert len(self.model.get_rule_by_index(positionner)) == 1
        assert "hello" in self.model.get_rule_by_index(positionner)

    def test_del(self):
        self.test_add()
        positionner = EditorModelPositionner()
        positionner.fact = "coucou"
        positionner.rule_index = 0
        positionner.condition = "hello"
        self.model.del_condition(positionner)
        assert positionner.condition is None
        assert len(self.model.get_rule_by_index(positionner)) == 0
        assert positionner.condition_valid() is False
        assert positionner.rule_valid()

        self.model.del_rule_by_index(positionner)
        assert len(self.model.get_fact_rules(positionner)) == 0
        assert positionner.rule_index is None
        assert positionner.rule_valid() is False
        assert positionner.fact_valid()

        self.model.del_fact(positionner)
        assert len(self.model.get_facts()) == 0
        assert positionner.fact is None
        assert positionner.fact_valid() is False

    def test_del_with_some_add(self):
        self.test_add()
        positionner = EditorModelPositionner()
        positionner.fact = "coucou"
        positionner.rule_index = 0
        positionner.condition = "hello"
        self.model.add_condition_to_rule("condition", positionner)
        self.model.del_condition(positionner)
        assert positionner.condition is None
        assert len(self.model.get_rule_by_index(positionner)) == 1
        assert positionner.condition_valid() is False
        assert positionner.rule_valid()

        self.model.add_rule_to_fact(positionner)
        self.model.add_condition_to_rule("condition", positionner)
        positionner.rule_index = 1
        self.model.add_condition_to_rule("condition", positionner)
        positionner.rule_index = 0
        self.model.del_rule_by_index(positionner)
        assert len(self.model.get_fact_rules(positionner)) == 1
        assert positionner.rule_index is None
        assert positionner.rule_valid() is False
        assert positionner.fact_valid()

        positionner.rule_index = 0
        assert len(self.model.get_rule_by_index(positionner)) == 1
        assert "condition" in self.model.get_rule_by_index(positionner)

        self.model.del_fact(positionner)
        assert len(self.model.get_facts()) == 0
        assert positionner.fact is None
        assert positionner.fact_valid() is False

    def test_positions(self):
        self.test_add()
        assert "coucou" in self.model.get_final_conclusions()
        assert len(self.model.get_final_conclusions()) == 1

        assert "hello" in self.model.get_initial_premises()
        assert len(self.model.get_initial_premises()) == 1

    def test_refactor_name(self):
        self.test_add()
        self.model.rename("coucou", "coucou2")

        assert "coucou2" in self.model.get_facts()
        assert len(self.model.get_facts()) == 1

        self.model.rename("hello", "hello2")
        position = EditorModelPositionner()
        position.fact = "coucou2"
        position.rule_index = 0
        assert "hello2" in self.model.get_rule_by_index(position)
        assert len(self.model.get_rule_by_index(position)) == 1

        self.model.add_fact("coucou")
        position.fact = "coucou"
        self.model.add_rule_to_fact(position)
        position.rule_index = 0
        self.model.add_condition_to_rule("hello", position)

        self.model.rename("coucou", "coucou2")
        position.fact = "coucou2"

        assert len(self.model.get_facts()) == 1
        assert len(self.model.get_fact_rules(position)) == 2
        assert len(self.model.get_fact_rules(position)[0]) == 1
        assert len(self.model.get_fact_rules(position)[1]) == 1
        assert ("hello2" in self.model.get_fact_rules(position)[0] and "hello" in self.model.get_fact_rules(position)[
            1]) or (
                   "hello2" in self.model.get_fact_rules(position)[1] and "hello" in
                   self.model.get_fact_rules(position)[0])
