#psudocode for management

define add
add_new_product("sku","name", "catagory","price","quantity", "lowquantity")
	inventory += {ammount to be added}

define restock
restock_product(invetory("sku","quantity") 
	restock.quantity += {ammount to restocked}

define sale
product_sale("sku", "requested_quantity")
	product sale =- {requested_quantity}

define report
print_product_state["sku", "inventory"]
	
#all of these should be defined under a broader management section
#keeping them short and sweet is ideal aswell


