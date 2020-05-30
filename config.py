#configuraion specifics for app
import os
from flask import Flask
from flask_cors import CORS
import model

def create_app():
    app = Flask(__name__)
    CORS(app)

    basedir = os.path.abspath(__file__)

    app.config.update(
        dict(
            SECRET_KEY="subscribe secretkey",
            WTF_CSRF_SECRET_KEY="subscribe csrf secret key",
            SQLALCHEMY_DATABASE_URI="sqlite:///" + 'aws-ssm-list.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False
        )
    )
    model.init_app(app)
    model.create_tables(app)
    return app
