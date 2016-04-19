import volunteer
from volunteer import Volunteer
from organization import Organization
from admin import Admin
import admin
from organization import *
import orgmember
import organization
import event
from flask import render_template,redirect, url_for, json, g
from flask.ext.api import status
from flask import Flask, request, jsonify, session
from db import Base, Session
from app import app
from user import User
import jwt
from datetime import datetime, timedelta
from event import Event
from flask.ext.cors import CORS, cross_origin

@app.route('/')
def index():
    content = {'test content':'disregard'}
    return content, status.HTTP_404_NOT_FOUND

@app.route('/organization/', methods=['POST'])
def create_org():
    success = {'status':'organization created, yay!'}
    error = {'error': 'Error in JSON/SQL syntax'}
    error3 = {'error': 'No organization data provided'}
    data = request.json
    if data:
        if createOrganization(data):
            return success, status.HTTP_200_OK
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return error3, status.HTTP_400_BAD_REQUEST

@app.route('/user/', methods=['POST'])
def create_user():
    success = {'status':'account created, yay!'}
    error = {'error': 'Error in JSON/SQL syntax'}
    error3 = {'error': 'No user data provided'}
    data = request.json
    if data:
        if data['permissions'] == 'volunteer':
            if volunteer.createVolunteer(data):
                return success, status.HTTP_200_OK
            else:
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        if data['permissions'] == 'admin':
            if admin.Admin.createAdmin(data):
                return success, status.HTTP_200_OK
            else:
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        if data['permissions'] == 'organization': 
            if organization.createOrganization(data):
                return success, status.HTTP_200_OK
            else:
                return error, status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        return error3, status.HTTP_400_BAD_REQUESTup

@app.route('/organizations/<int:org_id>', methods=['GET', 'POST', 'DELETE'])
def orgs(org_id):
    error = {'error': 'Error in JSON/SQL syntax'}
    updateSuccess = {'status':'Organization updated'}
    updateError = {'error': 'Organization not found/input validation failed.'}
    noOrg = {'error': 'Organization not found.'}
    # update user
    if request.method == 'POST':
        data = request.json
        if data:
            s = Session()
            o = s.query(Organization).filter_by(id=org_id).update(data)
            if o:
                s.commit()
                s.close()
                return updateSuccess, status.HTTP_200_OK
            else:
                return updateError, status.HTTP_400_BAD_REQUEST
    if request.method == 'GET':
        s = Session()
        u = s.query(Organization).filter_by(id=org_id).first()
        if u:
            return jsonify(u.asdict()), status.HTTP_200_OK
            s.close()
        else:
            return noOrg, status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        return error, HTTP_503_SERVICE_UNAVAILABLE


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
        if event.createEvent(data):
            return success, status.HTTP_200_OK
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
    if request.method == 'GET':
        return content, status.HTTP_200_OK

@app.route('/event/signup', methods=['POST'])
def signup():
    error = {'error': "Error in JSON/SQL syntax"}
    success = {'success': 'signup successful!'}
    if request.method == 'POST':
        data = request.json
        if (volunteer.addEvent(data['eventid'], data['userid'])):
            return success, status.HTTP_200_OK
        else: 
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/login', methods=['POST'])
@cross_origin(headers=['Content-Type','Authorization'])
def login():
    s = Session()
    json_data = request.json
    user = s.query(User).filter_by(email=json_data['email']).first()
    error = "Login Failed"
    s.close()
    if user and user.check_password(json_data['passwordhash']):
        #session['logged_in'] = True
        #status = True
        if create_token(user) is not None:
            return create_token(user), status.HTTP_200_OK
        else:
            return jsonify({'result': "Token Failed" }), status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        #status = False
        return jsonify({'result': error}), status.HTTP_401_UNAUTHORIZED

def create_token(user):
    payload = {
        # subject
        'sub': user.id,
        #issued at
        'iat': datetime.utcnow(),
        #expiry
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    s = Session()
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    try:
        if (user.permissions == 'volunteer'):
            us = s.query(Volunteer).filter_by(id=user.id).first()
            d = volunteer.Volunteer.asdict(us)
        if (user.permissions == 'admin'):
            us = s.query(Admin).filter_by(id=user.id).first()
            d = admin.Admin.asdict(us)
        if (user.permissions == 'organization'):
            us = s.query(Organization).filter_by(id=user.id).first()
            d =organization.Organization.asdict(us)
    except:
        return None
    finally:
        s.close() 
    m = {'token': str(token), 'user': d}
    return m


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.secret_key, algorithms='HS256')

@app.route('/logout', methods=['GET'])
def logout():
    return jsonify({'result': 'success'})
