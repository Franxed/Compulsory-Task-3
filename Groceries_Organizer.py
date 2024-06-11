import sqlite3

def initialize_database():
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Foodstock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Shopping_list (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    ''')

    db.commit()
    db.close()

initialize_database()

def pantry_single(item, quantity):
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()
    cursor.execute('''INSERT INTO Foodstock (item, quantity) VALUES (?, ?)''', (item, quantity))
    db.commit()
    db.close()

def use_item(item, quantity, threshold=1):
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()
    cursor.execute('SELECT quantity FROM Foodstock WHERE item = ?', (item,))
    current_quantity = cursor.fetchone()

    if current_quantity:
        new_quantity = current_quantity[0] - quantity
        if new_quantity < threshold:
            cursor.execute('DELETE FROM Foodstock WHERE item = ?', (item,))
            cursor.execute('INSERT INTO Shopping_list (item, quantity) VALUES (?, ?)', (item, abs(new_quantity) + threshold))
        else:
            cursor.execute('UPDATE Foodstock SET quantity = ? WHERE item = ?', (new_quantity, item))
    else:
        print("Item not found in pantry.")

    db.commit()
    db.close()

def view_shopping_list():
    db = sqlite3.connect('Groceries_Database.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM Shopping_list')
    items = cursor.fetchall()
    db.close()
    return items

def main():
    while True:
        print("\n1. Add single item to pantry")
        print("2. Use an item from pantry")
        print("3. View shopping list")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            while True:
                item = input("Enter item name (or type 'exit' to return to menu): ")
                if item.lower() == 'exit':
                    break
                quantity = int(input("Enter quantity: "))
                pantry_single(item, quantity)
                save = input("Save and return to menu? (y/n): ")
                if save.lower() == 'y':
                    break

        elif choice == '2':
            item = input("Enter item name: ")
            quantity = int(input("Enter quantity used: "))
            threshold = int(input("Enter preferred threshold: "))
            use_item(item, quantity, threshold)

        elif choice == '3':
            shopping_list = view_shopping_list()
            print("\nShopping List:")
            for item in shopping_list:
                print(f"Item: {item[1]}, Quantity: {item[2]}")

        elif choice == '4':
            save = input("Save before exiting? (y/n): ")
            if save.lower() == 'y':
                print("Changes saved. Exiting.")
            else:
                print("Exiting without saving.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
