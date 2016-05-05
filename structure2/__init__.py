from flask import Flask
import secrets

app = Flask(__name__)
app.secret_key = secrets.app_secret()

import sitstuff.views

