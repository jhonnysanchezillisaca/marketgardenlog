from flask import session as login_session
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)

app = Flask(__name__)


@app.route('/')
@app.route('/gardens')
def showGardens():
    return "List all the gardens"


@app.route('/gardens/<int:garden_id>/')
def showGarden(garden_id):
    return "Shows a garden"


@app.route('/gardens/<int:garden_id>/edit')
def editGarden(garden_id):
    return "Edit garden %s" % garden_id


@app.route('/gardens/<int:garden_id>/delete')
def deleteGarden(garden_id):
    return "Delete garden %s" % garden_id


@app.route('/gardens/new')
def newGarden(garden_id):
    return "Create new garden"


@app.route('/gardens/<int:garden_id>/newplant')
def newPlant(garden_id):
    return "Create new plant"


@app.route('/gardens/<int:garden_id>/<int:plant_id>/edit')
def editPlant(garden_id, plant_id):
    return "Edit plant %s from garden %s" % (plant_id, garden_id)


@app.route('/gardens/<int:garden_id>/<int:plant_id>/delete')
def deletePlant(garden_id, plant_id):
    return "Delete plant %s from garden %s" % (plant_id, garden_id)


@app.route('/login')
def login():
    return "Log in"


@app.route('/logout')
def logout():
    return "Log Out"


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
