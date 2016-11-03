# -*- coding:utf-8 -*-
from flask import Flask , flash , render_template , request
app=Flask(__name__)
app.secret_key = '123'

@app.route('/')
def hello_user():
    flash("Welcomt to China")
    return render_template("index11.html")



@app.route('/login', methods = ['POST'])
def login():
    form = request.form
    username = form.get('username')
    password = form.get('password')
    if not username:
        flash('please input username')
        return render_template("index11.html")
    if not password:
        flash("please input password")
        return render_template("index11.html")

    if username == "zhangwenjie" and password == "iamcool":
        flash("login success")
        return render_template("index11.html")
    else:
        flash("username or password is wrong")
        return render_template("index11.html")


if __name__== "__main__":
    app.run()