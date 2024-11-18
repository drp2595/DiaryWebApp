from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abcd1234@localhost/DiaryApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'age': self.age
        }

# # Create the database tables
# @app.before_first_request
# def create_tables():
#     db.create_all()

def login(request):
    data=request.get_json()
    username = data['username']
    password = data['password']
    
    # Example: hardcoded user credentials for the demo
    if username == "admin" and password == "admin":
        return jsonify({'message': 'Login successful', 'redirect': '/home'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not data.get('userName') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Username and Email are required'}), 400
    
    try:
        new_user = User(
            userName=data["userName"],
            firstName=data["firstName"],
            lastName=data["lastName"],
            city=data["city"],
            email=data["email"],
            password=data["password"],
            contact=data["contact"],
            active=1,
            )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Username or Email already exists'}), 400

# 2. Get all Users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# 3. Get a single User by ID
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# 4. Update a User
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'age' in data:
        user.age = data['age']
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

# 5. Delete a User
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User with id {id} deleted successfully'}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
