import volunteer
from volunteer import Volunteer
from admin import Admin
import admin
from organization import *
import orgmember
import organization
import event
from volunteerSkills import VolunteerSkills
from volunteerNeighborhoods import VolunteerNeighborhoods
from volunteerInterests import VolunteerInterests
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
    deleteSuccess = {'status' : 'Organization deleted'}
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
            s.close()
            return jsonify(u.asdict()), status.HTTP_200_OK
        else:
            return noOrg, status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        s = Session()
        org = s.query(Organization).filter_by(id=org_id).first()
        if not(org):
            return noOrg, status.HTTP_404_NOT_FOUND
        try:
            org.deleteSelf(s)
        except exc.SQLAlchemyError as e:
            deleteError = {'error': str(e)}
            return deleteError, status.HTTP_400_BAD_REQUEST
        s.close()
        return deleteSuccess, status.HTTP_200_OK


@app.route('/user/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
def users(user_id):
    error = {'error': 'Error in JSON/SQL syntax'}
    updateSuccess = {'status':'account updated'}
    updateError = {'error': 'User not found/input validation failed.'}
    noUser = {'error': 'User not found.'}
    deleteSuccess = {'status' : 'account deleted'}
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
            user_id = u.id
            u = u.asdict()
            u['skills'] = VolunteerSkills.get_skills(user_id)
            u['neighborhoods'] = VolunteerNeighborhoods.get_neighborhoods(user_id)
            u['interests'] = VolunteerInterests.get_interests(user_id)
            return jsonify(u), status.HTTP_200_OK
        else:
            return noUser, status.HTTP_404_NOT_FOUND
    if request.method == 'DELETE':
        s = Session()
        user = s.query(User).filter_by(id=user_id).first()
        if not(user):
            return noUser, status.HTTP_404_NOT_FOUND
        else:
            try:
                user.deleteSelf(s)
            except exc.SQLAlchemyError as e:
                deleteError = {'error' : e.args}
                return deleteError, status.HTTP_400_BAD_REQUEST
            finally:
                s.close()
            return deleteSuccess, status.HTTP_200_OK


@app.route('/user/loghours', methods=['POST'])
def hours():
    noVolunteer = {'error': 'Volunteer not found.'}
    wrong = {'error': 'JSON incorrect - need volunteer, event, and hours'}
    correct = {'status': 'hours logged!'}
    wrong2 = {'error': 'error logging hours'}
    data = request.json
    s = Session()
    vo = s.query(Volunteer).filter_by(id=data['volunteerid']).first()
    if not(vo):
        return noVolunteer, status.HTTP_404_NOT_FOUND
    else:
        eventid = data["eventid"]
        hours = data["hours"]
        if eventid and hours:
            if vo.log_hours(eventid, hours):
                return correct, status.HTTP_200_OK
            else:
                return wrong2, status.HTTP_500_INTERNAL_SERVER_ERROR
        else: 
            return wrong, status.HTTP_500_INTERNAL_SERVER_ERROR







@app.route('/event/<int:event_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def event(event_id):
    content = {'events': 'test'}
    success = {'status': 'event created'}
    updateSuccess = {'status':'account updated'}
    updateError = {'error': 'User not found/input validation failed.'}
    error = {'error': "Error in JSON/SQL syntax"}
    if request.method == 'POST':
        data = request.json
        if event.createEvent(data):
            return success, status.HTTP_200_OK
        else:
            return error, status.HTTP_500_INTERNAL_SERVER_ERROR
    if request.method == 'GET':
        return content, status.HTTP_200_OK
    if request.method == 'POST':
        data = request.json
        if data:
            s = Session()
            u = s.query(Event).filter_by(id=event_id).update(data)
            if u:
                s.commit()
                s.close()
                return updateSuccess, status.HTTP_200_OK
            else:
                return updateError, status.HTTP_400_BAD_REQUEST

@app.route('/event/get_all', methods=['GET'])
def get_all():
    if request.method == 'GET':
        s = Session()
        events = s.query(Event).all()
        events_Json = {'results':[]}
        for e in events:
            print(Event.asdict(e))
            events_Json['results'].append(Event.asdict(e))
        return events_Json, status.HTTP_200_OK



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

@app.route('/event/featured', methods=['GET'])
def featured():
    if request.method == 'GET':
        s = Session()
        feats = s.query(Event).filter_by(featured=True)
        feats_Json = {'results':[]}
        for e in feats:
            #print(Event.asdict(e))
            feats_Json['results'].append(Event.asdict(e))
        return feats_Json, status.HTTP_200_OK


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
