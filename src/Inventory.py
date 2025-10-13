from multiprocessing import process
import csv, os
from datetime import date, timedelta
from tkinter import filedialog, simpledialog, messagebox
from . import ShoppingCart

inventory = []

#To translate, edit these dialogs.
error_no_inventory = "No se encontro archivo de inventario, por favor, seleccione uno."
open_inventory_file_dialog = "Abrir archivo de inventario."
message_loaded_inventory = "Inventario cargado exitosamente."

from .Product import Product

current_date = date.today()
previous_date = current_date - timedelta(days=1)
directory_path = "./inventories/"
filename = "Inventario " + str(current_date) + ".csv"
previous_filename = "Inventario " + str(previous_date) + ".csv"
fieldnames = ['ID', 'Barcode', 'Name', 'Price', 'Quantity', 'Cost']

def load_inventory():
    #Creates inventory directory if it doesn't exist.
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    
    if os.path.exists(directory_path + filename):
        inventory = processInventoryFile(directory_path + filename)
    elif os.path.exists(directory_path + previous_filename):
        inventory = processInventoryFile(directory_path + previous_filename)
    else:
        print(error_no_inventory)
        fileToProcess = filedialog.askopenfilename(
            title = open_inventory_file_dialog,
            filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        inventory = processInventoryFile(fileToProcess)
    return inventory
    
def processInventoryFile(filePath):
    with open(filePath, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            product_id = row[0].strip()
            barcode = row[1].strip()
            name = row[2].strip()
            price = row[3].strip()
            quantity = int(row[4].strip())
            cost = row[5].strip()
            product = Product(product_id, barcode, name, price, quantity, cost)
            inventory.append(product)
    return inventory

def save_inventory(inventory):
    with open(directory_path + filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fieldnames)  # Write header
        for product in inventory:
            csv_writer.writerow([product.product_id, product.barcode, product.name, product.price, product.quantity, product.cost])
    return inventory

def substract_sale_from_inventory(shoppingCart):
    for product in shoppingCart:
        for item in inventory:
            if product.barcode == item.barcode:
                item.quantity -= product.quantity
                return
            
def add_new_product_to_inventory(new_product, inventory):
    inventory.append(new_product)
    return inventory

def define_new_product(inventory):
    product_id = simpledialog.askstring("Nuevo Producto", "Ingrese el ID del producto (dejar en blanco si no aplica):", initialvalue="")
    barcode = simpledialog.askstring("Nuevo Producto", "Ingrese el codigo de barras del producto (dejar en blanco si no aplica):", initialvalue="")
    name = simpledialog.askstring("Nuevo Producto", "Ingrese el nombre del producto:", initialvalue="Producto Nuevo")
    digit = False
    while not digit:
        price = simpledialog.askstring("Nuevo Producto", "Ingrese el precio del producto:", initialvalue="$1000")
        try:
            price_int = ShoppingCart.price_to_int(price)  # Attempt to convert to integer
            digit = True
        except ValueError:
            messagebox.showwarning("Precio Invalido", "El precio debe ser un numero entero.")

    digit = False
    while not digit:
        quantity_str = simpledialog.askstring("Nuevo Producto", "Ingrese la cantidad del producto:", initialvalue="1")
        try:
            quantity = int(quantity_str)
            digit = True
        except ValueError:
            messagebox.showwarning("Cantidad Invalida", "La cantidad debe ser un numero entero.")
    
    cost = simpledialog.askstring("Nuevo Producto", "Ingrese el costo del producto (dejar en blanco si no aplica):", initialvalue="")
    
    if name is None or name == '' or price is None or price == '' or quantity_str is None or quantity_str == '':
        return None
    
    
    new_product = Product(product_id, barcode, name, price, quantity, cost)
    inventory = add_new_product_to_inventory(new_product, inventory)
    return inventory

def quick_define_new_product(inventory):
    name = simpledialog.askstring("Nuevo Producto", "Ingrese el nombre del producto:", initialvalue="Producto Nuevo")
    digit = False
    while not digit:
        price = simpledialog.askstring("Nuevo Producto", "Ingrese el precio del producto:", initialvalue="$1000")
        try:
            price_int = ShoppingCart.price_to_int(price)  # Attempt to convert to integer
            digit = True
        except ValueError:
            messagebox.showwarning("Precio Invalido", "El precio debe ser un numero entero.")

    if name is None or name == '' or price is None or price == '':
        return None
    
    new_product = Product("", "", name, price, 1, "")
    inventory = add_new_product_to_inventory(new_product, inventory)
    return inventory