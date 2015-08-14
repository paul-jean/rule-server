from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_setup import Restaurant, MenuItem, User
from db_link import getDBLink

if __name__ == '__main__':
    # init SQLAlchemy
    Base = declarative_base()
    dblink = getDBLink()
    engine = create_engine(dblink)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind = engine)
    session = DBSession()

    pj_email = "paul.jean.letourneau@gmail.com"
    pj_user_existing = session.query(User).filter_by(email = pj_email).first()
    if pj_user_existing:
        pj_user = pj_user_existing
    else:
        pj_name = "Paul-Jean Letourneau"
        pj_picture = "https://lh3.googleusercontent.com/-wx2tKtlpIL8/AAAAAAAAAAI/AAAAAAAAADc/7vWBOFHN47E/photo.jpg"
        pj_user = User(name = pj_name, email = pj_email, picture = pj_picture)
        print "Adding user: " + pj_name
        session.add(pj_user)
        session.commit()

    rest_data = \
    [
            {
                'rest_name': "Samantha's Super Sammies",
                'user_id': pj_user.id,
                'menu_items': [
                    {
                        'item_name': 'Rosewater Roti',
                        'item_course': "Entree",
                        'item_description': "Roti with a hint of rosewater",
                        'item_price': "5.99",
                        'item_picture': "http://massystorestt.com/wp-content/uploads/2015/05/Thawa-Roti.jpg"
                    },
                    {
                        'item_name': "Super Sunday Ham Sammie",
                        'item_course': "Entree",
                        'item_description': "Ham sammich (only on Sundays)",
                        'item_price': "4.99",
                        'item_picture': "http://blogs.plos.org/obesitypanacea/files/2014/10/sandwich.jpg"
                    },
                    {
                        'item_name': "Sam's Iced Tea",
                        'item_course': "Beverege",
                        'item_description': "Mint, green, or Sam's special blend",
                        'item_price': "1.99",
                        'item_picture': "https://upload.wikimedia.org/wikipedia/commons/e/e1/NCI_iced_tea.jpg"
                    },
                    {
                        'item_name': "Sam's Sweet Ice Cream Sam'wich",
                        'item_course': "Dessert",
                        'item_description': "Sandwich with a sweet surprise",
                        'item_price': "3.99",
                        'item_picture': "https://michaelstvtray.files.wordpress.com/2013/08/ice-cream-sandwich.jpg"
                    },
                    {
                        'item_name': "Pre-sandwich pickle plate",
                        'item_course': "Appetizer",
                        'item_description': "Brine Pickles of many varieties",
                        'item_price': "3.99",
                        'item_picture': "http://www.thedeliciouslife.com/wp-content/uploads/2010/11/salts-cure-pickle-plate.jpg"
                    }
                ]
            }
    ]

    def add_item(item_data, rest_id, user_id):
        item_name = item_data['item_name']
        existing_item = session.query(MenuItem).filter_by(restaurant_id = rest_id, name = item_name).first()
        if not existing_item:
            item_course = item_data['item_course']
            item_description = item_data['item_description']
            item_price = item_data['item_price']
            item_picture = item_data['item_picture']
            item = MenuItem(
                name = item_name, course = item_course,
                description = item_description, price = item_price, picture = item_picture,
                restaurant_id = rest_id, user_id = user_id)
            print "Adding item: " + item_name
            session.add(item)
            session.commit()

    def add_restaurant(rest_data):
        rest_name = rest_data['rest_name']
        rest_user_id = rest_data['user_id']
        existing_rest = session.query(Restaurant).filter_by(name = rest_name).first()
        if existing_rest:
            rest = existing_rest
        else:
            rest = Restaurant(name = rest_name, user_id = rest_user_id)
            print "Adding restaurant: " + rest_name
            session.add(rest)
            session.commit()
        menu_items = rest_data['menu_items']
        for item in menu_items:
            add_item(item, rest.id, rest_user_id)

    for rest in rest_data:
        add_restaurant(rest)
