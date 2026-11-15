# Menu and main functions
inventory = {}
# inventory = {
#     "PRDT-001": {
#         "name": "Grapes",
#         "category": "Groceries",
#         "unit_price": 3.49,
#         "quantity": 40,
#         "low_stock_threshold": 10,
#         "active_status": True
#     },
#     "PRDT-002": {
#         "name": "Apples",
#         "category": "Groceries",
#         "unit_price": 5.99,
#         "quantity": 50,
#         "low_stock_threshold": 7,
#         "active_status": True
#     },
#     "PRDT-003": {
#         "name": "Milk",
#         "category": "Groceries",
#         "unit_price": 6.99,
#         "quantity": 70,
#         "low_stock_threshold":15,
#         "active_status": True
#     }
# }
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

# product management functions

def update_stock_duplicate(self, new_stock: int):
    if self.quantity + new_stock < 0:
        raise ValueError("Resulting quantity must be >= 0")
    self.quantity += int(new_stock)


def restock_product(sku, amount):
    clean_sku = validation(sku, "SKU")
    if clean_sku not in inventory:
        raise ValueError(f"Product '{clean_sku}' not found in inventory.")
    clean_amount = validation_positive_number(amount, "Restock Quantity")
    inventory[clean_sku]["quantity"] += int(clean_amount)
    print_product_state(clean_sku, "Restock")


def record_sale(sku, amount):
    clean_sku = validation(sku, "SKU")
    if clean_sku not in inventory:
        raise ValueError(f"Product '{clean_sku}' not found in inventory.")
    product = inventory[clean_sku]
    if not product["active_status"]:
        raise ValueError(f"Cannot sell '{clean_sku}': Product is marked inactive.")
    clean_amount = int(validation_positive_number(amount, "Sale Quantity"))
    if product["quantity"] < clean_amount:
        raise ValueError(f"Insufficient stock. Available: {product['quantity']}, Requested: {clean_amount}.")
    product["quantity"] -= clean_amount
    print_product_state(clean_sku, "Sale Recorded")

def search_products(query):
    clean_query = validation(query, "Search Query").lower()
    results = []

    for sku, details in inventory.items():
        if (clean_query in sku.lower() or
                clean_query in details["name"].lower() or
                clean_query in details["category"].lower()):
            results.append(sku)

    return results

def print_product_state(sku, event_name):
    p = inventory[sku]
    is_low = p['quantity'] <= p['low_stock_threshold']
    print(f"--- State After: {event_name} ---")
    print(f"SKU: {sku}")
    print(f"Name: {p['name']}")
    print(f"Quantity: {p['quantity']} (Low Stock Alert: {is_low})")
    print(f"Active Status: {p['active_status']}\n")

def add_new_product(sku, name, category, unit_price, quantity, low_stock_threshold, status):
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

while True:
    print("\n=========Ultrabin Store Management Menu=========")
    print("1. Add product")
    print("2. Product search")
    print("3. Restocking")
    print("4. Recording a sale")
    print("5. Exit")

    choice = input("Enter your selection: ")
    try:
        if choice == "1":
            sku = input("Enter SKU: ")
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = float(input("Enter unit price: "))
            qty = int(input("Enter unit quantity: "))
            low_stock_threshold = int(input("Enter low stock threshold: "))
            active_input = input("Confirm whether product is active (True or False): ").strip().lower()
            active_status = active_input == "true"

            add_new_product(sku, name, category, price, qty, low_stock_threshold, active_status)

        elif choice == "2":
            query = input("Enter SKU of product: ")
            matching_sku = search_products(query)
            if matching_sku:
                print(f"\nFound {len(matching_sku)} matching product(s):")
                for sku in matching_sku:
                    print_product_state(sku, "Product Search")
            else:
                print("No products found.")

        elif choice == "3":
            sku = input("Enter SKU to restock: ")
            amount = int(input("Enter quantity to add: "))
            restock_product(sku, amount)

        elif choice == "4":
            sku = input("Enter SKU sold: ")
            amount = int(input("Enter quantity sold: "))
            record_sale(sku, amount)

        elif choice == "5":
            print("Exiting Ultrabin Store Management Menu.")
            break

        else:
            print("Invalid selection. Please enter a number from 1 to 5.")

    except ValueError as e:
        print(f"Input or validation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


