import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

# Database connection
def get_db_connection():
  conn = sqlite3.connect('users.db')  # Connect to the database
  conn.row_factory = sqlite3.Row  # To return rows as dictionaries
  return conn

# Function to close database connection
def close_db(conn):
  conn.close()

# Create the database table if it doesn't exist
def create_database_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE,
            role TEXT DEFAULT 'user',
            profile_image_url TEXT,
            first_name TEXT,
            last_name TEXT,
            bio TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  conn = get_db_connection()
  error = None
  if request.method == 'POST':
    email = request.form['email']
    password = request.form['password']
    user = conn.execute(
      'SELECT * FROM users WHERE email = ?', (email,)
    ).fetchone()

    if user is None:
      error = 'Incorrect email or password.'
    elif not check_password_hash(user['password'], password):
      error = 'Incorrect email or password.'
    else:
      session['logged_in'] = True
      session['user_id'] = user['id']
      conn.execute(
        'UPDATE users SET last_login_at = CURRENT_TIMESTAMP WHERE id = ?', (user['id'],)
      )
      conn.commit()
      return redirect(url_for('profile'))

  conn.close()
  return render_template('login.html', error=error)

# Route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  conn = get_db_connection()
  error = None
  if request.method == 'POST':
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    password_confirm = request.form['password_confirm']

    if not username or not email or not password:
      error = 'Please fill in all fields.'
    elif password != password_confirm:
      error = 'Passwords do not match.'
    elif conn.execute(
      'SELECT id FROM users WHERE username = ?', (username,)
    ).fetchone() is not None:
      error = 'Username already exists.'
    elif conn.execute(
      'SELECT id FROM users WHERE email = ?', (email,)
    ).fetchone() is not None:
      error = 'Email already exists.'
    else:
      hashed_password = generate_password_hash(password)
      conn.execute(
        'INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
        (username, hashed_password, email)
      )
      conn.commit()
      return redirect(url_for('login'))

  conn.close()
  return render_template('signup.html', error=error)

# Route for the user profile page
@app.route('/profile')
def profile():
  if 'logged_in' in session:
    conn = get_db_connection()
    user_id = session['user_id']
    user = conn.execute(
      'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return render_template('profile.html', user=user)
  else:
    return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
  session.pop('logged_in', None)
  session.pop('user_id', None)
  return redirect(url_for('login'))

if __name__ == '__main__':
  create_database_table()  # Create the database table before running the app
  app.run(debug=True)