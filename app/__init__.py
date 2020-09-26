#Initialiserer app med de fleste importer
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


app = Flask(__name__)

#Lager secret key og database addresse
app.config['SECRET_KEY'] = '9cd062ffbbcb3a51fdf4e3ac9a75ae674cb7ff89a04627b372072d77b1eb4409'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testDB.db'

#activerer imports
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
limiter = Limiter(app, key_func=get_remote_address)

from app import routes
