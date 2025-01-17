from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian
from flasgger import Swagger

# from config import config_by_name

# Globally accessible libraries
db = SQLAlchemy()
guard = Praetorian()
swagger = Swagger()


def create_app():
    """Initialize the core app."""
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')

    # Register model
    from .usermanagement.models import UsermanagementModel

    # Initialize Plugins
    db.init_app(app)
    swagger.init_app(app)
    guard.init_app(app, UsermanagementModel)

    # Include our Routes
    @app.route('/')
    def index():
        """
        Index Endpoint
        ---
        tags:
            - index
        description: This is Index
        responses:
          200:
            description: index PAGE
        """
        return "must create index page"

    # Register Blueprints
    from .auth.views import auth_blueprint
    from .usermanagement.views import user_blueprint
    from .event.views import event_blueprint
    from .event.event_fish.views import event_fish_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(event_blueprint)
    app.register_blueprint(event_fish_blueprint)


    return app
