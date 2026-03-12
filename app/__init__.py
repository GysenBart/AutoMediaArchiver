from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config.from_object(Config)

# Configure database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-admin
admin = Admin(app, name="test")

from app import routes