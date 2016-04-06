import volunteer
import admin
import orgmember
import event
from flask import render_template,redirect, url_for, json, g
from flask.ext.api import status
from flask import Flask, request, jsonify, session
from db import Base, Session
from app import app
from user import User
import jwt
from datetime import datetime, timedelta
@app.route('/')
def index():
    content = {'test content':'disregard'}
    return content, status.HTTP_404_NOT_FOUND

@app.route('/user/', methods=['POST'])
def create_user():
    success = {'status':'account created, yay!'}
    error = {'error': 'Error in JSON/SQL syntax'}
    error2 = {'error': 'User already exists'}
    error3 = {'error': 'No user data provided'}
    data = request.json
    if data:
        if data['permissions'] == 'volunteer':
            if createVolunteer(data):
                return success, status.HTTP_200_OK
            else: 
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        if data['permissions'] == 'admin':
            if admin.Admin.createAdmin(data):
                return success, status.HTTP_200_OK
            else:
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        if data['permissions'] == 'orgmember':
            if orgmember.OrgMember.createMember(data):
                return success, status.HTTP_200_OK
            else:
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        return error3, status.HTTP_400_BAD_REQUEST

    # create a volunteer from a json blob
def createVolunteer(json):
    v = volunteer.Volunteer.fromdict(json)
    s = Session()
    try:
        s.add(v)
        s.commit()

    except:
        return False
    finally:
        #v1 = s.query(User).filter_by(email=v.email, name=v.name).first()
       # volunteer.Volunteer.grab_neighborhoods(v1, json)
        # volunteer.Volunteer.grab_skills(v,json)
        # volunteer.Volunteer.grab_interests(v, json)
        # volunteer.Volunteer.grab_availability(v, json)
        s.close()
        createEnums(v, json)
        return True

def createEnums(v, json):
    s = Session()
    try:
        v1 = s.query(User).filter_by(email=v.email).first()
        print("enums")
        print(v1.id)
        volunteer.Volunteer.grab_neighborhoods(v1.id, json)
    except:
        return False
    finally:
        s.close()
        return True

@app.route('/user/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
def users(user_id):
    error = {'error': 'Error in JSON/SQL syntax'}
    updateSuccess = {'status':'account updated'}
    updateError = {'error': 'User not found/input validation failed.'}
    noUser = {'error': 'User not found.'}
    # update user
    if request.method == 'POST':
        data = request.json
        if data:
            s = Session()
            u = s.query(User).filter_by(id=user_id).update(data)
            if u:
                s.commit()
                s.close()
                return updateSuccess, status.HTTP_200_OK
            else:
                return updateError, status.HTTP_400_BAD_REQUEST
    if request.method == 'GET':
        s = Session()
        u = s.query(User).filter_by(id=user_id).first()
        if u:
            return jsonify(u.asdict()), status.HTTP_200_OK
            s.close()
        else:
            return noUser, status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        return error, HTTP_503_SERVICE_UNAVAILABLE 

@app.route('/event', methods=['GET', 'POST', 'PUT', 'DELETE'])
def events():
    content = {'events': 'test'}
    success = {'status': 'event created'}
    error = {'error': "Error in JSON/SQL syntax"}
    if request.method == 'POST':
        data = request.json
        if event.Event.createEvent(data):
            return success, status.HTTP_200_OK
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
    if request.method == 'GET':
        return content, status.HTTP_200_OK

@app.route('/login', methods=['POST'])
def login():
    s = Session()
    json_data = request.json
    user = s.query(User).filter_by(email=json_data['email']).first()
    s.close()
    if user and user.check_password(json_data['passwordhash']):
        session['logged_in'] = True
        status = True
        return create_token(user)
    else:
        status = False
        return jsonify({'result': status})

def create_token(user):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.utcnow(),
        #expiry
        'exp': datetime.utcnow() + timedelta(days=1)
    }
 
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.secret_key, algorithms='HS256')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('logged_in', None)
    return jsonify({'result': 'success'})

