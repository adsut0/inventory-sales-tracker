#Product bank
import re
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
#validations
def validation(val, field_name):
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"Validation Error: {field_name} cannot be empty.")
    return val.strip()

def validation_positive_number(val, field_name):
    if not isinstance(val, (int, float))  or val <= 0:
        raise ValueError(f"Validation Error: {field_name} must be a positive number.")
    return val

def validation_nonnegative_number(val, field_name=None):
    if not isinstance(val, (int, float)) or val < 0:
        raise ValueError(f"Validation Error: {field_name or 'Value'} must be 0 or greater.")
    return val

def update_stock_duplicate(self, new_stock: int):
    if self.quantity + new_stock < 0:
        raise ValueError("Resulting quantity must be >= 0")
    self.quantity += int(new_stock)

def print_product_state(sku, event_name):
    p = inventory[sku]
    is_low = p['quantity'] <= p['low_stock_threshold']
    print(f"--- State After: {event_name} ---")
    print(f"SKU: {sku}")
    print(f"Name: {p['name']}")
    print(f"Quantity: {p['quantity']} (Low Stock Alert: {is_low})")
    print(f"Active Status: {p['active_status']}\n")

def add_new_product(sku, name, category, unit_price, quantity, low_stock_threshold):
    if sku in inventory:
        raise ValueError(f"Rejected: Product {sku} Already Exists. Cannot create a duplicate")

    clean_sku = validation(sku, "SKU")
    clean_name = validation(name, "Product Name")
    clean_category = validation(category, "Category")
    clean_price = validation_positive_number(unit_price, "Unit Price")
    clean_qty = validation_nonnegative_number(quantity, "Quantity")
    clean_threshold = validation_nonnegative_number(low_stock_threshold, "Low Stock Threshold")

    # 3. Add to inventory if all validations pass
    inventory[clean_sku] = {
        "name": clean_name,
        "category": clean_category,
        "unit_price": clean_price,
        "quantity": int(clean_qty),
        "low_stock_threshold": int(clean_threshold),
        "active_status": True
    }
    print_product_state(clean_sku, "Product added successfully")
def process_sale_transaction(sku, requested_quantity):
    if sku not in inventory:
        raise KeyError(f"Rejected: '{sku}' does not exist")
    requested_quantity = validation_positive_number(requested_quantity, "Requested quantity")
    available_stock = inventory[sku]["quantity"]

    if requested_quantity > available_stock:
        raise ValueError(
            f"Rejected: requested {requested_quantity} units of {inventory[sku]['name']} ({sku}), "
            f"only {available_stock} are available"
        )
#synthetic product records
print_product_state("PRDT-001", "Initial Setup")
inventory["PRDT-002"]["quantity"] += 50
#print_product_state("PRDT-002", "Restock (+20 units)")
#inventory["PRDT-003"]["quantity"] -= 20
#print_product_state("PRDT-003", "Sale ( -20 units)")
process_sale_transaction("PRDT-003", 999)
#add_new_product("PRDT-004", '', 'Groceries', '99.99.', '100', '10')
#add_new_product("PRDT-001",'Grapes', 'Groceries', '3.49', '40', '10')
#print_product_state("PRDT-004", "Sale ( -99 units)")
