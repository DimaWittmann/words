from flask import render_template, flash, redirect, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from infrastructure import app, lm, db
from forms import LoginForm, RegistrationForm
from models import User, Token, Match
import models


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='My words', lang=models.languages)


@app.route('/load_words')
def load_words():
    result = []
    words = Match.query.join(Match.word).filter(Token.lang=='en').order_by(Match.review_time.desc()).all()
    for w in words:
        #result.append({'user':w.user.name, 'word':w.word.text, 'translation': w.translation.text})
        result.append([w.user.name, w.word.text, w.translation.text])

    return jsonify(data=result)


@app.route('/save_word')
def save_word():
    word = request.args.get('word', '', type=str)
    word_lang = request.args.get('word_lang', '', type=str)
    trans= request.args.get('trans', '', type=str)
    trans_lang= request.args.get('trans_lang', '', type=str)

    models.add_word_and_translation(word, word_lang, trans, trans_lang)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    form_login = LoginForm()
    form_registration = RegistrationForm()

    if form_login.validate_on_submit():
        user = User.query.filter_by(name=form_login.login.data).first()
        if user is None:
            flash('Invalid login')
        elif user.verify_password(form_login.password.data):
            login_user(user, form_login.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Invalid password')

    if form_registration.validate_on_submit():
        user = User(
            email=form_registration.email.data,
            name=form_registration.login.data,
            password=form_registration.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return render_template('login.html', title='Hello!', form_login=form_login, form_registration=form_registration)

    return render_template('login.html', title='Hello!', form_login=form_login, form_registration=form_registration)


@app.route('/logout')
@login_required
def logout():
    flash('Bye!')
    logout_user()
    return redirect(url_for('index'))



@app.before_request
def before_request():
    g.user = current_user



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

