from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app=Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators = [Required()])
    submit = SubmitField('Submit')

@app.route('/', methods= ['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template("index111.html", form = form, name = name)









if __name__== "__main__":
    app.run()

