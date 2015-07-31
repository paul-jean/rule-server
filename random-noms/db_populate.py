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

    pj_name = "Paul-Jean Letourneau"
    pj_email = "paul.jean.letourneau@gmail.com"
    pj_picture = "https://lh3.googleusercontent.com/-wx2tKtlpIL8/AAAAAAAAAAI/AAAAAAAAADc/7vWBOFHN47E/photo.jpg"
    pj_user = User(name = pj_name, email = pj_email, picture = pj_picture)
    session.add(pj_user)
    session.commit()

    # user = session.query(User).filter_by(email = pj_email).one()

    rest_name = "Samantha's Super Sammies"
    rest_user_id = pj_user.id
    rest = Restaurant(name = rest_name, user_id = rest_user_id)
    session.add(rest)
    session.commit()

    item_name = "rose's rosewater rotie"
    item_course = "Entree"
    item_description = "rotie with a hint of rosewater"
    item_price = "5.99"
    item_picture = "http://massystorestt.com/wp-content/uploads/2015/05/Thawa-Roti.jpg"
    item = MenuItem(
        name = item_name, course = item_course,
        description = item_description, price = item_price, picture = item_picture,
        restaurant_id = rest.id, user_id = rest.user_id)
    session.add(item)
    session.commit()

