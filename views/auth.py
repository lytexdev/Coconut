from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from config import Config
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == Config.USERNAME and bcrypt.checkpw(password.encode('utf-8'), Config.HASHED_PASSWORD.encode('utf-8')):
            session['logged_in'] = True
            return redirect(url_for('main.index'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('auth.login'))
