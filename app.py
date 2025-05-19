from flask import Flask, request, jsonify
from config.menu_item import MenuItem
from config.menu_manager import MenuManager
from flask_cors import CORS

app = Flask(__name__)


# More comprehensive CORS configuration
CORS(app)

@app.route('/api/test', methods=['GET'])
def test():
    return 'test'

@app.route('/api/menu', methods=['GET'])
def get_all_items():
    items = MenuManager.all_items()
    return jsonify([item.__dict__ for item in items])

@app.route('/api/item', methods=['POST'], strict_slashes=False)
@app.route('/api/item/<name>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def handle_item(name=None):
    if request.method == 'GET':
        item = MenuManager.get_by_name(name)
        if item:
            return jsonify(item.__dict__), 200
        return jsonify({"error": "Item not found"}), 404

    elif request.method == 'POST':
        print("POST Called")
        if request.is_json:
            data = request.get_json()
            print(data)
            name = data[0]['name']
            price = data[0]['price']
            print(f"Name : {name}, price {price}")

            if not name or price is None:
                return jsonify({"error": "Name and price are required"}), 400

            try:
                item = MenuItem(name, price)
                item.save()
                return jsonify({"message": "Item added"}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Request must be JSON"}), 400

    elif request.method == 'PUT':
        if request.is_json:
            data = request.get_json()
            new_name = data[0]['name']       # Access first element of array
            new_price = data[0]['price']

            if not new_name or new_price is None:
                return jsonify({"error": "New name and price are required"}), 400

            item = MenuManager.get_by_name(name)
            if item:
                try:
                    item.update(new_name, new_price)
                    return jsonify({"message": "Item updated"}), 200
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
            return jsonify({"error": "Item not found"}), 404
        return jsonify({"error": "Request must be JSON"}), 400

    elif request.method == 'DELETE':
        item = MenuManager.get_by_name(name)
        if item:
            try:
                item.delete()
                return jsonify({"message": "Item deleted"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
