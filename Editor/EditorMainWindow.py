import os
from PySide.QtUiTools import QUiLoader
from PySide.QtCore import QObject, QFile
from PySide.QtGui import QInputDialog
from EditorModel import EditorModel, EditorModelPositionner


class EditorMainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__ui = None
        self.__setup_ui()
        self.__model = EditorModel()
        self.__current_model_position = EditorModelPositionner()

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

        self.__ui.btn_add_premise.clicked.connect(self.__add_condition_to_current_rule)

    def __add_fact(self):
        rule_conclusion, entered = QInputDialog.getText(self.__ui, self.tr("Enter rule conclusion label"),
                                                        self.tr("Conclusion"))
        if entered and rule_conclusion:
            self.__model.add_fact(rule_conclusion)
            self.__fill_facts()

    def __fill_facts(self):
        self.__ui.facts.clear()
        for fact in self.__model.get_facts():
            self.__ui.facts.addItem(fact)
        self.__ui.facts.setCurrentRow(self.__ui.facts.count() - 1)
        self.__update_helpers()

    def __delete_facts(self):
        self.__model.del_fact(self.__current_model_position)
        self.__fill_facts()

    def __fact_changed(self, fact_item):
        if fact_item:
            self.__current_model_position.fact = fact_item.text()
        self.__load_rules_for_current_fact()

    def __rule_changed(self, rule_item):
        if rule_item:
            self.__current_model_position.rule_index = rule_item.text()
        self.__load_premises_for_current_rule()

    def __load_rules_for_current_fact(self):
        self.__ui.rules.clear()
        rules = self.__model.get_fact_rules(self.__current_model_position)
        for index, rule in enumerate(rules):
            self.__ui.rules.addItem(str(index))
        if rules:
            self.__ui.rules.setCurrentRow(0)
            self.__load_premises_for_current_rule()
        self.__load_premises_for_current_rule()

    def __add_rule_for_current_fact(self):
        self.__model.add_rule_to_fact(self.__current_model_position)
        self.__load_rules_for_current_fact()
        self.__ui.rules.setCurrentRow(self.__ui.rules.count() - 1)

    def __del_rule_for_current_fact(self):
        self.__model.del_rule_by_index(self.__current_model_position)
        self.__load_rules_for_current_fact()
        if self.__model.get_fact_rules(self.__current_model_position):
            self.__ui.rules.setCurrentRow(0)

    def __load_premises_for_current_rule(self):
        premises = self.__model.get_rule_by_index(self.__current_model_position)
        self.__ui.premises.clear()
        if premises is not None:
            for premise in premises:
                self.__ui.premises.addItem(premise)
            if premises:
                self.__ui.premises.setCurrentRow(0)

    def __add_condition_to_current_rule(self):
        if self.__current_model_position.rule_index is not None:
            premise, valid = QInputDialog.getText(self.__ui, self.tr("Enter premise"), self.tr("Premise"))
            if valid:
                self.__model.add_condition_to_rule(premise, self.__current_model_position)
                self.__load_premises_for_current_rule()
            self.__update_helpers()

    def __update_helpers(self):
        self.__fill_initial_premises()
        self.__fill_final_conclusions()
        self.__fill_intermediate_conclusions()
        self.__fill_labels()

    def __fill_initial_premises(self):
        initial = self.__model.get_initial_premises()
        self.__ui.initial_premises.clear()
        for premise in initial:
            self.__ui.initial_premises.addItem(premise)

    def __fill_final_conclusions(self):
        self.__ui.final_conclusions.clear()
        final_conclusions = self.__model.get_final_conclusions()
        for conclusion in final_conclusions:
            self.__ui.final_conclusions.addItem(conclusion)

    def __fill_intermediate_conclusions(self):
        self.__ui.intermediate_conclusions.clear()
        intermediate_conclusions = self.__model.get_intermediate_conclusions()
        for intermediate_conclusion in intermediate_conclusions:
            self.__ui.intermediate_conclusions.addItem(intermediate_conclusion)

    def __fill_labels(self):
        labels = self.__model.get_labels()
        self.__ui.labels.clear()
        for label in labels:
            self.__ui.labels.addItem(label)
