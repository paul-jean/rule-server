import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import insert
from sqlalchemy import create_engine, distinct
from database_setup import Restaurant, MenuItem

Base = declarative_base()
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

def get_restaurants():
    name_id = [(r.id, r.name) for r in \
            session.query(Restaurant).\
            order_by(Restaurant.name).\
            distinct(Restaurant.name).\
            group_by(Restaurant.name).all()]
    return name_id

def add_restaurant(restaurant_name):
    new_restaurant = Restaurant(name = restaurant_name)
    session.add(new_restaurant)
    session.commit()

def restaurant_exists(restaurant_name):
    rest = session.query(Restaurant).filter_by(name = restaurant_name).all()
    return len(rest) >= 1

def restaurant_name(restaurant_id):
    rest = session.query(Restaurant).filter_by(id = restaurant_id).one()
    return rest.name

def change_name(rest_id, new_name):
    rest = session.query(Restaurant).filter_by(id = rest_id).one()
    rest.name = new_name
    session.add(rest)
    session.commit()
    return new_name

def delete_restaurant(rest_id):
    rest = session.query(Restaurant).filter_by(id = rest_id).one()
    session.delete(rest)
    session.commit()
    return

def test():
    rs = get_restaurants()
    for r in rs:
        print r
