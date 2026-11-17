=====Project Charter=====

10/15 The Ultrabin systems management program In this python application you will be able to add, search, Restock, and sell products
10/26 prototype finalized
11/8 all applications for the ultrabin product management are in place and prototype is discarded
10/15 Repeating command line menu to select management applications
10/17 checkpoint normalisation should work as there dont seem to be any logic errors however i cannot record tests regarding such things until data can be recorded and saved in a json file
commit number like 7 idk 
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


=========Ultrabin Store Management Menu=========
1. Add product
2. Product search
3. Restocking
4. Recording a sale
5. Exit

# enter number to make your choice, i.e 1-5
1. Is to create a product with the SKU, name, category, price, quantity, low stock thresh hold, and the status of the product
2. Simply enter the SKU of a product to search it in the system
3. restocking system to add more stock to an existing product, 
   just simply enter the sku of the product and the desired amount
4. works just like restocking but in reverse,
   when a sale is made, record it by entering the sku of the product and the amount sold
5. does as it says just exits the program nice and cleanly

