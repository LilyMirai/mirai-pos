import tkinter as tk
from tkinter import messagebox, simpledialog
from src.Inventory import *
from src.Sales import *
from src.Search import *
from src.ShoppingCart import *

sale = None
shoppingCart = []
sales = []
inventory = []
menuString = '''Seleccione una accion:

1. Añadir producto al carrito.
2. Añadir producto personalizado al carrito.
3. Ver Carrito
4. Vaciar Carrito.
5. Comprar Carrito

6. Ver Ventas
7. Ver Reportes (No implementado)

8. Guardar
9. Guardar y salir
0. Salir sin guardar
'''

addInstructions = "\n- Para buscar, ingresa un nombre o codigo de barra -\n"

def save():
    save_inventory(inventory)
    save_sales_file(sales)

def menu():
    global shoppingCart, sales, inventory
    while True:

        if shoppingCart == []: #menu when cart is empty
            finalMenu = menuString + addInstructions
            action = simpledialog.askstring("Menu", finalMenu)

        else: #menu when cart has items, shows cart contents, price and total in a separate line at the end
            cart_contents = "\n".join([f"{prod.getName()} - {prod.getPrice()}" for prod in shoppingCart])
            total_price = sum([price_to_int(prod.getPrice()) for prod in shoppingCart])
            finalMenu = menuString + addInstructions + f"\nCarrito:\n\n{cart_contents}\n\nPrecio Total: {total_price}"
            action = simpledialog.askstring("Menu", finalMenu)
        
        if action is None or action == '': #if cancelled or empty, loop
            continue

        elif action == '0': #exit without saving
            if messagebox.askyesno("Salir sin guardar", "¿Está seguro que desea salir sin guardar?"):
                break
        elif action == '9': #save and exit
            if not messagebox.askyesno("Guardar y salir", "¿Está seguro que desea guardar y salir?"):
                continue
            closing_statement(sales)
            save()
            break
        elif action == '8': #save
            closing_statement(sales)
            save()
            continue

        elif action == '1':
            search_term = look_up_menu()
            product = search(search_term)
            if product != None:
                shoppingCart = add_to_cart(product, shoppingCart)

        elif action == '2': #Add Custom Product
            shoppingCart = add_custom_product_to_cart(shoppingCart)

        elif action == '3': #Ver Carrito
            view_cart(shoppingCart)

        elif action == '4': #Vaciar Carrito
            shoppingCart = empty_shopping_cart(shoppingCart)

        elif action == '5': #Comprar Carrito
            result = buy_shopping_cart(shoppingCart, sales)
            if result != False:
                sales = result
                substract_sale_from_inventory(shoppingCart)
                shoppingCart = empty_shopping_cart(shoppingCart)
                messagebox.showinfo("Compra Exitosa", "Gracias por su compra.\nPega el contenido del portapapeles en la hoja de calculo.")
                save_inventory(inventory)
                save_sales_file(sales)
                sale = None
            else:
                continue

        elif action == '6': #Ver Ventas
            return_sales(sales)

        else:
            product = search(action)
            if product != None:
                shoppingCart = add_to_cart(product, shoppingCart)

inventory = load_inventory()
sales = load_sales_file()
save()
menu()


