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
            search_term = simpledialog.askstring("Añadir al Carrito", "Ingrese el codigo de barras o nombre del producto a añadir:")
            if search_term is None or search_term == '':
                continue
            else:
                addToCart(search(search_term))

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

        elif search(action) != None:
            addToCart(search(action))
            continue

load_inventory()
load_sales_file()
save()
menu()


