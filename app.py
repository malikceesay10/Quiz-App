<<<<<<< HEAD
import tkinter as tk
import random

questions = [
    {
        "frage": "Welche Programmiersprache wird häufig für Data Science verwendet?",
        "optionen": ["Java", "Python", "C#", "Ruby"],
        "antwort": "Python"
    },
    {
        "frage": "Was ist GitHub?",
        "optionen": ["Ein Betriebssystem", "Ein Texteditor", "Ein Code-Hosting-Dienst", "Eine Programmiersprache"],
        "antwort": "Ein Code-Hosting-Dienst"
    },
    {
        "frage": "Was bedeutet HTML?",
        "optionen": ["High Tech Markup Language", "Hyper Text Markup Language", "Home Tool Markup Language", "Hyperlinks Text Memory Language"],
        "antwort": "Hyper Text Markup Language"
    },
    {
        "frage": "Welches ist kein SQL Join?",
        "optionen": ["INNER JOIN", "LEFT JOIN", "CENTER JOIN", "FULL JOIN"],
        "antwort": "CENTER JOIN"
    }
]

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Quiz Anwendung")
        self.score = 0
        self.qn = 0
        self.correct = 0
        self.time_left = 10
        random.shuffle(questions)
        self.questions = questions
        self.create_start_screen()

    def create_start_screen(self):
        # Create and pack start frame
        self.start_frame = tk.Frame(self.master)
        self.start_frame.pack(expand=True, fill='both', pady=50)
        
        # Title
        title = tk.Label(self.start_frame, 
                        text="Wirtschaftsinformatik Quiz", 
                        font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Welcome message
        msg = tk.Label(self.start_frame,
                      text="Testen Sie Ihr Wissen!\n\nBeantworten Sie Multiple-Choice Fragen\ninnerhalb von 10 Sekunden.",
                      font=("Arial", 14),
                      justify="center")
        msg.pack(pady=30)
        
        # Start button
        start_btn = tk.Button(self.start_frame,
                             text="Quiz Starten",
                             command=self.start_quiz,
                             font=("Arial", 14, "bold"),
                             width=15,
                             height=2)
        start_btn.pack(pady=30)

    def start_quiz(self):
        # Hide start screen
        self.start_frame.destroy()
        
        # Create quiz widgets
        self.create_widgets()
        self.display_question()
        self.start_timer()

    def create_widgets(self):
        # Timer label
        self.timer_label = tk.Label(self.master, text="Zeit: 10", font=("Arial", 12))
        self.timer_label.pack(pady=5)

        # Question label
        self.question_label = tk.Label(self.master, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)
        
        # Frame for 2x2 grid
        self.options_frame = tk.Frame(self.master)
        self.options_frame.pack(pady=10)
        
        self.var = tk.IntVar()
        self.options = []
        
        # Create 2x2 grid of options
        for i in range(4):
            row = i // 2
            col = i % 2
            rb = tk.Radiobutton(self.options_frame, text="", variable=self.var, value=i, font=("Arial", 12))
            rb.grid(row=row, column=col, padx=10, pady=5, sticky="w")
            self.options.append(rb)
            
        self.submit_button = tk.Button(self.master, text="Antworten", command=self.check_answer)
        self.submit_button.pack(pady=20)
        
        self.result_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.result_label.pack()

        # Create frame for next button (right-aligned)
        self.next_button_frame = tk.Frame(self.master)
        self.next_button_frame.pack(fill='x', padx=20)
        
        # Next question button (initially hidden)
        self.next_button = tk.Button(self.next_button_frame, 
                                   text="Nächste Frage", 
                                   command=self.next_question,
                                   font=("Arial", 12))
        self.next_button.pack(side='right', pady=10)
        self.next_button.pack_forget()  # Hide initially

    def start_timer(self):
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.timer_label.config(text=f"Zeit: {self.time_left}")
            self.time_left -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.check_answer(timeout=True)

    def display_question(self):
        self.time_left = 10
        q = self.questions[self.qn]
        self.question_label.config(text=q["frage"])
        self.var.set(-1)
        for idx, option in enumerate(q["optionen"]):
            self.options[idx].config(text=option, fg="black", selectcolor="white")
        self.result_label.config(text="")

    def check_answer(self, timeout=False):
        if timeout:
            self.result_label.config(text="Zeit abgelaufen!", fg="red")
            self.highlight_correct_answer()
        else:
            selected = self.var.get()
            if selected == -1:
                self.result_label.config(text="Bitte wählen Sie eine Antwort aus.")
                return
            
            q = self.questions[self.qn]
            if q["optionen"][selected] == q["antwort"]:
                self.correct += 1
                self.result_label.config(text="Richtig!", fg="green")
                self.options[selected].config(fg="green")
            else:
                self.result_label.config(text=f"Falsch!", fg="red")
                self.options[selected].config(fg="red")
                self.highlight_correct_answer()

        # Show next button instead of auto-advancing
        if self.qn < len(self.questions) - 1:  # Don't show on last question
            self.next_button.pack(side='right', pady=10)
        self.submit_button.config(state='disabled')  # Disable answer button

    def highlight_correct_answer(self):
        q = self.questions[self.qn]
        correct_idx = q["optionen"].index(q["antwort"])
        self.options[correct_idx].config(fg="green")

    def next_question(self):
        self.qn += 1
        if self.qn < len(self.questions):
            self.next_button.pack_forget()  # Hide next button
            self.submit_button.config(state='normal')  # Re-enable answer button
            self.display_question()
        else:
            self.show_score()

    def show_score(self):
        self.timer_label.pack_forget()
        self.question_label.config(text=f"Quiz beendet! Sie haben {self.correct} von {len(self.questions)} Fragen richtig beantwortet.")
        self.options_frame.pack_forget()
        self.submit_button.pack_forget()

def main():
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
=======
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deine-geheime-schluessel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)


