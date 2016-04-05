from flask import Flask, request, render_template
from flask.ext.api import FlaskAPI, status


#when we have secret keys and such turn this back on
import config

app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = 'super-secret'
# will pull config options from config.py
#app.config.from_object(config)