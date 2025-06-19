from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Chatterbox API</h1>'

# GET all messages
@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

# POST a new message
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    try:
        new_msg = Message(username=data['username'], body=data['body'])
        db.session.add(new_msg)
        db.session.commit()
        return jsonify(new_msg.to_dict()), 201
    except Exception as e:
        return {"error": str(e)}, 400

# PATCH a message
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()

    if 'body' in data:
        message.body = data['body']
        db.session.commit()
        return jsonify(message.to_dict()), 200
    return {"error": "No body provided"}, 400

# DELETE a message
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return {"message": "Message deleted"}, 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
