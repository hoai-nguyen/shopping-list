# -*- coding: utf-8 -*-

from os import environ
from flask import g
from flask_oidc import OpenIDConnect
from okta import UsersClient
from dotenv import load_dotenv

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config, TestConfig
from apps.database import *

load_dotenv('.env')


def sso_setup(app):
    # secret credentials for Okta connection
    app.config["OIDC_CLIENT_SECRETS"] = "openidconnect_secrets.json"
    app.config["OIDC_COOKIE_SECURE"] = False
    app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
    app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
    app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"


def create_app(conf='any'):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY") or "my_secret"

    if conf == "TEST":
        app.config.from_object(TestConfig)
    else:
        sso_setup(app=app)
        app.config.from_object(Config)

    print(app.config['SQLALCHEMY_DATABASE_URI'])
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    return app


from apps import models

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# instantiate OpenID client to handle user session
oidc = OpenIDConnect(app)

# Okta client will determine if a user has an appropriate account
okta_client = UsersClient(
    environ.get("OKTA_ORG_URL"),
    # Securities -> API -> Tokens -> Create a token: https://dev-81881230-admin.okta.com/admin/access/api/tokens
    environ.get("OKTA_AUTH_TOKEN"),
)


@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


from apps import models
from apps.api import routes
from apps.pages import routes
