# #==== product bank ====#
# product_name = input("Please enter the product name: ")
# price = float(input("Please enter price: "))
# stock = int(input("Please enter stock count "))
#
# #cals
# total = round(price * stock, 2)
# print("--------------------------------------------")
# print(f"product: {product_name}")
# print(f"Total: ${total}")
# print("--------------------------------------------")

inventory = {
    "PRDT-001": {
        "name": "Grapes",
        "category": "Groceries",
        "unit_price": 3.49,
        "quantity": 40,
        "low_stock_threshold": 10,
        "active_status": True
    },
    "PRDT-002": {
        "name": "Apples",
        "category": "Groceries",
        "unit_price": 5.99,
        "quantity": 50,
        "low_stock_threshold": 7,
        "active_status": True
    },
    "PRDT-003": {
        "name": "Milk",
        "category": "Groceries",
        "unit_price": 6.99,
        "quantity": 70,
        "low_stock_threshold":15,
        "active_status": True
    }
}
def print_product_state(sku, event_name):
    p = inventory[sku]
    is_low = p['quantity'] <= p['low_stock_threshold']
    print(f"--- State After: {event_name} ---")
    print(f"SKU: {sku}")
    print(f"Name: {p['name']}")
    print(f"Quantity: {p['quantity']} (Low Stock Alert: {is_low})")
    print(f"Active Status: {p['active_status']}\n")
#synthetic product records
print_product_state("PRDT-001", "Initial Setup")
inventory["PRDT-002"]["quantity"] += 20
print_product_state("PRDT-002", "Restock (+20 units)")
inventory["PRDT-003"]["quantity"] -= 20
print_product_state("PRDT-003", "Sale ( -20 units)")