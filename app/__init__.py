from flask import Flask
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

from .models import db
db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)