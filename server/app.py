from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at).all()
        return jsonify([message.to_dict() for message in messages]), 200

    elif request.method == 'POST':
        data = request.get_json()
        if not data.get('body') or not data.get('username'):
            return jsonify({'error': 'body and username are required'}), 400

        message = Message(body=data['body'], username=data['username'])
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201


@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get_or_404(id)

    if request.method == 'PATCH':
        data = request.get_json()
        for key, value in data.items():
            setattr(message, key, value)
        db.session.commit()
        return jsonify(message.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify({'deleted': True}), 200


if __name__ == "__main__":
    app.run(port=5555)
