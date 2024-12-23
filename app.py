from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deine-geheime-schluessel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)


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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)