from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_reverse_proxy_fix.middleware import ReverseProxyPrefixFix
from prometheus_flask_exporter import PrometheusMetrics


from .config import config_by_name

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
metrics = PrometheusMetrics(None)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    app.config['REVERSE_PROXY_PATH'] = '/api'
    ReverseProxyPrefixFix(app)
    db.init_app(app=app)
    metrics.init_app(app)
    flask_bcrypt.init_app(app)

    return app