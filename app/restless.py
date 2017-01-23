from flask import request, jsonify, Blueprint
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from User import User
from Notes import Note
from app import app, db
from decorator import crossdomain

page = Blueprint('auth', __name__, url_prefix='/api')

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = User.query.filter_by(id=payload['identity']).first()
    return user_id


@page.route('/user', methods=['GET', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def protected():
    return '%s' % current_identity

@page.route('/Notes', methods=['GET', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def getNotes():
    notes = Note.query.filter_by(user_id=current_identity.id).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@page.route('/Tag/<tag>/Notes', methods=['GET', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def getNotesByTag(tag):
    notes = Note.query.filter_by(user_id=current_identity.id).filter_by(tag_id=tag).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@page.route('/Category/<category>/Notes', methods=['GET', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def getNotesByCat(category):
    notes = Note.query.filter_by(user_id=current_identity.id).filter_by(category_id=category).all()
    return jsonify(notes=[n.serialize() for n in notes]), 200

@page.route('/register', methods=['POST', 'OPTIONS'])#works
@crossdomain(origin='*')
def register():
    data = request.get_json(True);
    user = User(username=data['username'], password=data['password'])
    try:
        db.session.add(user)
        db.session.commit()
    except:
        return jsonify(message="Username not unique"), 400

    return jsonify(message="Account created successfully"), 201

@page.route('/Notes', methods=['POST', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def addNote():
    data = request.get_json(True);
    note = Note(title=data['title'],
                body=data['body'],
                category_id=data['category'],
                tag_id=data['tag'],
                user_id=current_identity.id)
    try:
        db.session.add(note)
        db.session.commit()
    except:
        return jsonify(message="Error"), 400

    return jsonify(message="Note added succesfully"), 201

@page.route('/Notes/<id>', methods=['PUT', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def editNote(id):
    data = request.get_json(True);
    note = Note.query.filter_by(id=id).first();
    try:
        note.title = data['title']
        note.body = data['body']
        note.category_id = data['category']
        note.tag_id = data['tag']
        db.session.commit()
    except:
        return jsonify(message="Error, note with this id doesn't exist"), 400
    return jsonify(message="Note edited succesfully"), 201

@page.route('/Notes/<id>', methods=['DELETE', 'OPTIONS'])#works
@crossdomain(origin='*')
@jwt_required()
def deleteNote(id):
    note = Note.query.filter_by(id=id).first();
    try:
        db.session.delete(note)
        db.session.commit()
    except:
        return jsonify(message="Error, note with this id doesn't exist"), 400
    return jsonify(message="Note removed succesfully"), 200

@page.route('/Notes/<id>')#works
@crossdomain(origin='*')
@jwt_required()
def get_note(id):
    note = Note.query.filter_by(id=id).first()
    try:
        response = jsonify(note.serialize()), 200
    except:
        return jsonify(message="Error, note with this id doesn't exist"), 400
    return response


jwt = JWT(app, authenticate, identity)



