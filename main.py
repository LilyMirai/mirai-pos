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
5. Comprar Carrito.

6. Aplicar Descuento.

8. Ver Ventas.
9. Añadir producto al inventario.

0. Salir.
'''

addInstructions = "\n- Para buscar, ingresa un nombre o codigo de barra -\n"

def save(inventory, sales):
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

        elif action == '0': #save and exit
            if not messagebox.askyesno("Guardar y salir", "¿Está seguro que desea guardar y salir?"):
                continue
            closing_statement(sales)
            save(inventory, sales)
            break

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

        elif action == '6': #Aplicar Descuento
            #make user choose between percentage or ammount discount, then call for the proper function
            discount_type = simpledialog.askstring("Tipo de Descuento", "Ingrese '1' para descuento porcentual o '2' para descuento en monto fijo:")
            if discount_type == '1':
                shoppingCart = add_percentage_discount_to_product(shoppingCart)
            elif discount_type == '2':
                shoppingCart = add_ammount_discount_to_cart(shoppingCart)
            else:
                messagebox.showwarning("Tipo de Descuento Invalido", "Debe ingresar '1' o '2'.")
                continue

        elif action == '8': #Ver Ventas
            return_sales(sales)
        elif action == '9': #Agregar Producto
            if messagebox.askyesno('Agregar Producto', '¿Desea agregar un nuevo producto de forma detallada? (Si selecciona No, se le pedira solo nombre y precio, y la cantidad sera 1)'):
                inventory = define_new_product(inventory)
            else:
                inventory = quick_define_new_product(inventory)

        else:
            product = search(action)
            if product != None:
                shoppingCart = add_to_cart(product, shoppingCart)

inventory = load_inventory()
sales = load_sales_file()
save(inventory, sales)
menu()

