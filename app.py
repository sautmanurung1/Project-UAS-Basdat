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
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)