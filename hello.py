from flask import Flask, session, redirect, url_for, escape, request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80),unique=False)

    def __init__(self, email, password):
        self.username = email
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

@app.route("/")
def welcome():
    if 'username' in session:
        return redirect(url_for('search'))
    return render_template('welcome.html')

@app.route("/search")
def search():
	return render_template('search.html')

@app.route("/Profiles")
def Profiles():
	return render_template('Profiles')

@app.route("/Amanage")
def Amanage():
	return render_template('Amanage')

@app.route("/History")
def History():
	return render_template('History')

@app.route("/profile")
def profile():
	if 'username' in session:
		return render_template('profile.html')
	return redirect(url_for('welcome'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':       
        if User.query.filter_by(username=request.form['username']).first() is None:
            db.session.add(User(request.form['username'],request.form['password']))
            db.session.commit()
            session['username'] = request.form['username']
            return redirect(url_for('search'))
        else:
            return render_template('welcome')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if str((User.query.filter_by(username=request.form['username']).first()).password) == request.form['password']:
            session['username'] = request.form['username']
            return redirect(url_for('search'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('welcome'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
    app.run()
