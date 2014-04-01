import os
from PySide.QtUiTools import QUiLoader
from PySide.QtCore import QObject, QFile
from PySide.QtGui import QInputDialog, QTreeWidgetItem
from Logic.Rules import Rules, Rule


class EditorMainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__ui = None
        self.__setup_ui()
        self.__model = {}
        self.__currentFactItem = None
        self.__currentRuleItem = None

    def __load_ui(self):
        ui_path = os.path.join(os.path.dirname(__file__), "MainWindow.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        ui_loader = QUiLoader()
        self.__ui = ui_loader.load(ui_file, None)

    def __setup_ui(self):
        self.__load_ui()
        self.__setup_slots()
        self.__ui.show()

    def __setup_slots(self):
        self.__ui.btn_add_fact.clicked.connect(self.__add_fact)
        self.__ui.btn_delete_fact.clicked.connect(self.__delete_facts)
        self.__ui.facts.currentItemChanged.connect(self.__fact_changed)

        self.__ui.btn_add_rule.clicked.connect(self.__add_rule_for_current_fact)
        self.__ui.btn_delete_rule.clicked.connect(self.__del_rule_for_current_fact)
        self.__ui.rules.currentItemChanged.connect(self.__rule_changed)

        self.__ui.btn_add_premise.clicked.connect(self.__add_premise_to_current_rule)

    def __add_fact(self):
        rule_conclusion, entered = QInputDialog.getText(self.__ui, self.tr("Enter rule conclusion label"),
                                                        self.tr("Conclusion"))
        if entered and rule_conclusion not in self.__model.keys():
            self.__ui.facts.addItem(rule_conclusion)
            self.__model[rule_conclusion] = []

            self.__ui.facts.setCurrentRow(self.__ui.facts.count() - 1)
            self.__update_helpers()

    def __delete_facts(self):
        fact_item = self.__currentFactItem
        if fact_item:
            self.__ui.facts.takeItem(self.__ui.facts.row(fact_item))
            del self.__model[fact_item.text()]

    def __fact_changed(self, fact_item):
        self.__currentFactItem = fact_item
        self.__currentRuleItem = None
        self.__load_rules_for_current_fact()

    def __rule_changed(self, rule_item):
        self.__currentRuleItem = rule_item
        self.__load_premises_for_current_rule()

    def __load_rules_for_current_fact(self):
        self.__ui.rules.clear()
        if self.__currentFactItem is not None:
            rules = self.__get_rules_of_current_fact()
            for index, rule in enumerate(rules):
                self.__ui.rules.addItem(str(index))
            if rules:
                self.__ui.rules.setCurrentRow(0)
                self.__load_premises_for_current_rule()
        self.__load_premises_for_current_rule()

    def __add_rule_for_current_fact(self):
        if self.__currentFactItem is not None:
            rule = []
            rules = self.__get_rules_of_current_fact()
            rules.append(rule)
            self.__load_rules_for_current_fact()
            self.__ui.rules.setCurrentRow(self.__ui.rules.count() - 1)

    def __del_rule_for_current_fact(self):
        rules = self.__get_rules_of_current_fact()
        if rules is not None and self.__currentRuleItem is not None:
            rule_index = int(self.__currentRuleItem.text())
            self.__ui.rules.takeItem(self.__ui.rules.row(self.__currentRuleItem))
            del rules[rule_index]
            self.__load_rules_for_current_fact()

            if rules:
                self.__ui.rules.setCurrentRow(0)

    def __load_premises_for_current_rule(self):
        premises = self.__get_premises_for_current_rule()
        self.__ui.premises.clear()
        if premises is not None:
            for premise in premises:
                self.__ui.premises.addItem(premise)
            if premises:
                self.__ui.premises.setCurrentRow(0)

    def __add_premise_to_current_rule(self):
        premises = self.__get_premises_for_current_rule()
        if premises is not None:
            premise, valid = QInputDialog.getText(self.__ui, self.tr("Enter premise"), self.tr("Premise"))
            if valid:
                premises.append(premise)
                self.__load_premises_for_current_rule()
            self.__update_helpers()

    def __get_rules_of_current_fact(self):
        if self.__currentFactItem is not None:
            return self.__model[self.__currentFactItem.text()]
        return None

    def __get_premises_for_current_rule(self):
        rules = self.__get_rules_of_current_fact()
        if rules and self.__currentRuleItem:
            return rules[int(self.__currentRuleItem.text())]
        return None

    def __get_all_conditions(self):
        conditions = []
        for fact in self.__model.keys():
            rules = self.__model[fact]
            for rule in rules:
                for condition in rule:
                    if condition not in conditions:
                        conditions.append(condition)
        return conditions

    def __get_labels(self):
        return self.__get_all_conditions()

    def __get_initial_premises(self):
        labels = self.__get_all_conditions()
        labels = [label for label in labels if label not in self.__model.keys()]
        return labels

    def __update_helpers(self):
        self.__fill_initial_premises()
        self.__fill_final_conclusions()
        self.__fill_intermediate_conclusions()

    def __fill_initial_premises(self):
        initial = self.__get_initial_premises()
        self.__ui.initial_premises.clear()
        for premise in initial:
            self.__ui.initial_premises.addItem(premise)

    def __find_final_conclusion(self):
        conditions = self.__get_all_conditions()
        final_conclusions = [conclusion for conclusion in self.__model.keys() if conclusion not in conditions]
        return final_conclusions

    def __fill_final_conclusions(self):
        self.__ui.final_conclusions.clear()
        final_conclusions = self.__find_final_conclusion()
        for conclusion in final_conclusions:
            self.__ui.final_conclusions.addItem(conclusion)

    def __find_intermediate_conclusions(self):
        initial = self.__get_initial_premises()
        conclusion = self.__find_final_conclusion()
        return [label for label in self.__get_labels() if label not in initial and label not in conclusion ]

    def __fill_intermediate_conclusions(self):
        self.__ui.intermediate_conclusions.clear()
        intermediate_conclusions = self.__find_intermediate_conclusions()
        for intermediate_conclusion in intermediate_conclusions:
            self.__ui.intermediate_conclusions.addItem(intermediate_conclusion)
