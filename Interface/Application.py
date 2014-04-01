from PySide.QtGui import QApplication
from PySide.QtCore import QFile
from PySide import QtUiTools
from PySide import QtGui
from PySide.QtCore import QTranslator, QObject

from Logic import ExpertSystem, Facts, Rules

import sys
import os.path
import locale


class Application(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.__translator = QTranslator()
        self.__rules = Rules.Rules()
        self.__facts = Facts.Facts()
        self.expert = ExpertSystem.Expert(self.__rules, self.__facts)
        self.__ui = None
        self.current_question = None
        self.__finished = False

        self.__rules.add_rule(Rules.Rule("Z", ["R"]))
        self.__rules.add_rule(Rules.Rule("C", ["A", "B"]))
        self.__rules.add_rule(Rules.Rule("E", ["C", "D", "F"]))
        self.__rules.add_rule(Rules.Rule("D", ["C"]))

        self.__app = QApplication(sys.argv)

        self.__setup_language()
        self.__init_ui()

        self.reset()

    def __setup_language(self):
        system_locale, _ = locale.getdefaultlocale()
        search_folder = os.path.dirname(__file__)
        search_folder = os.path.join(search_folder, "..", "translations")
        self.__translator.load(system_locale, search_folder)
        self.__app.installTranslator(self.__translator)

    def __init_ui(self):
        self.__load_ui()
        self.__setup_slots()

    def __load_ui(self):
        ui_path = os.path.dirname(__file__)
        ui_path = os.path.join(ui_path, "MainWindow.ui")
        ui_file = QFile(ui_path)
        ui_file.open(QFile.ReadOnly)
        ui_loader = QtUiTools.QUiLoader()
        self.__ui = ui_loader.load(ui_file, None)
        ui_file.close()

        self.__ui.answerTableWidget.setHorizontalHeaderLabels([self.tr("Question"), self.tr("Answer")])

    def __setup_slots(self):
        self.__ui.answer.button(QtGui.QDialogButtonBox.Yes).clicked.connect(self.slot_answer_clicked_yes)
        self.__ui.answer.button(QtGui.QDialogButtonBox.No).clicked.connect(self.slot_answer_clicked_no)
        self.__ui.actionNew.triggered.connect(self.reset)
        self.__ui.actionLoadRules.triggered.connect(self.load_rules)

    def slot_answer_clicked_yes(self):
        self.slot_answer_clicked(True)

    def slot_answer_clicked_no(self):
        self.slot_answer_clicked(False)

    def slot_answer_clicked(self, answer):
        self.__facts.set_fact_value(self.current_question, answer)
        self.add_answer_to_list(self.current_question, answer)

        conclusion_rule = self.expert.infer_forward()
        conclusion_text = self.tr("Can't conclude")
        if conclusion_rule is not None and self.__rules.is_terminal_rule(conclusion_rule):
            conclusion_text = conclusion_rule.conclusion
            self.finished()
        self.__ui.conclusionLabel.setText(conclusion_text)

        self.next_answer()

    def add_answer_to_list(self, question, answer):
        count = self.__ui.answerTableWidget.rowCount()
        self.__ui.answerTableWidget.setRowCount(count + 1)
        self.__ui.answerTableWidget.setItem(count, 0, QtGui.QTableWidgetItem(question))
        answer_text = self.tr("Yes") if answer else self.tr("No")
        self.__ui.answerTableWidget.setItem(count, 1, QtGui.QTableWidgetItem(answer_text))

    def reset(self):
        self.__facts.reset()
        self.__ui.answer.setEnabled(True)
        self.__ui.answerTableWidget.setRowCount(0)
        self.__ui.conclusionLabel.setText(self.tr("Can't conclude"))
        self.__finished = False
        self.next_answer()

    def run(self):
        self.__ui.show()
        self.__app.exec_()

    def next_answer(self):
        question = self.expert.infer_backward()
        if question is not None and not self.__finished:
            self.current_question = question
        else:
            question = None
            self.finished()
        question = self.tr("No more questions!") if question is None else question
        self.__ui.questionLabel.setText(question)

    def finished(self):
        self.__ui.answer.setEnabled(False)
        self.__finished = True

    def load_rules(self):
        file_path, file_filter = QtGui.QFileDialog.getOpenFileName(self.__ui, self.tr("Select rules file"), "",
                                                                   self.tr("Rules file") + " (*.rules);;")
        if file_path != "" and file_filter != "":
            pass


if __name__ == "__main__":
    application = Application()
    application.run()
