from decouple import config
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Blueprints
from web.accounts.views import accounts_bp
from web.core.views import core_bp

app.register_blueprint(accounts_bp)
app.register_blueprint(core_bp)

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "danger"


from web.accounts.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
