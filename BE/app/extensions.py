from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Istanzia le estensioni
db = SQLAlchemy()
migrate = Migrate()