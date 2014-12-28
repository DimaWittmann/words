from infrastructure import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, current_user
from hashlib import md5
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView
import datetime

languages = ["en", "uk", "de"]

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                    )

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(24), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    _password_hash = db.Column(db.String(124))

    #inherit this fields
    record = db.relationship("Match", backref="user")
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

    @property
    def password(self):
        raise AttributeError()

    @password.setter
    def password(self, password):
        self._password_hash = generate_password_hash(password)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' \
        + md5(self.email.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)

    def verify_password(self, password):
        return check_password_hash(self._password_hash, password)
    def __repr__(self):
        return '<User %r>' % (self.name)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0


class Token(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, index = True)
    lang = db.Column(db.Enum(*languages), default=languages[0])


    def __repr__(self):
        return '<Token %r %r>' % (self.lang, self.text)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    word_id = db.Column(db.Integer, db.ForeignKey('token.id'))
    word = db.relationship("Token", foreign_keys=[word_id])

    translation_id = db.Column(db.Integer, db.ForeignKey('token.id'))
    translation = db.relationship("Token", foreign_keys=[translation_id])

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    creation_time = db.Column(db.DateTime)
    review_time = db.Column(db.DateTime)

    level = db.Column(db.Integer, default=-2)

    description = db.Column(db.Text)



def add_word_and_translation(word, word_lang, translation, tran_lang):

    token1 = Token.query.filter_by(text=word, lang=word_lang).first()
    if not token1:
        token1 = Token(text=word, lang=word_lang)

    token2 = Token.query.filter_by(text=word, lang=word_lang).first()
    if not token2:
        token2 = Token(text=translation, lang=tran_lang)

    match = Match(word=token1, translation=token2, user=current_user._get_current_object(),\
                  creation_time=datetime.datetime.now(), review_time=datetime.datetime.now())

    db.session.add(token1)
    db.session.add(token2)
    db.session.add(match)

    db.session.commit()


admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Token, db.session))
admin.add_view(ModelView(Match, db.session))