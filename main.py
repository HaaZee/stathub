from flask_bcrypt import Bcrypt
from flask_admin import Admin
import os
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from fortnite_life import get_solo_stats, get_duo_stats, get_squad_stats, get_lifetime_stats
from fortnite_8 import get_8_solo_stats, get_8_duo_stats, get_8_squad_stats
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['TOKEN']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
admin = Admin(app)
settings_folder = os.path.join('static', 'settings')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already used. Try signing in instead!')

class SearchForm(FlaskForm):
    username = StringField('Username')
    submit = SubmitField('Search')

class ResetUsername(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm Changes')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ROUTES
@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate():
        name = search_form.username.data
        return redirect(url_for('stats', name=name))
    return render_template('home.html', title="StatHub", search_form=search_form)

@app.route('/stats/life/<name>')
def stats(name):
    try:
        if name == current_user.username:
            isown = True
        else:
            isown = False
    except:
        isown = False
    solo_stats = get_solo_stats(name, 'kbm')
    duo_stats = get_duo_stats(name, 'kbm')
    squad_stats = get_squad_stats(name, 'kbm')
    lifetime_kd = get_lifetime_stats(name, 'kbm')
    if not solo_stats:
        flash('Username not found.', 'danger')
    else:
        return render_template('stats_life.html', title="{} - Fortnite Player Stats -".format(name), name=name, isown=isown, solo_stats=solo_stats, duo_stats=duo_stats, squad_stats=squad_stats, lifetime_kd=lifetime_kd)
    return redirect(url_for('index'))

@app.route('/stats/8/<name>')
def stats_8(name):
    try:
        if name == current_user.username:
            isown = True
        else:
            isown = False
    except:
        isown = False
    solo_stats = get_8_solo_stats(name, 'kbm')
    duo_stats = get_8_duo_stats(name, 'kbm')
    squad_stats = get_8_squad_stats(name, 'kbm')
    if not solo_stats:
        flash('Player has no stats for season 8.', 'danger')
    else:
        return render_template('stats_8.html', title="{} - Fortnite Player Stats -".format(name), name=name, isown=isown, solo_stats=solo_stats, duo_stats=duo_stats, squad_stats=squad_stats)
    return redirect(url_for('stats', name=name))

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
    if form.validate():
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
    if form.validate():
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

@app.route("/support", methods=['GET', 'POST'])
@login_required
def support():
    form = ResetUsername()
    if form.validate():
        if form.username.data != current_user.username:
            user = User.query.filter_by(email=current_user.email).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                user.username = form.username.data
                db.session.commit()
                flash('The linked Epic Games name has been changed.', 'success')
                return redirect(url_for('stats', name=current_user.username))
            else:
                flash('Password incorrect. The linked Epic Games name has not been changed.', 'danger')
                return redirect(url_for('support'))
        else:
            flash('Username equal to current username. The linked Epic Games name has not been changed.', 'danger')
            return redirect(url_for('support'))

    return render_template('support.html', title='StatHub Support', form=form)

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


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))
