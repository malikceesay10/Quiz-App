from flask import Flask, render_template, request, redirect, url_for
from quiz_logic import QuizLogic

app = Flask(__name__)
quiz = QuizLogic()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    quiz.reset()
    return redirect(url_for('question'))

@app.route('/question')
def question():
    if quiz.qn >= len(quiz.questions):
        return redirect(url_for('result'))
    q = quiz.get_current_question()
    return render_template('question.html', question=q, qn=quiz.qn + 1, total=len(quiz.questions), enumerate=enumerate)

@app.route('/answer', methods=['POST'])
def answer():
    selected_option = int(request.form['option'])
    is_correct = quiz.check_answer(selected_option)
    quiz.next_question()
    return render_template('answer.html', is_correct=is_correct, selected_option=selected_option, question=quiz.get_current_question(), qn=quiz.qn, total=len(quiz.questions))

@app.route('/result')
def result():
    correct, total = quiz.get_score()
    percentage = (correct / total) * 100
    return render_template('result.html', correct=correct, total=total, percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True)