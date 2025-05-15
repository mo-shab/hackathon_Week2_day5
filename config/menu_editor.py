from config.menu_item import MenuItem
from config.menu_manager import MenuManager

def show_user_menu():
    print("V: View an Item (V)")
    print("A: Add an Item (A)")
    print("D: Delete an Item (D)")
    print("U: Update an Item (U)")
    print("S: Show the Menu (S)")
    print("Q: Quit (Q)")
    print("Please select an option (V, A, D, U, S, Q): ", end="")
    
    choice = input().strip().upper()
    while choice is not 'Q':
        match choice:
            case 'V':
                print("View an Item")
                name = input("Enter the name of the item to view: ")
                item = MenuManager.get_by_name(name)
                if item:
                    print(f"Item found: {item.name}, {item.price}")
                else:
                    print("Item not found.")
            case 'A':
                print("Add an Item")
                add_item_to_menu()
            case 'D':
                print("Delete an Item")
                remove_item_from_menu()    
            case 'U':
                print("Update an Item")
                update_item_from_menu()
            case 'S':
                print("Show the Menu")
                show_restaurant_menu()
            case 'Q':
                print("Quit")
                show_restaurant_menu()
                return
            case _:
                print("Invalid option. Please try again.")
                show_restaurant_menu()
        choice = input("Please select an option (V, A, D, U, S, Q): ").strip().upper()
    
def add_item_to_menu():
    print("Add an Item to the Menu")
    name = input("Enter the name of the item: ")
    price = float(input("Enter the price of the item: "))
    item = MenuItem(name, price)
    item.save()
    print(f"Item added: {item.name}, {item.price}")

def remove_item_from_menu():
    print("Remove an Item from the Menu")
    name = input("Enter the name of the item to remove: ")
    item = MenuManager.get_by_name(name)
    if item:
        item.delete()
        print(f"Item removed: {item.name}")
    else:
        print("Item not found.")

def update_item_from_menu():
    print("Update an Item in the Menu")
    name = input("Enter the name of the item to update: ")
    item = MenuManager.get_by_name(name)
    if item:
        new_name = input("Enter the new name of the item (leave blank to keep current): ")
        new_price = input("Enter the new price of the item (leave blank to keep current): ")
        if new_price:
            new_price = float(new_price)
        else:
            new_price = None
        item.update(new_name, new_price)
        print(f"Item updated: {item.name}, {item.price}")
    else:
        print("Item not found.")

def show_restaurant_menu():
    print("Restaurant Menu")
    print("Showing all items in the menu...")
    items = MenuManager.all_items()
    for item in items:
        print(f"Item: {item.name}, Price: {item.price}")

if __name__ == "__main__":
    show_user_menu()