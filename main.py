import csv, os
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import date, timedelta

#orden csv entrante: codigo, nombre, precio, inventario, descripcion, siniva, coniva, venta, final

#Startup - Creacion de Variables

directory_path = "./inventories/"
current_date = date.today()
previous_date = current_date - timedelta(days=1)
filename = "Inventario " + str(current_date) + ".csv"
filename_previous = "Inventario " + str(previous_date) + ".csv"
file_exists = 0 #0 doesn't exist, 1 exists, 2 previous exists.
shoppingCart = []

def openInventoryFile():
    if os.path.exists(directory_path + filename):
        file_exists = 1
        processInventoryFile(directory_path + filename)
    elif os.path.exists(directory_path + filename_previous):
        file_exists = 2
        processInventoryFile(directory_path + filename_previous)
    else:
        file_exists = 0
        print("No se encontro un archivo de inventario. Importe uno.")
        fileToProcess = filedialog.askopenfilename(
            title = "Abrir archivo de Inventario",
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        )
        processInventoryFile(fileToProcess)

Products = []
class Product:
    def __init__(self, barcode, name, price, quantity, description, siniva, coniva, venta, final):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.siniva = siniva
        self.coniva = coniva
        self.venta = venta
        self.final = final

    def getBarcode(self):
        return self.barcode
    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getQuantity(self):
        return self.quantity
    def getDescription(self):
        return self.description
    
    def addQuantity(self, amount):
        self.quantity += amount
    def addOne(self):
        self.quantity += 1
    def removeOne(self):
        self.quantity -= 1
    def setPrice(self, new_price):
        self.price = new_price

def processInventoryFile(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if present
        for row in csv_reader:
            barcode = row[0].strip()
            name = row[1].strip()
            price = row[2].strip()
            quantity = int(row[3].strip())
            description = row[4].strip()
            siniva = row[5].strip()
            coniva = row[6].strip()
            venta = row[7].strip()
            final = row[8].strip()
            productToAdd = Product(barcode, name, price, quantity, description, siniva, coniva, venta, final)
            Products.append(productToAdd)
    print("Archivo de inventario procesado exitosamente.")

def lookUpProduct():
    barcode_to_lookup = simpledialog.askstring("Buscar Producto", "Ingrese el codigo de barras del producto:")
    for product in Products:
        if product.getBarcode() == barcode_to_lookup:
            messagebox.showinfo("Producto Encontrado", f"Nombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}\nDescripcion: {product.getDescription()}")
            return
    messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")

def quickLookUpProduct(barcode):
    for product in Products:
        if product.getBarcode() == barcode:
            messagebox.showinfo("Producto Encontrado", f"Nombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}\nDescripcion: {product.getDescription()}")
            return
    messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")

def emptyShoppingCart():
    shoppingCart = []

def addToCart(product):
    shoppingCart.append(product)

def removeFromCart(product):
    if product in shoppingCart:
        shoppingCart.remove(product)
    else:
        print("Producto no encontrado en el carrito.")

def substractProductsFromInventory():
    for prod in shoppingCart:
        for item in Products:
            if prod.getBarcode() == item.getBarcode():
                item.removeOne()
                break

def viewCart():
    cart_contents = "\n".join([f"{prod.getName()} - {prod.getPrice()}" for prod in shoppingCart])
    messagebox.showinfo("Carrito de Compras", f"Productos en el carrito:\n{cart_contents}")

def buyShoppingCart():
    total = 0
    for prod in shoppingCart:
        ammount = prod.getPrice()
        ammount = ammount.replace("$", "")
        ammount = ammount.replace(".", "")
        total += (int(ammount))
    messagebox.showinfo("Total a Pagar", f"El total a pagar es: ${total:,}")

def menu():
    while True:
        action = simpledialog.askstring("Menu", "Seleccione una accion:\n1. Buscar Producto\n2. Añadir producto al carrito. \n3. Ver Carrito \n4. Vaciar Carrito\n5. Comprar Carrito\n0. Salir")
        if action == '1':
            lookUpProduct()
        elif action == '2':
            barcode = simpledialog.askstring("Añadir al Carrito", "Ingrese el codigo de barras del producto a añadir:")
            for product in Products:
                if product.getBarcode() == barcode:
                    addToCart(product)
                    messagebox.showinfo("Añadido", f"{product.getName()} ha sido añadido al carrito.")
                    break
            else:
                messagebox.showwarning("No Encontrado", "Producto no encontrado en el inventario.")
        elif action == '3':
            viewCart()
        elif action == '4':
            emptyShoppingCart()
            messagebox.showinfo("Carrito Vaciado", "El carrito ha sido vaciado.")
        elif action == '5':
            buyShoppingCart()
            substractProductsFromInventory()
            emptyShoppingCart()
            messagebox.showinfo("Compra Exitosa", "Gracias por su compra.")
        elif action == '0':
            break
        elif int(action) > 5:
            quickLookUpProduct(action)



openInventoryFile()
menu()


