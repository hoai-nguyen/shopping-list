# -*- coding: utf-8 -*-

from flask import Response, redirect, g, url_for, render_template
from apps import app, oidc


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
@oidc.require_login
def landing_page():
    return redirect(url_for('login'))


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".index"))


@app.route('/index')
def index():
    return render_template('home/index.html', segment='index')


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".landing_page"))


@app.route("/profile")
@oidc.require_login
def profile():
    user = g.user
    return render_template('home/profile.html', **{
        "current_user": {
            "email": user.profile.email,
            "username": user.profile.email,
        }
    })