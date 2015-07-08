from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem, User
from bleach import clean
from random import randrange
from re import sub
from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# init Flask
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Random Restaurant Application"

# init SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu_withusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

def createUser(login_session):
    newUser = User(
            name = login_session['username'],
            email = login_session['email'],
            picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def getUserID(user_email):
    try:
        user = session.query(User).filter_by(email = user_email).one()
        return user.id
    except:
        return None

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user:
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Send http GET request to revoke current token:
    access_token = credentials.access_token
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session:
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For some reason, the given token was invalid:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain one-time authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    #Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later user
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if this user has an account
    user_id = getUserID(login_session['email'])
    if not user_id:
        # Create a new user
        user_id = createUser(login_session)

    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    credentials = login_session.get('credentials')
    if credentials is None:
        return render_template('restaurants_public.html', restaurants=restaurants)
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON/')
def showRestaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])

@app.route('/')
@app.route('/random/', methods = ['GET', 'POST'])
def randomRestaurant():
    if request.method == 'POST':
        restaurants = session.query(Restaurant).all()
        num_restaurants = len(restaurants)
        rand_restaurant_index = randrange(0, num_restaurants)
        rand_restaurant = restaurants[rand_restaurant_index]
        return render_template('random_choice.html', restaurant=rand_restaurant)
    else:
        return render_template('random_button.html')


@app.route('/restaurant/new', methods = ['GET', 'POST'])
def newRestaurant():
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        restName = request.form['name']
        restName = clean(restName)
        restObj = Restaurant(name = restName, user_id = login_session['user_id'])
        session.add(restObj)
        session.commit()
        restaurants = session.query(Restaurant)
        flash('Added restaurant: ' + restName)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:rest_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(rest_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        restObj = session.query(Restaurant).filter_by(id = rest_id).one()
        restName = request.form['name']
        restName = clean(restName)
        restObj.name = restName
        session.add(restObj)
        session.commit()
        restaurants = session.query(Restaurant)
        flash('Edited restaurant: ' + restName)
        return redirect(url_for('showRestaurants'))
    else:
        rest = session.query(Restaurant).filter_by(id = rest_id).one()
        return render_template('editRestaurant.html', restaurant=rest)

@app.route('/restaurant/<int:rest_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(rest_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        restObj = session.query(Restaurant).filter_by(id = rest_id).one()
        session.delete(restObj)
        session.commit()
        flash('Deleted restaurant: ' + restObj.name)
        return redirect(url_for('showRestaurants'))
    else:
        rest = session.query(Restaurant).filter_by(id = rest_id).one()
        return render_template('deleteRestaurant.html', restaurant=rest)

@app.route('/restaurant/<int:rest_id>/')
@app.route('/restaurant/<int:rest_id>/menu')
def showMenu(rest_id):
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
    for i in menuItems:
        i.price = sub('\$', '', i.price)
    if restObj.user_id == login_session['user_id']:
        return render_template('menu.html', restaurant=restObj, items=menuItems)
    else:
        creator = getUserInfo(restObj.user_id)
        return render_template('menu_public.html', restaurant=restObj, items=menuItems, creator=creator)

@app.route('/restaurant/<int:rest_id>/menu/JSON/')
def showMenuJSON(rest_id):
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
    for i in menuItems:
        i.price = sub('\$', '', i.price)
    return jsonify(MenuItems=[i.serialize for i in menuItems])

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/JSON/')
def showMenuItemJSON(rest_id, menu_id):
    menuItem = session.query(MenuItem).filter_by(restaurant_id = rest_id, id=menu_id).one()
    menuItem.price = sub('\$', '', menuItem.price)
    return jsonify(MenuItem=menuItem.serialize)

@app.route('/restaurant/<int:rest_id>/menu/new', methods = ['GET', 'POST'])
def newMenuItem(rest_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newItem = MenuItem(
                name = name, course = course,
                description = description, price = price,
                restaurant_id = rest_id, user_id = restObj.user_id)
        session.add(newItem)
        session.commit()
        flash('Added menu item: ' + name)
        return redirect(url_for('showMenu', rest_id=restObj.id))
    else:
        return render_template('newMenuItem.html', restaurant=restObj)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(rest_id, menu_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    menuItemObj = session.query(MenuItem).filter_by(id = menu_id).one()
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        menuItemObj.name = name
        menuItemObj.description = description
        menuItemObj.price = price
        menuItemObj.course = course
        session.add(menuItemObj)
        session.commit()
        flash('Edited menu item: ' + menuItemObj.name)
        menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
        return redirect(url_for('showMenu', rest_id=rest_id))
    else:
        return render_template('editMenuItem.html', restaurant=restObj, item=menuItemObj)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(rest_id, menu_id):
    credentials = login_session.get('credentials')
    if credentials is None:
        return redirect(url_for('showLogin'))
    menuItemObj = session.query(MenuItem).filter_by(id = menu_id).one()
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        session.delete(menuItemObj)
        session.commit()
        flash('Deleted menu item: ' + menuItemObj.name)
        return redirect(url_for('showMenu', rest_id=rest_id))
    else:
        return render_template('deleteMenuItem.html', restaurant=restObj, item=menuItemObj)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
