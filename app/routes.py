import os
import requests
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from app import app, bcrypt, db
from app.models import User
from app.forms import LoginForm, RegisterForm, SearchForm
from app.fortnite import get_solo_stats, get_duo_stats, get_squad_stats

settings_folder = os.path.join('static', 'settings')


# ROUTES
@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        name = search_form.username.data
        return redirect(url_for('stats', name=name))
    return render_template('home.html', title="StatHub", search_form=search_form)

@app.route('/stats/<name>')
def stats(name):
    try:
        if name == current_user.username:
            isown = True
        else:
            isown = False
    except:
        isown = False
    solo_stats = get_solo_stats(name, 'pc')
    duo_stats = get_duo_stats(name, 'pc')
    squad_stats = get_squad_stats(name, 'pc')
    lifetime_stats = get_lifetime_stats(name, 'pc')
    if not solo_stats:
        flash('Username not found.', 'danger')
    else:
        return render_template('stats.html', title="{} - Fortnite Player Stats -".format(name), name=name, isown=isown, solo_stats=solo_stats, duo_stats=duo_stats, squad_stats=squad_stats, lifetime_stats=lifetime_stats)
    return redirect(url_for('index'))

@app.route('/guide')
def guide():
    return render_template('guide.html', title="Guide")

@app.route('/about')
def about():
    return render_template('about.html', title="About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now logged in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form, title="Login")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/support")
@login_required
def support():
    return render_template('support.html', title='StatHub Support')

@app.route("/account")
@login_required
def account():
    name = current_user.username
    return redirect(url_for('stats', name=name))


# UPDATE CSS
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
