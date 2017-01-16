from flask import session as login_session
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)

app = Flask(__name__)


@app.route('/')
@app.route('/gardens')
def showGardens():
    return render_template('gardens.html')


@app.route('/gardens/<int:garden_id>/')
def showGarden(garden_id):
    return render_template('garden.html', garden_id=garden_id)


@app.route('/gardens/<int:garden_id>/edit')
def editGarden(garden_id):
    return render_template('edit_garden.html', garden_id=garden_id)


@app.route('/gardens/<int:garden_id>/delete')
def deleteGarden(garden_id):
    return render_template('delete_garden.html', garden_id=garden_id)


@app.route('/gardens/new')
def newGarden():
    return render_template('new_garden.html')


@app.route('/gardens/<int:garden_id>/newplant')
def newPlant(garden_id):
    return render_template('new_plant.html', garden_id=garden_id)


@app.route('/gardens/<int:garden_id>/<int:plant_id>/edit')
def editPlant(garden_id, plant_id):
    return render_template('edit_plant.html', garden_id=garden_id,
                           plant_id=plant_id)


@app.route('/gardens/<int:garden_id>/<int:plant_id>/delete')
def deletePlant(garden_id, plant_id):
    return render_template('delete_plant.html', garden_id=garden_id,
                           plant_id=plant_id)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
