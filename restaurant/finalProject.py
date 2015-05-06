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
    return render_template('placeholder.html', message='This page will show all \
            restaurants.')

@app.route('/restaurant/new')
def newRestaurant():
    return render_template('placeholder.html', message='This page will be for \
    making a new restaurant.')

@app.route('/restaurant/<int:rest_id>/edit')
def editRestaurant(rest_id):
    return render_template('placeholder.html', message='This page will be for \
    editing restaurant %s.' % rest_id)

@app.route('/restaurant/<int:rest_id>/delete')
def deleteRestaurant(rest_id):
    return render_template('placeholder.html', message='This page will be for \
    deleting restaurant %s.' % rest_id)

@app.route('/restaurant/<int:rest_id>/')
@app.route('/restaurant/<int:rest_id>/menu')
def showMenu(rest_id):
    return render_template('placeholder.html', message='This page is the menu for \
    restaurant %s.' % rest_id)

@app.route('/restaurant/<int:rest_id>/menu/new')
def newMenuItem(rest_id):
    return render_template('placeholder.html', message='This page is for \
    making a new menu item for restaurant %s.' % rest_id)

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit')
def editMenuItem(rest_id, menu_id):
    return render_template('placeholder.html', message='This page is for \
    editing menu item %s for restaurant %s.' % (menu_id, rest_id))

@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(rest_id, menu_id):
    return render_template('placeholder.html', message='This page is for \
    deleting menu item %s for restaurant %s.' % (menu_id, rest_id))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
