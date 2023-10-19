from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector

connection=mysql.connector.connect(
    host='localhost', port='3307', database='codecircledb', user='root', password=''
)

cursor=connection.cursor()

app=Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route("/login",methods=['GET','POST'])
def login():
    if 'loggedin' in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email,password))
        account=cursor.fetchone()


        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']

            return redirect(url_for('home'))
        else:
            error = 'Invalid email or password. Please try again.'
            return render_template('login.html', error=error)
         
    return render_template('login.html')


@app.route("/home",methods=['GET'])
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # Assuming you have a database connection and cursor defined
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE id = %s', (session['id'],))
        account = cursor.fetchone()

        # Check if the account is found in the database
        if account:
            # Pass the account information to the template
            return render_template('home.html', account=account)
        else:
            # Handle the case where the account is not found
            return render_template('error.html', message='Account not found')
    else:
        # Redirect to the login page if the user is not logged in
        return redirect(url_for('login'))

@app.route("/logout",methods=['GET'])
def logout():
    # Clear session variables
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('email', None)

    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        password = request.form['password']
        email = request.form['email']

        cursor.execute("INSERT INTO users (firstname, lastname, password, email) VALUES (%s, %s, %s, %s)",
                       (firstname, lastname, password, email))
        connection.commit()
        flash('Registration successful', 'success')
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)