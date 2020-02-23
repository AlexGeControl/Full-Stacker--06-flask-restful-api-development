from flask import Flask

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import basedir, config
import logging
from .utils import format_datetime, create_file_handler

db = SQLAlchemy()
moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    # load configs:
    app.config.from_object(config[config_name])    
    config[config_name].init_app(app)    
    
    # activate extensions:
    db.init_app(app)
    moment.init_app(app)

    # jinja:
    app.jinja_env.filters['datetime'] = format_datetime
    # logging:
    app.logger.setLevel(logging.INFO)
    app.logger.info('errors')
    app.logger.addHandler(create_file_handler(basedir))

    # attach routes and custom error pages here    
    from .main import main as blueprint_main
    app.register_blueprint(blueprint_main)

    return app

from . import models