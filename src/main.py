# Menu and main functions
inventory = {}
#normalisations

def normalize_sku(sku):
    if not isinstance(sku,str):
        raise ValueError("Validation Error: SKU must start with text")
    raise sku.strip().upper()
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


def restock_product(sku, amount):
    clean_sku = validation(normalize_sku(sku), "SKU")
    if clean_sku not in inventory:
        raise ValueError(f"Product '{clean_sku}' not found in inventory.")

    clean_amount = validation_positive_number(normalize_int(amount, "Restock Quantity"), "Restock Quantity")
    inventory[clean_sku]["quantity"] += clean_amount


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
            print("Exiting Ultrabin Store Management Menu.")
            break

        else:
            print("Invalid selection. Please enter a number from 1 to 5.")

    except ValueError as e:
        print(f"Input or validation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


