from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    mood_logs = db.relationship('MoodLog', backref='user', lazy=True)

# Mood Tracking Model
class MoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

# User Registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"})

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials!"}), 401

# Mood Logging
@app.route('/log_mood', methods=['POST'])
def log_mood():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user:
        new_mood = MoodLog(user_id=user.id, mood=data['mood'])
        db.session.add(new_mood)
        db.session.commit()
        return jsonify({"message": "Mood logged successfully!"})
    return jsonify({"message": "User not found!"}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
