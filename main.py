from app import app
from db_config import mysql
from flask import Flask, render_template, url_for, redirect, request,session
from werkzeug.security import check_password_hash, generate_password_hash
import MySQLdb.cursors
import re
import datetime as dt

@app.route('/')
def dashboard():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, ))
        users = cursor.fetchone()
        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['email'] = users['email']
            msg = 'Logged in Successfully !'
            return render_template('home.html', msg = msg)
        elif not check_password_hash(users['password'], password):
            msg = 'Incorrect Password'
        else:
            msg = 'Incorrect email / password !'
    return render_template('login.html', msg = msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'first_name' in request.form and 'last_name' in request.form and 'email' in request.form and 'password' in request.form and 'phone' in request.form:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        phone_number = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, ))
        users = cursor.fetchone()
        if users:
            msg = 'Account already exist !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not email or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, 2)', (first_name, last_name, email, generate_password_hash(password), phone_number, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/room-list')
def room_list():
    return render_template('room_list.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        bookingDetails = request.form
        roomtype = bookingDetails['room_class']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        check_in_format = dt.datetime.strptime(check_in, '%Y-%m-%d')
        check_out_format = dt.datetime.strptime(check_out, '%Y-%m-%d')
        print(check_in_format)
        print(check_out_format)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO pemesanan VALUES (NULL, % s, % s, % s)', (roomtype, check_in, check_out, ))
    return render_template('booking.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)