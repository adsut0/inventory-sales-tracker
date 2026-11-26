# Menu and main functions
from datetime import datetime
# Synthetic data only to be used until a permanent structure/json data can be made
inventory = {
    "PRDT-001": {
        "name": "Grapes",
        "category": "Groceries",
        "unit_price": 3.49,
        "quantity": 5,
        "low_stock_threshold": 10,
        "active_status": True
    },
    "PRDT-002": {
        "name": "Apples",
        "category": "Groceries",
        "unit_price": 5.99,
        "quantity": 5,
        "low_stock_threshold": 7,
        "active_status": True
    },
    "PRDT-003": {
        "name": "Milk",
        "category": "Groceries",
        "unit_price": 6.99,
        "quantity": 5,
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
class Product:
    def __init__(self, sku, name, category, unit_price, quantity, low_stock_threshold, active_status=True):
        self.sku = validation(normalize_sku(sku), "SKU")
        self.name = validation(normalize_text(name), "Product Name")
        self.category = validation(normalize_text(category), "Category")
        self.unit_price = validation_positive_number(normalize_price(unit_price), "Unit Price")
        self.quantity = int(validation_nonnegative_number(normalize_int(quantity, "Quantity"), "Quantity"))
        self.low_stock_threshold = int(
            validation_nonnegative_number(normalize_int(low_stock_threshold, "Low Stock Threshold"),
                                          "Low Stock Threshold"))
        self.active_status = bool(active_status)

    def restock(self, amount):
        clean_amount = validation_positive_number(normalize_int(amount, "Restock Quantity"), "Restock Quantity")
        self.quantity += clean_amount

    def update_fields(self, **updates):
        field_rules = {
            "name": (normalize_text, validation, "Product Name"),
            "category": (normalize_text, validation, "Category"),
            "unit_price": (normalize_price, validation_positive_number, "Unit Price"),
            "quantity": (normalize_int, validation_nonnegative_number, "Quantity"),
            "low_stock_threshold": (normalize_int, validation_nonnegative_number, "Low Stock Threshold"),
        }

        for field, value in updates.items():
            if field in field_rules:
                normalizer, validator, label = field_rules[field]

                if field in ["quantity", "low_stock_threshold", "unit_price"]:
                    normalized = normalizer(value, label)
                else:
                    normalized = normalizer(value)

                cleaned_value = validator(normalized, label)

                if field in ["quantity", "low_stock_threshold"]:
                    cleaned_value = int(cleaned_value)

                setattr(self, field, cleaned_value)
            elif field == "active_status":
                self.active_status = bool(updates["active_status"])


class InventoryManager:
    def __init__(self, initial_data=None):
        self.inventory = {}
        self.sales = []

        if initial_data:
            self._load_legacy_data(initial_data)

    def _load_legacy_data(self, data):
        for sku, item in data.items():
            self.inventory[sku] = Product(
                sku=sku,
                name=item["name"],
                category=item["category"],
                unit_price=item["unit_price"],
                quantity=item["quantity"],
                low_stock_threshold=item["low_stock_threshold"],
                active_status=item["active_status"]
            )

    def add_product(self, sku, name, category, unit_price, quantity, low_stock_threshold, active_status=True):
        temp_sku = validation(normalize_sku(sku), "SKU")
        if temp_sku in self.inventory:
            raise ValueError(f"Product '{temp_sku}' already exists.")

        new_product = Product(sku, name, category, unit_price, quantity, low_stock_threshold, active_status)
        self.inventory[new_product.sku] = new_product

    def search_products(self, query):
        clean_query = query.strip().upper()
        results = [p for sku, p in self.inventory.items() if clean_query in sku or clean_query in p.name.upper()]
        return results

    def restock_product(self, sku, amount):
        clean_sku = validation(normalize_sku(sku), "SKU")
        if clean_sku not in self.inventory:
            raise ValueError(f"Product '{clean_sku}' not found in inventory.")
        self.inventory[clean_sku].restock(amount)

    def record_sale(self, sku, quantity_sold):
        clean_sku = validation(normalize_sku(sku), "SKU")
        qty = int(validation_positive_number(normalize_int(quantity_sold, "Quantity Sold"), "Quantity Sold"))

        if clean_sku not in self.inventory:
            raise ValueError(f"Product '{clean_sku}' not found.")

        product = self.inventory[clean_sku]
        if not product.active_status:
            raise ValueError("Cannot sell an inactive product.")
        if product.quantity < qty:
            raise ValueError(f"Insufficient stock. Only {product.quantity} available.")

        product.quantity -= qty
        total_amount = round(product.unit_price * qty, 2)

        self.sales.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sale_id": f"sale-{int(datetime.now().timestamp())}",
            "product_name": product.name,
            "quantity_sold": qty,
            "total_amount": total_amount
        })
        print(f"Sale successful! Total: ${total_amount:.2f}")

    def update_product(self, sku, **updates):
        clean_sku = validation(normalize_sku(sku), "SKU")
        if clean_sku not in self.inventory:
            raise KeyError(f"Product '{clean_sku}' not found.")
        self.inventory[clean_sku].update_fields(**updates)

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
    for sale in sorted(sales, key=lambda x: x["timestamp"]):
        total_revenue += sale["total_amount"]
        print(f"{sale['timestamp']} | {sale['transaction_id']} | {sale['product_name']} x{sale['quantity_sold']} | ${sale['total_amount']:.2f}")
    print(f"Total Revenue: ${total_revenue:.2f}")

