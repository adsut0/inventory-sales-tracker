# Menu and main functions

# Synthetic data only to be used until a permanent structure can be made
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

sales = []
# normalisations

def normalize_sku(sku):
    if not isinstance(sku,str):
        raise ValueError("Validation Error: SKU must start with text")
    return sku.strip().upper()
def normalize_text(text):
    if not isinstance(text, str):
        raise ValueError("ValidationError: Input must be text")
    return " ".join(text.strip().split()).title()
def normalize_price(price):
    try:
        return round(float(price), 2)
    except (ValueError, TypeError):
        raise ValueError("Validation Error: Price must be a valid number")
def normalize_int(val, field_name="Value"):
    try:
        return int(val)
    except (ValueError, TypeError):
        raise ValueError("Validation Error: Price must be a valid number")

#validations

def validation(val, field_name):
    if not isinstance(val, str) or not val.strip():
        raise ValueError(f"Validation Error: {field_name} cannot be empty.")
    return val.strip()
def validation_positive_number(val, field_name):
    if isinstance(val, bool) or not isinstance(val, (int, float)) or val <= 0:
        raise ValueError(f"Validation Error: {field_name} must be a positive number.")
    return val
def validation_nonnegative_number(val, field_name=None):
    if isinstance(val, bool) or not isinstance(val, (int, float)) or val < 0:
        raise ValueError(f"Validation Error: {field_name or 'Value'} must be 0 or greater.")
    return val

# product management functions
# ADDING NEW PRODUCT
def add_product(sku, name, category, unit_price, quantity, low_stock_threshold):
    clean_sku = validation(normalize_sku(sku), "SKU")
    if clean_sku in inventory:
        raise ValueError(f"Product '{clean_sku}' already exists.")

    clean_name = validation(normalize_text(name), "Product Name")
    clean_category = validation(normalize_text(category), "Category")
    clean_price = validation_positive_number(normalize_price(unit_price), "Unit Price")
    clean_qty = validation_nonnegative_number(normalize_int(quantity, "Quantity"), "Quantity")
    clean_threshold = validation_nonnegative_number(normalize_int(low_stock_threshold, "Low Stock Threshold"),"Low Stock Threshold")

    inventory[clean_sku] = {
        "name": clean_name,
        "category": clean_category,
        "unit_price": clean_price,
        "quantity": int(clean_qty),
        "low_stock_threshold": int(clean_threshold),
        "active_status": True
    }

# RESTOCK

def restock_product(sku, amount):
    clean_sku = validation(normalize_sku(sku), "SKU")
    if clean_sku not in inventory:
        raise ValueError(f"Product '{clean_sku}' not found in inventory.")

    clean_amount = validation_positive_number(normalize_int(amount, "Restock Quantity"), "Restock Quantity")
    inventory[clean_sku]["quantity"] += clean_amount

# PRODUCT UPDATE

def update_product(sku, **updates):
    clean_sku = validation(normalize_sku(sku), "SKU")
    if clean_sku not in inventory:
        raise KeyError(f"Product '{clean_sku}' not found.")


    field_rules = {
        "name": (normalize_text, validation, "Product Name"),
        "category": (normalize_text, validation, "Category"),
        "unit_price": (normalize_price, validation_positive_number, "Unit Price"),
        "quantity": (normalize_int, validation_nonnegative_number, "Quantity"),
        "low_stock_threshold": (normalize_int, validation_nonnegative_number, "Low Stock Threshold"),
    }

    validated_updates = {}
    for field, value in updates.items():
        if value is not None:
            normalizer, validator, label = field_rules[field]
            normalized_val = normalizer(value)
            validated_updates[field] = validator(normalized_val, label)
    validated_updates = {}
    for field, value in updates.items():
        if value is not None and field in field_rules:
            normalizer, validator, label = field_rules[field]
            normalized_val = normalizer(value)
            validated_updates[field] = validator(normalized_val, label)
    inventory[clean_sku].update(validated_updates)

# SALE