def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)  
    wrong_answer1 = db.Column(db.String(200), nullable=False)
    wrong_answer2 = db.Column(db.String(200), nullable=False)
    wrong_answer3 = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    answers = db.Column(db.Text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            session.permanent = True
            session['username'] = user.username
            return redirect(url_for('index'))
        flash('Ungültige Anmeldedaten')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        if User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben')
            return redirect(url_for('register'))
        
        if request.form.get('password') != request.form.get('password2'):
            flash('Passwörter stimmen nicht überein')
            return redirect(url_for('register'))

        user = User(
            username=username,
            firstname=request.form.get('firstname'),
            lastname=request.form.get('lastname')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()

        session.permanent = True
        session['username'] = username
        return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    if 'username' in session:
        user = get_current_user()
        return render_template('dashboard.html',
                            username=session['username'],
                            stats=get_user_stats(user.id),
                            top_categories=get_top_categories(user.id))
    return render_template('index.html')

@app.route('/categories')
@login_required
def categories():
    return render_template('categories.html', username=session['username'])

@app.route('/quiz/start/<category>')
@login_required
def start_quiz(category):
    if category.lower() == 'zufällige fragen':
        questions = Quiz.query.order_by(db.func.random()).limit(5).all()
    else:
        questions = Quiz.query.filter_by(category=category.lower()).order_by(db.func.random()).limit(5).all()

    if not questions:
        flash('Keine Fragen verfügbar für diese Kategorie')
        return redirect(url_for('categories'))

    session['quiz'] = {
        'questions': [q.id for q in questions],
        'current': 0,
        'correct': 0,
        'answers': [],
        'category': category
    }
    return redirect(url_for('show_question'))

@app.route('/quiz/question', methods=['GET', 'POST'])
@login_required
def show_question():
    quiz_data = session['quiz']
    if quiz_data['current'] >= len(quiz_data['questions']):
        return redirect(url_for('quiz_result'))
    
    question = Quiz.query.get(quiz_data['questions'][quiz_data['current']])
    answers = [
        question.correct_answer,
        question.wrong_answer1,
        question.wrong_answer2,
        question.wrong_answer3
    ]
    random.shuffle(answers)
    
    return render_template('question.html', 
                         question=question,
                         answers=answers,
                         current=quiz_data['current'] + 1,
                         total=len(quiz_data['questions']))

@app.route('/quiz/answer', methods=['POST'])
@login_required
def submit_answer():
    quiz_data = session['quiz']
    answer = request.form.get('answer')
    question = Quiz.query.get(quiz_data['questions'][quiz_data['current']])
    
    quiz_data['answers'].append({
        'question': question.question,
        'user_answer': answer,
        'correct_answer': question.correct_answer,
        'is_correct': answer == question.correct_answer
    })
    
    if answer == question.correct_answer:
        quiz_data['correct'] += 1
    
    quiz_data['current'] += 1
    session['quiz'] = quiz_data

    if quiz_data['current'] >= len(quiz_data['questions']):
        return redirect(url_for('quiz_result'))
    
    return redirect(url_for('show_question'))

@app.route('/quiz/result')
@login_required
def quiz_result():
    quiz_data = session.get('quiz')
    if not quiz_data:
        return redirect(url_for('categories'))
    
    score = quiz_data['correct']
    total = len(quiz_data['questions'])
    answers = quiz_data['answers']
    category = quiz_data.get('category', 'unbekannt')
    
    user = get_current_user()
    if user is None:
        return redirect(url_for('login'))
    
    result = QuizResult(
        user_id=user.id, 
        score=score, 
        category=category,
        answers=json.dumps(answers)
    )
    db.session.add(result)
    db.session.commit()
    
    session.pop('quiz', None)
    
    return render_template('quiz_result.html', 
                         score=score, 
                         total=total,
                         answers=answers)

@app.route('/result/<int:result_id>')
@login_required
def show_result(result_id):
    result = QuizResult.query.get_or_404(result_id)
    user = get_current_user()
    
    if result.user_id != user.id:
        flash('Zugriff verweigert')
        return redirect(url_for('index'))
        
    answers = json.loads(result.answers) if result.answers else []
    
    return render_template('quiz_result.html',
                         score=result.score,
                         total=len(answers),
                         answers=answers)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
>>>>>>> 0fcb6e1f7eec7c0758390872c06ffb988ac04703
