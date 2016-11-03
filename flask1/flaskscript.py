from flask_script import Manager
from flask import Flask
app = Flask(__name__)

manager = Manager(app)

@app.route('/')
def index():
    return '<h1>hello world</h1>'

if __name__ == '__main__':
    manager.run()

