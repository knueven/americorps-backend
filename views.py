import volunteer
import admin
import orgmember
import event
from flask import render_template,redirect, url_for, json, g
from flask.ext.login import login_user, logout_user, current_user, login_required
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

@app.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def users():
    content = {'content':'blah'}
    success = {'status':'account created, yay!'}
    error = {'error': 'Error in JSON/SQL syntax'}
    error2 = {'error': 'User already exists'}
    if request.method == 'POST':
        data = request.json
        if data['permissions'] == 'volunteer':
            if volunteer.Volunteer.createVolunteer(data):
                return success, status.HTTP_200_OK
            else: 
                return error2, status.HTTP_200_OK
        if data['permissions'] == 'admin':
            if admin.Admin.createAdmin(data):
                return success, status.HTTP_200_OK
        if data['permissions'] == 'orgmember':
            if orgmember.OrgMember.createMember(data):
                return success, status.HTTP_200_OK
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR

    if request.method == 'GET':
        return content, status.HTTP_200_OK

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

