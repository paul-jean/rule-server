from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem

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

@app.route('/restaurant/new')
def newRestaurant():
    return render_template('newRestaurant.html')

@app.route('/restaurant/<int:rest_id>/edit')
def editRestaurant(rest_id):
    rest = findRestaurant(rest_id)
    return render_template('editRestaurant.html', rest=rest)

@app.route('/restaurant/<int:rest_id>/delete')
def deleteRestaurant(rest_id):
    rest = findRestaurant(rest_id)
    return render_template('deleteRestaurant.html', rest=rest)

@app.route('/restaurant/<int:rest_id>/')
@app.route('/restaurant/<int:rest_id>/menu')
def showMenu(rest_id):
    rest = findRestaurant(rest_id)
    return render_template('menu.html', restaurant=rest, items=items)

@app.route('/restaurant/<int:rest_id>/menu/new')
def newMenuItem(rest_id):
    rest = findRestaurant(rest_id)
    return render_template('newMenuItem.html', restaurant=rest)

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
