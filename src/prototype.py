#==== product bank ====#
product_name = input("Please enter the product name: ")
price = float(input("Please enter price: "))
stock = int(input("Please enter stock count "))

#cals
total = round(price * stock, 2)
print("--------------------------------------------")
print(f"product: {product_name}")
print(f"Total: ${total}")
print("--------------------------------------------")
