from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem
from bleach import clean

# init Flask
app = Flask(__name__)

# init SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant)
    return render_template('restaurants.html', restaurants=restaurants)

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
    return render_template('menu.html', restaurant=restObj, items=menuItems)

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

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit')
def editMenuItem(rest_id, menu_id):
    rest = findRestaurant(rest_id)
    menuItem = findMenuItem(menu_id)
    return render_template('editMenuItem.html', restaurant=rest, item=menuItem)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(rest_id, menu_id):
    rest = findRestaurant(rest_id)
    menuItem = findMenuItem(menu_id)
    return render_template('deleteMenuItem.html', restaurant=rest, item=menuItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
