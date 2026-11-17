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
	        |, 'Groceries', '99.99.'        |	          | Product Name cannot be empty.
	       	| '100', '10')
================================================================================================================================
| oversell      | inventory["PRDT-003"]		| ValueError	  | ValueError: Rejected: requested 999 units of Milk (PRDT-003),
		|  ["quantity"] -= 999				  | only 70 are available
================================================================================================================================
