from flask import render_template, flash, redirect, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from infrastructure import app, lm, db
from forms import LoginForm, RegistrationForm
from models import User, Token, Match
import models



class IndexSijaxHandler(object):

    @staticmethod
    def save_word(obj_response, *data):
        row = """
        <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        </tr>
        """ % (current_user._get_current_object().name, data[0], data[2])

        models.add_word_and_translation(*data)

        obj_response.html_prepend('.table tbody', row)



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    if g.sijax.is_sijax_request:
        g.sijax.register_object(IndexSijaxHandler)
        return g.sijax.process_request()

    words = Match.query.join(Match.word).filter(Token.lang=='en').order_by(Match.review_time.desc()).all()
    return render_template('index.html', title='My words', words=words, \
    lang=models.languages)


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

