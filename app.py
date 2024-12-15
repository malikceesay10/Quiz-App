from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'deine-geheime-schluessel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.permanent_session_lifetime = timedelta(days=7)
db = SQLAlchemy(app)