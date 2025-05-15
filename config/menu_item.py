import psycopg2

HOSTNAME = 'localhost'
USERNAME = 'postgres'
PASSWORD = 'shab1991'
DATABASE = 'restaurant'
PORT = "5432"
class MenuItem():
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    def connect(self):
        """Connect to the database."""
        try:
            self.connection = psycopg2.connect(host=HOSTNAME, user=USERNAME, password=PASSWORD, dbname=DATABASE )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return None
        return self.cursor
    
    def disconnect(self):
        """Disconnect from the database."""
        try:
            self.cursor.close()
            self.connection.close()
        except Exception as e:
            print(f"Error disconnecting from the database: {e}")

    def save(self):
        """Save the menu item to the database."""
        self.connect()
        try:
            query = "INSERT INTO menu_item (item_name, item_price) VALUES (%s, %s)"
            self.cursor.execute(query, (self.name, self.price))
            self.connection.commit()
            print(f"Menu item saved: {self.name}, {self.price}")
        except Exception as e:
            print(f"Error saving the menu item: {e}")
        finally:
            self.disconnect()

    def update(self, name=None, price=None):
        """Update the menu item in the database."""
        if name is None and price is None:
            print("No new values provided for update.")
            return
        
        self.connect()

        try:
            query = "UPDATE menu_item SET item_name = %s, item_price = %s WHERE item_name = %s"
            self.cursor.execute(query, (name, price, self.name))
            self.connection.commit()
        except Exception as e:
            print(f"Error updating the menu item: {e}")
        finally:
            self.disconnect()

    def delete(self):
        """Delete the menu item from the database."""
        self.connect()
        try:
            query = "DELETE FROM menu_item WHERE item_name = %s"
            self.cursor.execute(query, (self.name,))
            self.connection.commit()
            print(f"Menu item deleted: {self.name}")
        except Exception as e:
            print(f"Error deleting the menu item: {e}")
        finally:
            self.disconnect()


