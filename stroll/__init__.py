from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '60e46d736a895ca04b3da5e5364c11f8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # 'sqlite://stroll/site.db' ?
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
db = SQLAlchemy(app)

from stroll import routes