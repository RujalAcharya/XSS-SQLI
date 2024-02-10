from flask import Flask, request, render_template
import sqlite3
from random import randint

app = Flask(__name__)

# Initialize SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')
conn.commit()

pwd = randint(100000, 500000)

# Insert sample data
c.execute(f"INSERT INTO users (username, password) VALUES ('admin', '{pwd}')")
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sqli')
def sqli():
    return render_template('index_sqli.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Vulnerable SQL query (no input validation or parameterization)
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return f"Welcome, {username}!"
    else:
        return "Invalid username or password."
    
@app.route('/xss')
def xss():
    return render_template('xss.html')

if __name__ == '__main__':
    app.run(debug=True)
