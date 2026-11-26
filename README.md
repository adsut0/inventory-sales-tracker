======Project Charter======
This is a project designed to facilatate Product management for the fictional Ultrabin store system
The program needs to be able to manage products based on an SKU system with a name, catagory, price, quantity,
low stock threshold, and finally an activity status.

The scope of this project as of now is ever changing and the project will have to constantly have portions of it rewriten
to better accomodate future furnishings 

======SKU Layout======
| SKU      | Name   | Catagory  | Unit Price | Quantity  | Low-stock Threshold  | Active status |
| PRDT-001 | Grapes | Groceries | 3.49       | 40        | 10                   | True |
| PRDT-002 | Apples | Groceries | 5.99       | 50        | 7                    | True |
| PRDT-003 | Milk   | Groceries | 6.99       | 70        | 15                   | True |

======Inventory line format====== 

~~**`[SKU] Name: [Name] | Cat: [Category] | Price: $[Unit Price] | Qty: [Quantity] [ALERT if Qty <= Threshold]`**

~~**`Example output`**

~~**`[PRDT-002] Name: Apples | [SKU] - [Name] x [Qty Sold] @ $[Unit Price] = $`**

~~**`Sales receipt line format`**

~~**`[SKU] - [Name] x [Qty Sold] @ $[Unit Price] = $[Subtotal]`**

~~**`PRDT-3 - Milk x 3 @ $6.99 = $20.97`**

~~**`======Acceptance verification======`**

~~**`Known sale: 3 Units`**

~~**`Expected remaining quantities: 14-3 = 11 (passes check)`**

~~**`Expected total: 3*3.49 = $10.47 (passes check)`**

=====Project Layout=====
imports
|-inventory
|normalisations
   |Class Product
	|--restock
	|--update_fields
   |Class InventoryManager
	|--#legacy data (temporary)
	|--add_product
	|--search_products
	|--restock_product
	|--record_sale
	|--update_product
|#prints(not a class)
|print_product_state
|inventory_report
|low_stock_report
|sales_report
MENU
===============   DEMO MENU     ================
=========Ultrabin Store Management Menu=========

	1. Add product
	2. Product search
	3. Restocking
	4. Recording a sale
	5. Product Update
	6. Product report
	7. Low stock report
	8. Sales report
	9. Exit

# enter number to make your choice, i.e 1-5

1. Is to create a product with the SKU, name, category, price, quantity, low stock thresh hold, and the status of the product
2. Simply enter the SKU of a product to search it in the system
3. restocking system to add more stock to an existing product, 
   just simply enter the sku of the product and the desired amount
4. works just like restocking but in reverse,
   when a sale is made, record it by entering the sku of the product and the amount sold
5. Updates an existing product with sku, name, catagory, price, quantity, and lowstock threshold
6. Prints a report of the full list of items currently in the inventory
7. Prints a report of all of the items currently within the low stock threshold limit
8. Prints a list of all past sales
9. does as it says just exits the program nice and cleanly

