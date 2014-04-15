import sys
import os.path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from PySide.QtDeclarative import *
from PySide.QtCore import QObject, Qt
from PySide.QtGui import QApplication
from Logic.Rules import Rules, Rule
from Logic.ExpertSystem import Expert
from Logic.Facts import Facts

import tts
import sys
import os


class QmlApplication(QObject):
    def __init__(self, root, tts_module):
        QObject.__init__(self)
        self.root = root
        self.tts = tts_module
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
            content = self.tr("I conclude that:\n %s") % answer.conclusion
            self.set_dialog_text(content)
            self.tts.speak(content)
        else:
            self.next_question()

    def set_dialog_text(self, question):
        self.root.setProperty("dialogText", question)

    def next_question(self):
        question = self.expert.infer_backward()
        self.current_question = question
        if question is None:
            content = self.tr("Can't conclude!")
            self.set_dialog_text(content)
            self.set_finished_state(True)
            self.tts.speak(content)
        else:
            self.set_dialog_text(question)
            self.tts.speak(question)

    def set_finished_state(self, finished):
        self.root.setProperty("finished", finished)

    def reset(self):
        self.facts.reset()
        self.set_finished_state(False)
        self.next_question()


tts_module = tts.tts("en")
app = QApplication(sys.argv)
view = QDeclarativeView()
view.rootContext().setContextProperty("mainWindow", view)

view.setWindowFlags(Qt.FramelessWindowHint)
view.setSource(os.path.join(os.path.dirname(__file__), "QML_Interface.qml"))
root = view.rootObject()
view.engine().quit.connect(view.close)

view.show()

logic = QmlApplication(root, tts_module)

sys.exit(app.exec_())