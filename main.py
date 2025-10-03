import csv, os, pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import date, timedelta
from Inventory import *
from Sales import *
from Search import *


#orden csv entrante: codigo, nombre, precio, inventario, descripcion, siniva, coniva, venta, final
 
onDevelopmentBranch = True

current_date = date.today()
previous_date = current_date - timedelta(days=1)
directory_path = "./inventories/"
sales_path = "./sales/"
filename = "Inventario " + str(current_date) + ".csv"
filename_previous = "Inventario " + str(previous_date) + ".csv"
sales_filename = "Ventas " + str(current_date) + ".csv"

shoppingCart = []
sale = None

Products = []
Sales = []

def lookUpProduct():
    barcode_to_lookup = simpledialog.askstring("Buscar Producto", "Ingrese el codigo de barras del producto:")
    if barcode_to_lookup != "":
        for product in Products:
            if product.getBarcode() == barcode_to_lookup:
                messagebox.showinfo("Producto Encontrado", f"Nombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}\nDescripcion: {product.getDescription()}")
                return
        messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")

def quickLookUpProduct(barcode):
    if barcode != "":
        for product in Products:
            if product.getBarcode() == barcode:
                messagebox.showinfo("Producto Encontrado", f"Nombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}\nDescripcion: {product.getDescription()}")
                return
        messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")

def nameSearch(name, mode):
    if name is None or name == '':
        return
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        if mode == 1:
            product_list = "\n".join([f"{prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for prod in found_products])
            messagebox.showinfo("Productos Encontrados", f"Productos que coinciden con '{name}':\n{product_list}")
        elif mode == 2:
            product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(found_products)])
            choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}':\n{product_list}\nIngrese el numero del producto a añadir al carrito:")
            if choice is None or choice == '':
                return
            if choice.isdigit() and 1 <= int(choice) <= len(found_products):
                selected_product = found_products[int(choice)-1]
                addToCart(selected_product)
            else:
                messagebox.showwarning("No Valido", "Seleccion invalida.")

def quickAddToCart(name):
    MAX_ELEMENTS_PAGE = 40;
    if name is None or name == '':
        return
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        # Paginacion
        current_page = 0;
        pages = [found_products[i:i+MAX_ELEMENTS_PAGE] for i in range (0, len(found_products), MAX_ELEMENTS_PAGE)]

        while(True):
            product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(pages[current_page])])
            choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}' (Pagina '{current_page+1}/{len(pages)}'):\n{product_list}\n\nEscape o Cancelar para salir\nAnterior o Siguiente para cambiar pagina\n\nPara añadir al carrito ingrese numero:")
            if choice is None or choice == '':
                return
            if choice.isdigit() == False:
                if choice.lower() == "anterior" or choice.lower() == "a":
                    current_page = max(0, current_page - 1)
                elif choice.lower() == "siguiente" or choice.lower() == "s":
                    current_page = min(len(pages) - 1, current_page + 1)
                elif choice.lower() == "escape" or choice.lower() == "cancelar":
                    return
            if choice.isdigit() and 1 <= int(choice) <= len(found_products):
                selected_product = found_products[int(choice)-1]
                addToCart(selected_product)
                return

def quickNameLookUp(name):
    #change messagebox for a prompt that asks if they want to add one of the listed items to cart, closing or clicking no returns to menu
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        product_list = "\n".join([f"{prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for prod in found_products])
        if messagebox.askyesno("Productos Encontrados", f"Productos que coinciden con '{name}':\n{product_list}\n¿Desea añadir alguno al carrito?"):
            addToCartFromName(name)
    else:
        messagebox.showwarning("No Encontrado", "No se encontraron productos que coincidan con el nombre.")

def addToCartFromName(name):
    if name is None or name == '':
        return
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(found_products)])
        choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}':\n{product_list}\nIngrese el numero del producto a añadir al carrito:")
        if choice is None or choice == '':
            return
        if choice.isdigit() and 1 <= int(choice) <= len(found_products):
            selected_product = found_products[int(choice)-1]
            addToCart(selected_product)
        else:
            messagebox.showwarning("No Valido", "Seleccion invalida.")

def addToCartFromBarcode(barcode):
    if barcode is None or barcode == '':
        return
    for product in Products:
        if product.getBarcode() == barcode:
            addToCart(product)
            return
    messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")

