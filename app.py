from flask import Flask, render_template, request, redirect, session
from database import get_db

app = Flask(__name__)
app.secret_key = "veridia_secret"

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    
 
 ## Register Route
    
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        db.commit()
        return redirect('/login')
    return render_template('register.html')

## Login Route

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )
        user = cursor.fetchone()

        if user:
            session['user_id'] = user['id']
            return redirect('/dashboard')

    return render_template('login.html')

## Apply Route

@app.route('/apply', methods=['GET','POST'])
def apply():
    if request.method == 'POST':
        role = request.form['role']
        skills = request.form['skills']
        experience = request.form['experience']

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO applications (user_id,role,skills,experience) VALUES (%s,%s,%s,%s)",
            (session['user_id'],role,skills,experience)
        )
        db.commit()
        return redirect('/dashboard')

    return render_template('apply.html')


## Dashboard Route

@app.route('/dashboard')
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM applications WHERE user_id=%s",
        (session['user_id'],)
    )
    apps = cursor.fetchall()
    return render_template('dashboard.html', apps=apps)

## Admin Panel
## Admin Login

@app.route('/admin')
def admin():
    return render_template('admin_login.html')

## Admin Dashboard

@app.route('/admin/dashboard')
def admin_dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM applications")
    apps = cursor.fetchall()
    return render_template('admin_dashboard.html', apps=apps)


## Send Email

import smtplib
from email.message import EmailMessage

def send_email(to, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = "chandhu192002@gmail.com"
    msg['To'] = to

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login("chandhu192002@gmail.com","root")
        smtp.send_message(msg)
