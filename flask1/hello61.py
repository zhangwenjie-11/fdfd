from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from flask import Flask, render_template,session, redirect, url_for
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_script import Manager,Shell
from flask_mail import Mail,Message
from threading import Thread



basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = '13062526057<13062526057@163.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')


manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
mail = Mail(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [Required()])
    submit = SubmitField('Submit')


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] +subject,
                sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body=render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr=Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                 send_email(app.config['FLASKY_ADMIN'], 'New User',
                            'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data=''
        return redirect(url_for('index'))
    return render_template('index5.html', form=form, name=session.get('name'),
                             known=session.get('known', False))


if __name__ == '__main__':
    manager.run()