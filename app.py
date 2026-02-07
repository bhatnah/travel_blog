from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# 1. SQL Database Setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_blog.db'
db = SQLAlchemy(app)

# Blog Post Model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    recommendation = db.Column(db.String(200)) # e.g. "Visit this cafe!"
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    location = db.Column(db.String(100)) # India locations

# Create the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    # Replace with your actual Google Maps API Key
    MAP_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
    # Stripe or PayPal link
    PAYMENT_LINK = "https://buy.stripe.com/your_link" 
    
    return render_template('index.html', posts=posts, map_key=MAP_API_KEY, pay_link=PAYMENT_LINK)

@app.route('/add', methods=['POST'])
def add_post():
    from datetime import datetime
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form.get('start_date') else None
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form.get('end_date') else None
    
    new_post = Post(
        title=request.form['title'],
        content=request.form['content'],
        recommendation=request.form['recommendation'],
        start_date=start_date,
        end_date=end_date,
        location=request.form.get('location')
    )
    db.session.add(new_post)
    db.session.commit()
    return redirect('/')

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
