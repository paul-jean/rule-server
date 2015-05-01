# Random restaurant

## Routes

### Show all restaurants
/restaurants, /

### Create new restaurant
/restaurant/new

### Edit a restaurant
/restaurant/<int:rest_id>/edit

### Delete a restaurant
/restaurant/<int:rest_id>/delete

### Show a restaurant menu
/restaurant/<int:rest_id>/menu, /restaurant/<int:rest_id>

### Create a new menu item
/restaurant/<int:rest_id>/menu/new

### Edit a menu item
/restaurant/<int:rest_id>/menu/<int:menu_id>/edit

### Delete a menu item
/restaurant/<int:rest_id>/menu/<int:menu_id>/delete
