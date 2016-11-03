# -*- coding:utf-8 -*-
# 消息提示+异常处理
from flask import Flask , flash , render_template , request

app=Flask(__name__)
app.secret_key = '123'
# secret 是用来对flash进行加密的





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
        flash("username of password is wrong")
        return render_template("index11.html")






@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>'% name

if __name__== "__main__":
    app.run(debug=True)
