from flask import Flask, request, jsonify
from config.menu_item import MenuItem
from config.menu_manager import MenuManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/api/all_items', methods=['GET'])
def get_all_items():
    """Get all menu items."""
    items = MenuManager.all_items()
    return jsonify([item.__dict__ for item in items])

@app.route('/api/item/<name>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/api/item/', methods=['POST'])
def handle_item(name=None):
    """Handle menu item operations."""
    if request.method == 'GET':
        # Get a menu item by name
        item = MenuManager.get_by_name(name)
        if item:
            return jsonify(item.__dict__)
        else:
            return jsonify({"error": "Item not found"}), 404

    elif request.method == 'POST':
        # Add a new menu item
        if request.is_json:
            data = request.get_json()
            name = data[0]['name']
            price = data[0]['price']
            item = MenuItem(name, price)
            item.save()
            return jsonify({"message": "Item added"}), 201
        else:
            return jsonify({"error": "Request must be JSON"}), 400

    elif request.method == 'PUT':
        print(f"PUT request received for item: {name}")
        # Update an existing menu item
        if request.is_json:
            data = request.get_json()
            new_name = data[0]['name']
            new_price = data[0]['price']
            
            # Récupérer l'item à partir du nom dans l'URL
            item = MenuManager.get_by_name(name)
            
            if item:
                print(f"Item found: {item.name}, {item.price}")
                print(f"Updating to: {new_name}, {new_price}")
                
                # Mettre à jour avec le nouveau nom et prix
                item.update(new_name, new_price)
                
                print(f"Item updated successfully")
                return jsonify({"message": "Item updated"}), 200
            else:
                print(f"Item not found: {name}")
                return jsonify({"error": "Item not found"}), 404
        else:
            return jsonify({"error": "Request must be JSON"}), 400

    elif request.method == 'DELETE':
        # Delete a menu item
        item = MenuManager.get_by_name(name)
        if item:
            item.delete()
            return jsonify({"message": "Item deleted"}), 200
        else:
            return jsonify({"error": "Item not found"}), 404

@app.route('/api/menu', methods=['GET'])
def show_menu():
    """Show the restaurant menu."""
    items = MenuManager.all_items()
    return jsonify([item.__dict__ for item in items])

if __name__ == '__main__':
    app.run(debug=True)


