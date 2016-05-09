from flask import Flask
import secrets

app = Flask(__name__)
app.secret_key = secrets.APP_SECRET

import views#, controllers

