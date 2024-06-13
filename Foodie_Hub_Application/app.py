import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///general.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_path = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    rating = db.Column(db.Float)
    # Define relationships, if any, e.g., reviews
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
with app.app_context():
    db.create_all()
 
app.config['SECRET_KEY'] = 'testing'
csrf = CSRFProtect(app)

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
@app.route('/add-restaurant', methods=['GET', 'POST'])
def addrestaurant():
    if request.method == 'POST':
        new_restaurant = {
            "name": request.form['name'],
            "description": request.form['description'],
            "rating": float(request.form['rating']),
            "image": request.form['image']
        }
        restaurants.append(new_restaurant)
        return redirect(url_for('restaurants'))
    return render_template('add-restaurant.html')


@app.route('/add_srestaurant', methods=['GET', 'POST'])
def add_restaurant():
    if request.method == 'POST':
        # Process the submitted form data
        name = request.form['name']
        description = request.form['description']
        image_path = request.form['image_path']
        rating = request.form.get('rating', type=float)

        new_restaurant = Restaurant(name=name, description=description, image_path=image_path, rating=rating)
        db.session.add(new_restaurant)
        db.session.commit()

        return redirect(url_for('restaurant', restaurant_id=new_restaurant.id))
    else:
        # Display the form for a GET request
        return render_template('add_restaurant.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/restaurant/<int:restaurant_id>')
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    return render_template('restaurant.html', restaurant=restaurant)
    
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/restaurants')
def restaurants():
    return render_template('restaurants.html', restaurants=restaurants)

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

        if user is None or not check_password_hash(user['password'], password):
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
        elif conn.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone() is not None:
            error = 'Username already exists.'
        elif conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone() is not None:
            error = 'Email already exists.'
        else:
            hashed_password = generate_password_hash(password)
            conn.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)',
                         (username, hashed_password, email))
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_database_table()  # Create the database table
    app.run(debug=True)  # Added the missing closing parenthesis

