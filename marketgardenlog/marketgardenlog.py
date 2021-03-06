from flask import session as login_session
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Garden, Plant, User

import json
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

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


@app.route('/gardens/<int:garden_id>/<int:plant_id>/JSON')
def gardenPlantJSON(garden_id, plant_id):
    plant = session.query(Plant).filter_by(id=plant_id).one()
    return jsonify(Plant=plant.serialize)


@app.route('/')
@app.route('/gardens/')
def showGardens():
    gardens = session.query(Garden).order_by(asc(Garden.created))
    typesOfGardens = set([g.garden_type for g in gardens])
    if 'username' not in login_session:
        return render_template('publicgardens.html', gardens=gardens)
    return render_template('gardens.html', gardens=gardens)


@app.route('/gardens/<int:garden_id>/')
def showGarden(garden_id):
    garden = session.query(Garden).filter_by(id=garden_id).one()
    plants = session.query(Plant).filter_by(garden_id=garden_id).all()
    if 'username' not in login_session:
        return render_template('publicgarden.html',
                               garden=garden, plants=plants)
    return render_template('garden.html', garden=garden, plants=plants,
                           creator=garden.user)


@app.route('/gardens/<garden_type>/')
def showGardenType(garden_type):
    gardens = session.query(Garden).filter_by(garden_type=garden_type).all()
    return render_template('gardenstypes.html', gardens=gardens,
                           garden_type=garden_type)


@app.route('/gardens/plants/<plant_type>/')
def showPlantType(plant_type):
    plants = session.query(Plant).filter_by(plant_type=plant_type).all()
    return render_template('plantstypes.html', plants=plants,
                           plant_type=plant_type)


@app.route('/gardens/<int:garden_id>/edit/', methods=['GET', 'POST'])
def editGarden(garden_id):
    if 'username' not in login_session:
        return redirect('login')
    garden = session.query(Garden).filter_by(id=garden_id).one()
    if login_session['username'] != garden.user.name:
        flash('Only the creator can edit this garden.')
        return redirect(url_for('showGarden', garden_id=garden_id))
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
    if 'username' not in login_session:
        return redirect('login')
    garden = session.query(Garden).filter_by(id=garden_id).one()
    if login_session['username'] != garden.user.name:
        flash('Only the creator can delete this garden.')
        return redirect(url_for('showGarden', garden_id=garden_id))

    if request.method == 'POST':
        plants = session.query(Plant).filter_by(garden_id=garden_id).all()
        for plant in plants:
            session.delete(plant)
        session.delete(garden)
        session.commit()
        flash('Garden Successfully Deleted')
        return redirect(url_for('showGardens'))
    else:
        return render_template('delete_garden.html', garden=garden)


@app.route('/gardens/new/', methods=['GET', 'POST'])
def newGarden():
    if 'username' not in login_session:
        return redirect('login')
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
    if 'username' not in login_session:
        return redirect('login')
    garden = session.query(Garden).filter_by(id=garden_id).one()
    if login_session['username'] != garden.user.name:
        flash('Only the creator can create a plant in this garden.')
        return redirect(url_for('showGarden', garden_id=garden_id))

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
    if 'username' not in login_session:
        return redirect('login')
    plant = session.query(Plant).filter_by(id=plant_id).one()
    if login_session['username'] != plant.user.name:
        flash('Only the creator can edit this plant.')
        return redirect(url_for('showGarden', garden_id=garden_id))

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
    if 'username' not in login_session:
        return redirect('login')
    plant = session.query(Plant).filter_by(id=plant_id).one()
    if login_session['username'] != plant.user.name:
        flash('Only the creator can delete this plant.')
        return redirect(url_for('showGarden', garden_id=garden_id))

    if request.method == 'POST':
        session.delete(plant)
        session.commit()
        return redirect(url_for('showGarden', garden_id=garden_id))
    else:
        return render_template('delete_plant.html', plant=plant)


# User Helper Functions
def createUser(login_session):
    """
    createUser: stores a user in the DB with the data from the parameter
    Args:
        login_session: the data to create the user
    """
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    """
    getUserInfo: returns the user object from the DB with the id from the
    parameter
    Args:
        user_id (data type: int): the id of the user to return
    Returns:
        return the user object
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    """
    getUserID: returns the id of user with the email from the parameter
    Args:
        email (data type: String): the email of the user to return
    Returns:
        return the id of the user
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/login')
def login():
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html')


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already \
                                 connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
              150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    return h.request(url, 'GET')[0]


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchange client token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json',
                        'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json',
                            'r').read())['web']['app_secret']
    url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (app_id, app_secret, access_token)  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Strip expire tag from access token
    token = result.split("&")[0]

    # Get user info
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['credentials'] = access_token
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token  # NOQA
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
              150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session.get('credentials')
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # NOQA
    # url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    h = httplib2.Http()
    return h.request(url, 'DELETE')[1]


@app.route('/logout')
def logout():
    print login_session
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            result = gdisconnect()
            del login_session['gplus_id']
        if login_session['provider'] == 'facebook':
            result = fbdisconnect()
            del login_session['facebook_id']
        print result
        del login_session['credentials']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        del login_session['state']
        flash("You have successfully been logged out.")
        print login_session
        return redirect(url_for('showGardens'))

    else:
        flash("You were not logged in")
        return redirect(url_for('showGardens'))


# Perform queries with every request can affect the perfomance with more data
# TODO: explore cache options
@app.context_processor
def injectTypesOfGardens():
    return dict(typesOfGardens=typesOfGardens(),
                typesOfPlants=typesOfPlants())


def typesOfGardens():
    """
    typesOfGardens: returns a set with the types of gardens present in the DB
    Returns:
        return a set of Strings with the types of gardens
    """
    gardens = session.query(Garden).order_by(asc(Garden.created))
    return set([g.garden_type for g in gardens])


def typesOfPlants():
    """
    typesOfPlants: returns a set with the types of plants present in the DB
    Returns:
        return a set of Strings with the types of plants
    """
    plants = session.query(Plant).order_by(asc(Plant.date_planted))
    return set([p.plant_type for p in plants])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000)
