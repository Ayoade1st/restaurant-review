from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_path = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    rating = db.Column(db.Float)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')
    profile_image_url = db.Column(db.String(200))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.String(200))
    reviews = db.relationship('Review', backref='user', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='pending')
    helpful_count = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        bio = request.form.get('bio', '')

        new_user = User(username=username, password_hash=password, email=email,
                        first_name=first_name, last_name=last_name, bio=bio)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename, cache_timeout=0)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/restaurants')
def restaurants():
    all_restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=all_restaurants)
    
    
# @app.route('/restaurants')
# def restaurants():
    # return render_template('restaurants.html')
    
    
@app.route('/explore')
def explore():
    return redirect(url_for('restaurants'))  # Redirect to /restaurants route

@app.route('/reviews')
def reviews():
    all_reviews = Review.query.all()
    return render_template('reviews.html', reviews=all_reviews)
    

@app.route('/restaurant/<int:id>')  # Renamed route to avoid conflict with 'reviews' function name
def restaurant_reviews(id):
    restaurant = Restaurant.query.get_or_404(id)  # Fetch the restaurant by its ID
    reviews = Review.query.filter_by(id=id).all()  # Fetch reviews for this restaurant
    return render_template('restaurants.html', restaurant=restaurant, reviews=reviews)  # Pass the restaurant object along with reviews
    
#@app.route('/restaurant/<int:restaurant_id>')  # Pass restaurant_id as an argument
#def restaurant_reviews(restaurant_id):
    #restaurant = Restaurant.query.get_or_404(restaurant_id)  # Fetch the restaurant by its ID
    #reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()  # Fetch reviews for this restaurant
    #return render_template('restaurants.html', restaurant=restaurant, reviews=reviews)

@app.route('/add-restaurant', methods=['GET', 'POST'])
def addrestaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(
            name=request.form['name'],
            image_path=request.form['image_path'],
            description=request.form['description'],
            rating=float(request.form['rating'])
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for('restaurants'))
    return render_template('add-restaurant.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            # User's credentials are correct
            # Here you would set up the user session
            return redirect(url_for('profile', username=user.username))  # Assuming you have a profile view that uses username
        else:
            flash('Invalid email or password')
    return render_template('login.html')
    
    

@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@app.route('/restaurant/<int:id>')  # Route for restaurant details
def restaurant_details(id):
    restaurant = Restaurant.query.get_or_404(id)  # Get restaurant by ID
    return render_template('restaurant_details.html', restaurant=restaurant)

#@app.route('/restaurant/<int:restaurant_id>/reviews')
#def restaurant_reviews(restaurant_id):
    #restaurant = Restaurant.query.get_or_404(restaurant_id)
    #$reviews = Review.query.filter_by(restaurant_id=restaurant_id).all()  # Fetch reviews for this restaurant
    #$return render_template('restaurant_reviews.html', restaurant=restaurant, reviews=reviews)

if __name__ == '__main__':
    app.run(debug=True)
