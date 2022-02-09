from flask import Flask, request, jsonify,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token)

app = Flask(__name__)

DATABASE_URI = "sqlite:///itemss.db"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['JWT_SECRET_KEY'] = "secret-key"

jwt = JWTManager(app)
db = SQLAlchemy(app)

db.create_all()
app.run(debug=True)

class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    todo_item = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"User('{self.id}', '{self.todo_item}')"

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.password}')"

@app.route('/reg', methods=['POST'])
def register():
    id = request.json.get('id')
    username = request.json.get('username')
    password = request.json.get('password')

    user = User(id=id, username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        return {
            'status': 'success',
            'data': 'user added',
        }
    except:
        return {
            'status': 'failed',
            'data': 'invalid info',
        }


@app.route('/login', methods=['POST'])
def login():
    users = User.query.all()
    username = request.json.get('username')
    password = request.json.get('password')
    for user in users:
        if username == user.email and password == user.password:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'status': 'success',
                'data': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        return {
                'status': 'failed',
                'data': 'Bad username or password'
            }




@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    username = get_jwt_identity()
    return {
        'status': 'success',
        'data': 'you have valid token'
    }

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    access_token = create_access_token(identity=username)

    return {
        'access_token': access_token
    }

@app.route('/', methods=['GET'])
def home():  # put application's code here
    items = Items.query.all()
    data_result = []
    for item in items:
        u = {}
        u["id"] = item.id
        u["todo_item"] = item.todo_item
        u["status"] = item.status

        data_result.append(u)

    return jsonify({
        "result": "success",
        "data": data_result
    })

@app.route('/insert', methods=['POST'])
@jwt_required()
def insert():
    data = json.loads(request.data)
    id = data["id"]
    todo_item = data["todo_item"]
    status = data["status"]

    try:
        item = Items(id=id, todo_item=todo_item, status=status)
        db.session.add(item)
        db.session.commit()
    except ValueError as e:
        return jsonify({
                "result": "Failed",
                "data": "failed in add user"
            })

    return jsonify({
                "result": "success",
                "data": "user added successfully"
            })


@app.route('/delete/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    item = Items.query.filter_by(id=id).first()
    # user = User.query.get(id)
    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "result": "success",
        "data": "user deleted successfully"
    })


@app.route('/update/<id>', methods=['PUT'])
@jwt_required()
def update(id):
    item = Items.query.get(id)
    data = json.loads(request.data)

    todo_item = data["todo_item"]
    item.todo_item = todo_item

    status = data["status"]
    item.status = status

    db.session.commit()

    return jsonify({
        "result": "success",
        "data": "user updated successfully"
    })

@app.before_first_request
def set_config():
    db.create_all()


if __name__ == '__main__':
    app.run()
