from flask import session as login_session
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Garden, Plant, User

import json


app = Flask(__name__)

engine = create_engine('sqlite:///marketgardenlog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON APIs
@app.route('/gardens/JSON')
def gardensJSON():
    gardens = session.query(Garden).all()
    return jsonify(Gardens=[i.serialize for i in gardens])


@app.route('/gardens/<int:garden_id>/JSON')
def gardenPlantsJSON(garden_id):
    plants = session.query(Plant).filter_by(garden_id=garden_id).all()
    return jsonify(Plants=[i.serialize for i in plants])


@app.route('/')
@app.route('/gardens/')
def showGardens():
    gardens = session.query(Garden).order_by(asc(Garden.created))
    return render_template('gardens.html', gardens=gardens)


@app.route('/gardens/<int:garden_id>/')
def showGarden(garden_id):
    garden = session.query(Garden).filter_by(id=garden_id).one()
    plants = session.query(Plant).filter_by(garden_id=garden_id).all()
    return render_template('garden.html', garden=garden, plants=plants)


@app.route('/gardens/<int:garden_id>/edit/', methods=['GET', 'POST'])
def editGarden(garden_id):
    garden = session.query(Garden).filter_by(id=garden_id).one()
    if request.method == 'POST':
        if request.form['name']:
            garden.name = request.form['name']
            garden.garden_type = request.form['type']
            garden.location = request.form['location']
            garden.comments = request.form['comments']
            flash('Garden Successfully Edited %s' %
                  garden.name)
            return redirect(url_for('showGarden', garden_id=garden_id))
    else:
        return render_template('edit_garden.html', garden=garden)


@app.route('/gardens/<int:garden_id>/delete/', methods=['GET', 'POST'])
def deleteGarden(garden_id):
    garden = session.query(Garden).filter_by(id=garden_id).one()
    if request.method == 'POST':
        session.delete(garden)
        session.commit()
        flash('Garden Successfully Deleted')
        return redirect(url_for('showGardens'))
    else:
        return render_template('delete_garden.html', garden=garden)


@app.route('/gardens/new/', methods=['GET', 'POST'])
def newGarden():
    login_session['user_id'] = 1
    if request.method == 'POST':
        new_garden = Garden(name=request.form['name'],
                            garden_type=request.form['type'],
                            location=request.form['location'],
                            comments=request.form['comments'],
                            user_id=login_session['user_id'])
        session.add(new_garden)
        session.commit()
        flash('New garden %s Successfully Created' % (new_garden.name))
        return redirect(url_for('showGarden', garden_id=new_garden.id))
    else:
        return render_template('new_garden.html')


@app.route('/gardens/<int:garden_id>/newplant/', methods=['GET', 'POST'])
def newPlant(garden_id):
    login_session['user_id'] = 1
    if request.method == 'POST':
        new_plant = Plant(name=request.form['name'],
                          plant_type=request.form['type'],
                          comments=request.form['comments'],
                          garden_id=garden_id,
                          user_id=login_session['user_id'])
        session.add(new_plant)
        session.commit()
        return redirect(url_for('showGarden', garden_id=garden_id))
    return render_template('new_plant.html', garden_id=garden_id)


@app.route('/gardens/<int:garden_id>/<int:plant_id>/edit/',
           methods=['GET', 'POST'])
def editPlant(garden_id, plant_id):
    plant = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        print "Inside POST"
        if request.form['name']:
            print "name correct"
            plant.name = request.form['name']
        if request.form['type']:
            print "type correct"
            plant.plant_type = request.form['type']
        else:
            # flash('Name and type are required')
            print "Inside post incorrect"
            return redirect(url_for('editPlant', garden_id=garden_id,
                            plant_id=plant.id))
        plant.comments = request.form['comments']
        session.add(plant)
        session.commit()
        print "Session comited"
        print url_for('showGarden', garden_id=garden_id)
        return redirect(url_for('showGarden', garden_id=garden_id))

    else:
        return render_template('edit_plant.html', plant=plant)


@app.route('/gardens/<int:garden_id>/<int:plant_id>/delete/',
           methods=['GET', 'POST'])
def deletePlant(garden_id, plant_id):
    plant = session.query(Plant).filter_by(id=plant_id).one()
    if request.method == 'POST':
        session.delete(plant)
        session.commit()
        return redirect(url_for('showGarden', garden_id=garden_id))
    else:
        return render_template('delete_plant.html', plant=plant)


@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html')


@app.route('/logout')
def logout():
    return redirect('/')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
