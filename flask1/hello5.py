from flask_sqlalchemy import SQLAlchemy
import os
from flask_wtf import FlaskForm
from flask import Flask, render_template,session, redirect, url_for
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask_script import Manager,Shell



basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///'+ os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True


manager = Manager(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    def __repr__(self):
        return '<Role %r>' % self.name
    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique =True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username




class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [Required()])
    submit = SubmitField('Submit')


@app.route('/', methods= ['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known']= False
        else:
            session['known']=True
        session['name']= form.name.data
        return redirect(url_for('index'))
    return render_template('index5.html',form=form, name=session.get('name'),
                           known = session.get('known',False))


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)
manager.add_command("shell", Shell(make_context=make_shell_context))




if __name__== "__main__":
    manager.run()

