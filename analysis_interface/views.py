from flask import request, jsonify, render_template
from analysis_interface import app


@app.route('/')
@app.route('/index.html')
def index1():
    return render_template('index.html', the_title='Tiger Home Page')


@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')


@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')


@app.route('/my_api')
def my_api():
    return jsonify("MESSAGE"), 200

