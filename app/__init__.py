from flask import Flask
from config import Config
from .models import db, Users
from flask_migrate import Migrate
from flask_login import LoginManager

from .auth.routes import auth
from .deck.routes import deck
from .battle.routes import battle

site = Flask(__name__)

# Add all items to site config 
config_instance = Config()
config = config_instance.__dict__
# Add all config fields to site config
site.config["ENV"] = config["config"]["env"]
site.config["SECRET_KEY"] = config["secret_key"]
for key, value in config["config"].items():
    site.config[key.upper()] = value
    
# Register Blueprint
site.register_blueprint(auth)
site.register_blueprint(deck)
site.register_blueprint(battle)

login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

login_manager.init_app(site)
login_manager.login_view = 'auth.login'

# Register DB
db.init_app(site)
migrate = Migrate(site, db)


from . import routes