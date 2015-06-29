from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem
from bleach import clean
from random import randrange
from re import sub

# init Flask
app = Flask(__name__)

# init SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
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
    if request.method == 'POST':
        restName = request.form['name']
        restName = clean(restName)
        restObj = Restaurant(name = restName)
        session.add(restObj)
        session.commit()
        restaurants = session.query(Restaurant)
        return render_template('restaurants.html', restaurants=restaurants)
    else:
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:rest_id>/edit', methods = ['GET', 'POST'])
def editRestaurant(rest_id):
    if request.method == 'POST':
        restObj = session.query(Restaurant).filter_by(id = rest_id).one()
        restName = request.form['name']
        restName = clean(restName)
        restObj.name = restName
        session.add(restObj)
        session.commit()
        restaurants = session.query(Restaurant)
        return render_template('restaurants.html', restaurants=restaurants)
    else:
        rest = session.query(Restaurant).filter_by(id = rest_id).one()
        return render_template('editRestaurant.html', restaurant=rest)

@app.route('/restaurant/<int:rest_id>/delete', methods = ['GET', 'POST'])
def deleteRestaurant(rest_id):
    if request.method == 'POST':
        restObj = session.query(Restaurant).filter_by(id = rest_id).one()
        session.delete(restObj)
        session.commit()
        restaurants = session.query(Restaurant)
        return render_template('restaurants.html', restaurants=restaurants)
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
    return render_template('menu.html', restaurant=restObj, items=menuItems)

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
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        course = request.form['course']
        newItem = MenuItem(name = name, course = course, description = description, price = price, restaurant_id = rest_id)
        session.add(newItem)
        session.commit()
        menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
        return render_template('menu.html', restaurant=restObj, items=menuItems)
    else:
        return render_template('newMenuItem.html', restaurant=restObj)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(rest_id, menu_id):
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
        menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
        return render_template('menu.html', restaurant=restObj, items=menuItems)
    else:
        return render_template('editMenuItem.html', restaurant=restObj, item=menuItemObj)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(rest_id, menu_id):
    menuItemObj = session.query(MenuItem).filter_by(id = menu_id).one()
    restObj = session.query(Restaurant).filter_by(id = rest_id).one()
    if request.method == 'POST':
        session.delete(menuItemObj)
        session.commit()
        menuItems = session.query(MenuItem).filter_by(restaurant_id = rest_id).all()
        return render_template('menu.html', restaurant=restObj, items=menuItems)
    else:
        return render_template('deleteMenuItem.html', restaurant=restObj, item=menuItemObj)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
