from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

myapp = Flask(__name__,instance_relative_config=True)

myapp.config.from_pyfile("config.py")

db = SQLAlchemy(myapp)
csrf = CSRFProtect(myapp)
mail = Mail(myapp)

from applawlist import mymodels

from applawlist.routes import routes,adminroutes