def emptyShoppingCart(shoppingCart):
    shoppingCart = []
    return shoppingCart

def addToCart(product):
    shoppingCart.append(product)

def removeFromCart(product):
    global shoppingCart
    if product in shoppingCart:
        shoppingCart.remove(product)
    else:
        print("Producto no encontrado en el carrito.")

def viewCart():
    cart_contents = "\n".join([f"{prod.getName()} - {prod.getPrice()}" for prod in shoppingCart])
    messagebox.showinfo("Carrito de Compras", f"Productos en el carrito:\n{cart_contents}")

def transformPriceToInt(price):
    ammount = price.replace("$", "")
    ammount = ammount.replace(".", "")
    return int(ammount)

def addCustomProductToCart():
    name = simpledialog.askstring("Nombre del Producto", "Ingrese el nombre del producto:", initialvalue="Cartas Sueltas")
    price = simpledialog.askstring("Precio del Producto", "Ingrese el precio del producto:", initialvalue="$1000")
    if name is None or name == '' or price is None or price == '':
        return
    product = Product('', name, price, 1, "Producto Personalizado", "", "", "", "")
    addToCart(product)

def defineKindOfSearch(input):
    if input is None or input == '':
        return False
    if input.isdigit() == False:
        quickAddToCart(input)
        return True
    elif int(input) > 5:
        quickLookUpProduct(input)
        return True
    return False

def closingStatement():
    if not Sales:
        messagebox.showinfo("Ventas", "No hay ventas registradas.")
        return
    ventasTotales = 0
    for venta in Sales:
        ventasTotales += venta.getAmmount()
    sales_list = "\n".join([f"Venta: {sale.getAmmount()} - Metodo: {sale.getKindOfPayment()}" for sale in Sales])
    messagebox.showinfo("Ventas Registradas", f"Ventas:\n{sales_list}\n\nTotal: {ventasTotales}")

menuString = "Seleccione una accion:\n\n1. Añadir producto al carrito. \n2. Añadir producto personalizado al carrito.\n\n3. Ver Carrito \n4. Vaciar Carrito\n5. Comprar Carrito\n\n6. Ver Ventas\n\n8. Guardar\n9. Guardar y salir\n0. Salir sin guardar\n"
addInstructions = "\n- Para buscar, ingresa un nombre o codigo de barra -\n"

def save():
    save_inventory()
    save_sales_file()


def menu():
    global shoppingCart
    while True:

        if shoppingCart == []: #menu when cart is empty
            finalMenu = menuString + addInstructions
            action = simpledialog.askstring("Menu", finalMenu)

        else: #menu when cart has items, shows cart contents, price and total in a separate line at the end
            cart_contents = "\n".join([f"{prod.getName()} - {prod.getPrice()}" for prod in shoppingCart])
            total_price = sum([transformPriceToInt(prod.getPrice()) for prod in shoppingCart])
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
            closingStatement()
            saveInventoryFile()
            break

        elif action == '8': #save
            closingStatement()
            save()
            continue

        elif action == '1':
            search = simpledialog.askstring("Añadir al Carrito", "Ingrese el codigo de barras o nombre del producto a añadir:")
            if search is None or search == '':
                continue
            if search.isdigit() == False:
                nameSearch(search, 2)
            else:
                addToCartFromBarcode(search)

        elif action == '2': #Add Custom Product
            addCustomProductToCart()

        elif action == '3': #Ver Carrito
            viewCart()

        elif action == '4': #Vaciar Carrito
            shoppingCart = emptyShoppingCart(shoppingCart)
            messagebox.showinfo("Carrito Vaciado", "El carrito ha sido vaciado.")

        elif action == '5': #Comprar Carrito
            if buy_shopping_cart(shoppingCart) != False:
                substract_sale_from_inventory(shoppingCart)
                shoppingCart = emptyShoppingCart(shoppingCart)
                messagebox.showinfo("Compra Exitosa", "Gracias por su compra.\nPega el contenido del portapapeles en la hoja de calculo.")
                save_inventory()
                save_sales_file()
                sale = None
            else:
                continue

        elif action == '6': #Ver Ventas
            return_sales(Sales)

        elif defineKindOfSearch(action): #if the input was a search, search, then skip the rest of the loop
            continue



load_inventory()
load_sales_file()
save()
menu()


