import mysql.connector

HOSTNAME = 'localhost'
USERNAME = 'db'
PASSWORD = 'zEtSfaHDjTGh6Sb5'
DATABASE = 'db'
PORT = 3306

class MenuItem():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def connect(self):
        """Connect to the MySQL database."""
        try:
            self.connection = mysql.connector.connect(
                host=HOSTNAME,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE,
                port=PORT
            )
            self.cursor = self.connection.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
        return self.cursor

    def disconnect(self):
        """Disconnect from the database."""
        try:
            self.cursor.close()
            self.connection.close()
        except mysql.connector.Error as e:
            print(f"Error disconnecting from the database: {e}")

    def save(self):
        """Save the menu item to the database."""
        self.connect()
        print("Connect to database")
        try:
            print("Entre try")
            query = "INSERT INTO menu_item (item_name, item_price) VALUES (%s, %s)"
            self.cursor.execute(query, (self.name, self.price))
            self.connection.commit()
            print(f"Menu item saved: {self.name}, {self.price}")
        except mysql.connector.Error as e:
            print(f"Error saving the menu item: {e}")
        finally:
            self.disconnect()

    def update(self, name=None, price=None):
        """Update the menu item in the database."""
        if name is None and price is None:
            return

        new_name = name if name is not None else self.name
        new_price = price if price is not None else self.price

        self.connect()

        try:
            query = "UPDATE menu_item SET item_name = %s, item_price = %s WHERE item_name = %s"
            self.cursor.execute(query, (new_name, new_price, self.name))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                old_name = self.name
                self.name = new_name
                self.price = new_price
                print(f"Menu item updated: {old_name} -> {self.name}, {self.price}")
            else:
                print(f"No rows affected when updating {self.name}")
        except mysql.connector.Error as e:
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
        except mysql.connector.Error as e:
            print(f"Error deleting the menu item: {e}")
        finally:
            self.disconnect()
