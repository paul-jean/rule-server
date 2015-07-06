# Random restaurant

## App setup

``` bash
    vagrant@vagrant-ubuntu-trusty-32:/vagrant/restaurant$ python lotsofmenus.py
    added menu items!
```

Note: app needs a G+ client secrets file called `client_secrets.json`.

## Routes

### Random restaurant
/restaurants/random, /

![random-rest](images/random-rest.png)

### Show all restaurants
/restaurants

![restaurants](images/restaurants.png)

### Create new restaurant
/restaurant/new

![new-rest](images/new-rest.png)

### Edit a restaurant
/restaurant/<int:rest_id>/edit

![edit-rest](images/edit-rest.png)

### Delete a restaurant
/restaurant/<int:rest_id>/delete

![delete-rest](images/delete-rest.png)

### Show a restaurant menu
/restaurant/<int:rest_id>/menu, /restaurant/<int:rest_id>

![menu](images/menu.png)

### Create a new menu item
/restaurant/<int:rest_id>/menu/new

![add-item](images/add-item.png)

### Edit a menu item
/restaurant/<int:rest_id>/menu/<int:menu_id>/edit

![edit-item](images/edit-item.png)

### Delete a menu item
/restaurant/<int:rest_id>/menu/<int:menu_id>/delete

![delete-item](images/delete-item.png)
