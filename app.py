from flask import Flask, render_template, url_for, redirect, request
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import MySQLdb.cursors
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sautmanurung234'
app.config['MYSQL_DB'] = 'booking-app-database'

mysql = MySQL(app)

@app.route('/')
def dashboard():
    return 'Hello Guys'

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['email'] = users['email']
            msg = 'Logged in Successfully !'
            return render_template('index.html', msg = msg)
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)