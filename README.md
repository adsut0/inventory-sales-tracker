=====Project Charter=====

The Ultrabin systems management program In this python application you will be able to add, manage and track and manage Customers, products, revue and employees.

======SKU======

| SKU | Name | Catagory | Unit Price | Quantity  | Low-stock Threshold  | Active status |
| - | - | - | - | - | - | - |
| PRDT-001 | Grapes | Groceries | 3.49 | 40 | 10 | True  |
| PRDT-002 | Apples  | Groceries | 5.99 | 50 | 7 | True  |
| PRDT-003 | Milk  | Groceries | 6.99 | 70 | 15 | True |


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
