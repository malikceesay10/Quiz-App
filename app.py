from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func, desc
import random, json
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

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

def get_user_stats(user_id):
    if user_id is None:
        return {
            'total_quizzes': 0,
            'average_score': 0,
            'best_category': "Keine",
            'hardest_category': "Keine"
        }
    return {
        'total_quizzes': QuizResult.query.filter_by(user_id=user_id).count(),
        'average_score': calculate_average_score(user_id),
        'best_category': get_best_category(user_id),
        'hardest_category': get_hardest_category(user_id)
    }

def get_current_user():
    if 'username' in session:
        return User.query.filter_by(username=session['username']).first()
    return None

def get_total_quizzes(user_id):
    return QuizResult.query.filter_by(user_id=user_id).count()

def calculate_average_score(user_id):
    results = QuizResult.query.filter_by(user_id=user_id).all()
    if not results:
        return 0
    total_score = sum(result.score for result in results)
    return round((total_score / (len(results) * 5)) * 100, 1)

def get_best_category(user_id):
    results = QuizResult.query.filter_by(user_id=user_id)\
        .with_entities(QuizResult.category, db.func.avg(QuizResult.score).label('avg_score'))\
        .group_by(QuizResult.category)\
        .order_by(db.desc('avg_score'))\
        .first()
    return results.category.capitalize() if results else "Keine"

def get_hardest_category(user_id):
    results = QuizResult.query.filter_by(user_id=user_id)\
        .with_entities(QuizResult.category, db.func.avg(QuizResult.score).label('avg_score'))\
        .group_by(QuizResult.category)\
        .having(db.func.count(QuizResult.id) >= 1)\
        .order_by(db.asc('avg_score'))\
        .first()
    return results.category.capitalize() if results else "Keine"

def get_top_categories(user_id):
    categories = QuizResult.query.filter_by(user_id=user_id)\
        .with_entities(
            QuizResult.category,
            db.func.count(QuizResult.id).label('total_quizzes'),
            db.func.avg(QuizResult.score).label('avg_score')
        )\
        .group_by(QuizResult.category)\
        .order_by(db.desc('avg_score'))\
        .limit(3)\
        .all()
    
    return [
        {
            'name': cat.category.capitalize(),
            'percentage': int(round(float(cat.avg_score or 0) / 5 * 100))
        }
        for cat in categories
    ] or [{'name': 'Keine Daten', 'percentage': 0}] * 3

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
        if user is None:
            session.clear()
            return redirect(url_for('login'))
        return render_template('dashboard.html',
                            username=session['username'],
                            stats=get_user_stats(user.id),
                            top_categories=get_top_categories(user.id))
    return render_template('index.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_current_user()
    if user is None:
        session.clear()
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'update_profile' in request.form:
            new_username = request.form.get('username')
            if new_username != user.username and User.query.filter_by(username=new_username).first():
                flash('Benutzername bereits vergeben')
                return redirect(url_for('profile'))
            
            user.username = new_username
            user.firstname = request.form.get('firstname')
            user.lastname = request.form.get('lastname')
            session['username'] = new_username
            db.session.commit()
            flash('Profil erfolgreich aktualisiert')
        elif 'update_password' in request.form:
            if not user.check_password(request.form.get('old_password')):
                flash('Aktuelles Passwort ist falsch')
                return redirect(url_for('profile'))
            
            if request.form.get('new_password') != request.form.get('confirm_password'):
                flash('Neue Passwörter stimmen nicht überein')
                return redirect(url_for('profile'))

            user.set_password(request.form.get('new_password'))
            db.session.commit()
            session.clear()
            flash('Passwort erfolgreich geändert. Bitte erneut einloggen.')
            return redirect(url_for('login'))

    return render_template('profile.html', user=user, stats=get_user_stats(user.id), username=user.username)

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = get_current_user()
    if user:
        Friendship.query.filter(
            (Friendship.user_id == user.id) | (Friendship.friend_id == user.id)
        ).delete()
        
        db.session.delete(user)
        db.session.commit()
        session.clear()
        flash('Ihr Konto wurde erfolgreich gelöscht.')
        
    return redirect(url_for('login'))

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

@app.route('/all-questions')
@login_required
def all_questions_categories():
    return render_template('categories.html', username=session['username'], mode='all_questions')

@app.route('/all-questions/<category>')
@login_required
def show_category_questions(category):
    questions = Quiz.query.filter_by(category=category).all()
    return render_template('all_questions.html', 
                         username=session['username'], 
                         category=category, 
                         questions=questions)

@app.route('/question/<int:question_id>')
@login_required
def answer_single_question(question_id):
    question = Quiz.query.get_or_404(question_id)
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
                         current=1,
                         total=1,
                         single_question=True)

