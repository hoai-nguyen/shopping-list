# -*- coding: utf-8 -*-

from os import environ
from flask import Flask, Response, redirect, g, url_for
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


@app.route("/protected")
@oidc.require_login
def protected():
    html = """
    <html>
        <body>

            <form>
                <div>
               <input type="button" onclick="location.href='http://localhost:5000/logout';" value="Logout" />
            </div>
              <div class="form-group">
                <label for="exampleFormControlInput1">Email address</label>
                <input type="email" class="form-control" id="exampleFormControlInput1" placeholder="name@example.com">
              </div>
              <div class="form-group">
                <label for="exampleFormControlSelect1">Example select</label>
                <select class="form-control" id="exampleFormControlSelect1">
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                  <option>5</option>
                </select>
              </div>
              <div class="form-group">
                <label for="exampleFormControlSelect2">Example multiple select</label>
                <select multiple class="form-control" id="exampleFormControlSelect2">
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                  <option>5</option>
                </select>
              </div>
              <div class="form-group">
                <label for="exampleFormControlTextarea1">Example textarea</label>
                <textarea class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
              </div>
            </form>
        </body>
    </html>
    """
    return Response(html)


@app.route("/")
def landing_page():
    html = """
    <div>
       <input type="button" onclick="location.href='http://localhost:5000/login';" value="SSO Login" />
    </div>
    Welcome!

    """
    return Response(html)


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".protected"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".landing_page"))


from apps import models
from apps.api import routes

