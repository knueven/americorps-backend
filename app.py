from flask import Flask, request, render_template
from flask.ext.api import FlaskAPI, status
from flask.ext.cors import CORS


#when we have secret keys and such turn this back on
import config

app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = 'super-secret'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# will pull config options from config.py
#app.config.from_object(config)