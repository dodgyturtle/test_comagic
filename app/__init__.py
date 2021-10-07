from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)

ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config")
    ma.init_app(app)

    # from app.api_app.views import api_blueprint
    from app.web_app.views import web_blueprint

    # app.register_blueprint(api_blueprint)
    app.register_blueprint(web_blueprint)

    return app
