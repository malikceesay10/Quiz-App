# quiz_logic.py

import random
from questions import questions

class QuizLogic:
    def __init__(self):
        self.score = 0
        self.qn = 0
        self.correct = 0
        random.shuffle(questions)
        self.questions = questions

    def get_current_question(self):
        return self.questions[self.qn]

    def check_answer(self, selected_option):
        q = self.get_current_question()
        is_correct = (q["optionen"][selected_option] == q["antwort"])
        if is_correct:
            self.correct += 1
        return is_correct

    def next_question(self):
        self.qn += 1
        return self.qn < len(self.questions)

    def get_score(self):
        return self.correct, len(self.questions)

    def reset(self):
        self.score = 0
        self.qn = 0
        self.correct = 0
        random.shuffle(self.questions)
