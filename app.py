from flask import Flask, request, render_template
from flask.ext.api import FlaskAPI, status

#when we have secret keys and such turn this back on
#import config

app = FlaskAPI(__name__)
# will pull config options from config.py
#app.config.from_object(config)

@app.route("/")
def index():
	content = {'test content':'disregard'}
	return content, status.HTTP_404_NOT_FOUND

if __name__ == "__main__":
    app.run(debug=True)