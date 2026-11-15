=====Project Charter=====

The Ultrabin systems management program In this python application you will be able to add, manage and track and manage Customers, products, revue and employees.

======SKU======
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

==Prototype tests (acceptance check)==
| Test          | Input                         | Expected result | Actual result |
================================================================================================================================
| sale          | "PRDT-003", "Sale (20 units)" | successful sale | --- State After: Sale ( -20 units) ---
                                                                    SKU: PRDT-003
                                                                    Name: Milk
                                                                    Quantity: 0 (Low Stock Alert: True)
                                                                    Active Status: True
================================================================================================================================
| duplicate SKU | #add_new_product("PRDT-001",  | ValueError      | ValueError: Rejected: Product PRDT-001 Already Exists. 
                | 'Grapes', 'Groceries', '3.49',|                 | Cannot create a duplicate
|               |    '40', '10')
================================================================================================================================
| blank name    | add_new_product("PRDT-004", ''| ValueError	  | ValueError: Validation Error: 
		        |, 'Groceries', '99.99.',	    |  		          | Product Name cannot be empty.
	        	| '100', '10')			        | 
================================================================================================================================
| oversell      | inventory["PRDT-003"]		| ValueError	  | ValueError: Rejected: requested 999 units of Milk (PRDT-003),
		|  ["quantity"] -= 999				  | only 70 are available
================================================================================================================================


=========Ultrabin Store Management Menu=========
1. add product
2. record a sale
3. invetory report
4. sales report 
5. save 
6. load
7. quit

# enter number to make your choice, i.e 1-5