@app.route('/question/<int:question_id>/answer', methods=['POST'])
@login_required
def submit_single_answer(question_id):
    question = Quiz.query.get_or_404(question_id)
    answer = request.form.get('answer')
    is_correct = answer == question.correct_answer
    
    user = get_current_user()
    
    result = QuizResult(
        user_id=user.id,
        score=1 if is_correct else 0,
        category=question.category,
        answers=json.dumps([{
            'question': question.question,
            'user_answer': answer,
            'correct_answer': question.correct_answer,
            'is_correct': is_correct
        }])
    )
    
    db.session.add(result)
    db.session.commit()
    
    return render_template('quiz_result.html',
                         score=1 if is_correct else 0,
                         total=1,
                         answers=[{
                             'question': question.question,
                             'user_answer': answer,
                             'correct_answer': question.correct_answer,
                             'is_correct': is_correct
                         }],
                         single_question=True)

@app.route('/friends', methods=['GET', 'POST'])
@login_required
def friends():
    user = get_current_user()
    
    if request.method == 'POST':
        friend_username = request.form.get('friend_username')
        friend = User.query.filter_by(username=friend_username).first()
        
        if friend and friend.id != user.id:
            existing_friendship = Friendship.query.filter(
                ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
                ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
            ).first()
            
            if not existing_friendship:
                friendship = Friendship(user_id=user.id, friend_id=friend.id)
                db.session.add(friendship)
                db.session.commit()
                return redirect(url_for('friends'))
    
    friends_list = User.query.join(Friendship, 
        ((User.id == Friendship.friend_id) & (Friendship.user_id == user.id)) |
        ((User.id == Friendship.user_id) & (Friendship.friend_id == user.id))
    ).all()
    
    return render_template('friends.html', friends=friends_list, username=session['username'])

@app.route('/remove_friend', methods=['POST'])
@login_required
def remove_friend():
    user = get_current_user()
    friend_username = request.form.get('friend_username')
    friend = User.query.filter_by(username=friend_username).first()
    
    if friend and friend.id != user.id:
        friendship = Friendship.query.filter(
            ((Friendship.user_id == user.id) & (Friendship.friend_id == friend.id)) |
            ((Friendship.user_id == friend.id) & (Friendship.friend_id == user.id))
        ).first()
        
        if friendship:
            db.session.delete(friendship)
            db.session.commit()
    
    return redirect(url_for('friends'))

@app.route('/api/search_user/<username>')
@login_required
def search_user(username):
    user = User.query.filter_by(username=username).first()
    current_user = get_current_user()
    
    if user and user != current_user:
        friendship = Friendship.query.filter(
            ((Friendship.user_id == current_user.id) & (Friendship.friend_id == user.id)) |
            ((Friendship.user_id == user.id) & (Friendship.friend_id == current_user.id))
        ).first()
        
        if not friendship:
            return jsonify({
                'found': True,
                'username': user.username
            })
    
    return jsonify({'found': False})

@app.route('/api/user_profile/<username>')
@login_required
def get_user_profile(username):
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
  
    user_stats = get_user_stats(user.id)
    
    return jsonify({
        'username': user.username,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'stats': {
            'total_quizzes': user_stats['total_quizzes'],
            'average_score': user_stats['average_score'],
            'best_category': user_stats['best_category']
        }
    })

@app.context_processor
def utility_processor():
    def get_user_results():
        if 'username' in session:
            user = User.query.filter_by(username=session['username']).first()
            if user is None:
                return []
            all_results = QuizResult.query.filter_by(user_id=user.id).order_by(QuizResult.date.desc()).all()
            return [result for result in all_results if len(json.loads(result.answers)) == 5]
        return []
    return dict(get_user_results=get_user_results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)