from flask import Flask , flash , render_template , request
app=Flask(__name__)



@app.route('/')
def index(name):
    return '<h1>Hello World!</h1>'

if __name__== "__main__":
    app.run(debug=True)
