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
    

@app.route('/')
def index():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session.permanent = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Ungültige Anmeldedaten')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        firstname = request.form.get('firstname') 
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if User.query.filter_by(username=username).first():
            flash('Benutzername bereits vergeben')
            return redirect(url_for('register'))
            
        if password != password2:
            flash('Passwörter stimmen nicht überein')
            return redirect(url_for('register'))

        user = User(username=username, firstname=firstname, lastname=lastname)
        user.set_password(password)
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)