def record_sale(sku, amount):
    clean_sku = validation(normalize_sku(sku), "SKU")
    if clean_sku not in inventory:
        raise ValueError(f"Product '{clean_sku}' not found in inventory.")
    clean_amount = validation_positive_number(normalize_int(amount, "Sale Quantity"), "Sale Quantity")
    if inventory[clean_sku]["quantity"] < clean_amount:
        raise ValueError("Validation Error: Insufficient stock for sale.")

    inventory[clean_sku]["quantity"] -= clean_amount
    print_product_state(clean_sku, "Sale")

def update_stock_duplicate(self, new_stock: int):
    if self.quantity + new_stock < 0:
        raise ValueError("Resulting quantity must be >= 0")
    self.quantity += int(new_stock)

def search_products(query):
    clean_query = validation(query, "Search Query").lower()
    results = []

    for sku, details in inventory.items():
        if (clean_query in sku.lower() or
                clean_query in details["name"].lower() or
                clean_query in details["category"].lower()):
            results.append(sku)

    return results

#PRINT

def print_product_state(sku, event_name):
    clean_sku = sku.strip().upper()
    if clean_sku not in inventory:
        print(f"Error: SKU '{clean_sku}' not found.\n")
        return

    p = inventory[clean_sku]
    is_low = p['quantity'] <= p['low_stock_threshold']

    print(f"--- State After: {event_name} ---")
    print(f"SKU: {clean_sku}")
    print(f"Name: {p['name']}")
    print(f"Quantity: {p['quantity']} (Low Stock Alert: {is_low})")
    print(f"Active Status: {p['active_status']}\n")

# INVENTORY, LOW STOCK, AND SALES REPORT

def inventory_report(inventory):
    print("\n--- COMPLETE INVENTORY ---")
    total_value = 0
    for sku, item in sorted(inventory.items()):
        if item["active_status"]:
            value = item["unit_price"] * item["quantity"]
            total_value += value
            print(f"{sku} | {item['name']} ({item['category']}) | ${item['unit_price']:.2f} | Qty: {item['quantity']} | Value: ${value:.2f}")
    print(f"Total Inventory Value: ${total_value:.2f}")


def low_stock_report(inventory):
    print("\n--- LOW STOCK ALERTS ---")
    found = False
    for sku, item in sorted(inventory.items()):
        if item["active_status"] and item["quantity"] <= item["low_stock_threshold"]:
            found = True
            print(f"{sku} | {item['name']} | Stock: {item['quantity']} (Threshold: {item['low_stock_threshold']})")
    if not found:
        print("No low-stock items.")


def sales_report(sales):
    print("\n--- SALES HISTORY ---")
    if not sales:
        print("No sales recorded yet.")
        return

    total_revenue = 0
    for txn in sorted(sales, key=lambda x: x["timestamp"]):
        total_revenue += txn["total_amount"]
        print(f"{txn['timestamp']} | {txn['transaction_id']} | {txn['product_name']} x{txn['quantity_sold']} | ${txn['total_amount']:.2f}")
    print(f"Total Revenue: ${total_revenue:.2f}")

# command line menu

while True:
    print("\n=========Ultrabin Store Management Menu=========")
    print("1. Add product")
    print("2. Product search")
    print("3. Restocking")
    print("4. Recording a sale")
    print("5. Product Update")
    print("6. Product report")
    print("7. Exit")

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

            add_product(sku, name, category, price, qty, low_stock_threshold, active_status)

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
            sku = input("Enter SKU of product you would like to update: ")
            print("!Leave any field blank and press Enter to keep its current value!.")
            name = input("New product name: ").strip() or None
            category = input("New category: ").strip() or None
            price_str = input("New unit price: ").strip()
            qty_str = input("New quantity: ").strip()
            threshold_str = input("New low stock threshold: ").strip()
            unit_price = float(price_str) if price_str else None
            quantity = int(qty_str) if qty_str else None
            low_stock_threshold = int(threshold_str) if threshold_str else None
            update_product(
                sku,
                name=name,
                category=category,
                unit_price=unit_price,
                quantity=quantity,
                low_stock_threshold=low_stock_threshold,
            )
            print("Product updated successfully!")



        elif choice == "7":
            print("Exiting Ultrabin Store Management Menu.")
            break

        else:
            print("Invalid selection. Please enter a number from 1 to 5.")

    except ValueError as e:
        print(f"Input or validation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