# COMMAND LINE MENU
store = InventoryManager(inventory)
while True:
    print("\n========= Ultrabin Store Management Menu =========")
    print("1. Add product")
    print("2. Product search")
    print("3. Restocking")
    print("4. Recording a sale")
    print("5. Product Update")
    print("6. Inventory report")
    print("7. Low stock report")
    print("8. Sales report")
    print("9. Exit")
    choice = input("Enter your selection: ")

    try:
        # ADD PRODUCT
        if choice == "1":
            sku = input("Enter SKU: ")
            name = input("Enter product name: ")
            category = input("Enter product category: ")
            price = input("Enter unit price: ")
            qty = input("Enter unit quantity: ")
            threshold = input("Enter low stock threshold: ")
            active_input = input(
                "Confirm whether product is active (True or False): "
            ).strip().lower()

            active_status = active_input == "true"
            store.add_product(
                sku, name, category, price,
                qty, threshold, active_status
            )
            print("Product added successfully!")

        # PRODUCT SEARCH
        elif choice == "2":
            query = input("Enter SKU or product name: ")

            results = store.search_products(query)

            if results:
                print(f"\nFound {len(results)} matching product(s):")

                for product in results:
                    print(f"\nSKU: {product.sku}")
                    print(f"Name: {product.name}")
                    print(f"Category: {product.category}")
                    print(f"Price: ${product.unit_price:.2f}")
                    print(f"Quantity: {product.quantity}")
                    print(f"Active: {product.active_status}")
            else:
                print("No products found.")

        # RESTOCK PRODUCT
        elif choice == "3":
            sku = input("Enter SKU to restock: ")
            amount = input("Enter quantity to add: ")
            store.restock_product(sku, amount)
            print("Product restocked successfully!")

        # RECORD SALE
        elif choice == "4":
            sku = input("Enter SKU sold: ")
            amount = input("Enter quantity sold: ")

            store.record_sale(sku, amount)

        # UPDATE PRODUCT
        elif choice == "5":
            sku = input("Enter SKU of product to update: ")
            print("Leave any field blank to keep its current value.")

            updates = {}
            name = input("New product name: ").strip()
            category = input("New category: ").strip()
            price = input("New unit price: ").strip()
            qty = input("New quantity: ").strip()
            threshold = input("New low stock threshold: ").strip()

            if name:
                updates["name"] = name
            if category:
                updates["category"] = category
            if price:
                updates["unit_price"] = price
            if qty:
                updates["quantity"] = qty
            if threshold:
                updates["low_stock_threshold"] = threshold
            store.update_product(sku, **updates)
            print("Product updated successfully!")

        # INVENTORY REPORT
        elif choice == "6":
            print("\n--- COMPLETE INVENTORY ---")
            total_value = 0
            for sku, product in sorted(store.inventory.items()):
                if product.active_status:
                    value = product.unit_price * product.quantity
                    total_value += value
                    print(
                        f"{sku} | {product.name} | "
                        f"{product.category} | "
                        f"${product.unit_price:.2f} | "
                        f"Qty: {product.quantity} | "
                        f"Value: ${value:.2f}"
                    )
            print(f"Total Inventory Value: ${total_value:.2f}")

        # LOW STOCK REPORT
        elif choice == "7":
            print("\n--- LOW STOCK ALERTS ---")
            found = False
            for sku, product in sorted(store.inventory.items()):
                if (product.active_status and
                    product.quantity <= product.low_stock_threshold):
                    found = True
                    print(
                        f"{sku} | {product.name} | "
                        f"Stock: {product.quantity} | "
                        f"Threshold: {product.low_stock_threshold}"
                    )

            if not found:
                print("No low-stock items.")

        # SALES REPORT
        elif choice == "8":
            print("\n--- SALES HISTORY ---")
            if not store.sales:
                print("No sales recorded yet.")
            else:
                total_revenue = 0
                for sale in sorted(
                    store.sales,
                    key=lambda x: x["timestamp"]
                ):
                    total_revenue += sale["total_amount"]
                    print(
                        f"{sale['timestamp']} | "
                        f"{sale['transaction_id']} | "
                        f"{sale['product_name']} x"
                        f"{sale['quantity_sold']} | "
                        f"${sale['total_amount']:.2f}"
                    )
                print(f"Total Revenue: ${total_revenue:.2f}")

        # EXIT
        elif choice == "9":
            print("Exiting Ultrabin Store Management Menu.")
            break
        else:
            print("Invalid selection. Please enter a number from 1 to 9.")

    except ValueError as e:
        print(f"Input or validation error: {e}")

    except KeyError as e:
        print(f"Product error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
