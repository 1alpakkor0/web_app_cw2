from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from app import views, models

@login_manager.user_loader ## This function is used for loading the user from the database using the user id
def load_user(user_id):
     return models.User.query.get(int(user_id))



csfr = CSRFProtect(app)