from flask_bootstrap import Bootstrap
from flask import Flask , render_template
app=Flask(__name__)


bootstrap = Bootstrap(app)

@app.route('/user/<name>')
def user(name):
    name = "handsome         " + str(name)
    return render_template("user1.html",name = name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__== "__main__":
    app.run()