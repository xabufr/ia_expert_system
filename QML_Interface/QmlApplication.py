from PySide.QtDeclarative import *
from PyQt4.QtCore import QObject, Qt
from PySide.QtGui import QApplication
from Logic.Rules import Rules, Rule
from Logic.ExpertSystem import Expert
from Logic.Facts import Facts

import sys
import os


class QmlApplication(QObject):
    def __init__(self, root):
        QObject.__init__(self)
        self.root = root
        self.rules = Rules()
        self.facts = Facts()
        self.current_question = None
        self.rules.add_rule(Rule("Z", ["R"]))
        self.rules.add_rule(Rule("C", ["A", "B"]))
        self.rules.add_rule(Rule("E", ["C", "D", "F"]))
        self.rules.add_rule(Rule("D", ["C"]))

        self.expert = Expert(self.rules, self.facts)
        self.root.answerYes.connect(lambda: self.answer(True))
        self.root.answerNo.connect(lambda: self.answer(False))
        self.root.restartProcess.connect(self.reset)

        self.next_question()

    def answer(self, answer):
        self.facts.set_fact_value(self.current_question, answer)
        answer = self.expert.infer_forward()

        if answer is not None and self.rules.is_terminal_rule(answer):
            self.set_finished_state(True)
            self.set_dialog_text(answer.conclusion)
        else:
            self.next_question()

    def set_dialog_text(self, question):
        self.root.setProperty("dialogText", question)

    def next_question(self):
        question = self.expert.infer_backward()
        self.current_question = question
        if question is None:
            self.set_dialog_text(self.tr("Can't conclude!"))
            self.set_finished_state(True)
        else:
            self.set_dialog_text(question)

    def set_finished_state(self, finished):
        self.root.setProperty("finished", finished)

    def reset(self):
        self.facts.reset()
        self.set_finished_state(False)
        self.next_question()


app = QApplication(sys.argv)
view = QDeclarativeView()

view.setWindowFlags(Qt.FramelessWindowHint)
view.setSource(os.path.join(os.path.dirname(__file__), "QML_Interface.qml"))
root = view.rootObject()
view.engine().quit.connect(view.close)

view.show()

logic = QmlApplication(root)


sys.exit(app.exec_())