from multiprocessing import process
import csv, os
from datetime import date, timedelta
from tkinter import filedialog

inventory = []

#To translate, edit these dialogs.
error_no_inventory = "No se encontro archivo de inventario, por favor, seleccione uno."
open_inventory_file_dialog = "Abrir archivo de inventario."
message_loaded_inventory = "Inventario cargado exitosamente."

class Product:
    def __init__(self, product_id, barcode, name, price, quantity, cost):
        self.product_id = product_id #WooCommerce or other store front ID.
        self.barcode = barcode #SKU
        self.name = name
        self.price = price
        self.quantity = quantity
        self.cost = cost

    def getProductID(self):
        return self.product_id
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

current_date = date.today()
previous_date = current_date - timedelta(days=1)
directory_path = "./inventories/"
filename = "Inventario " + str(current_date) + ".csv"
previous_filename = "Inventario " + str(previous_date) + ".csv"
fieldnames = ['ID', 'Barcode', 'Name', 'Price', 'Quantity', 'Cost']

def load_inventory():
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
    # Check if inventory directory exists before saving the file
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)

    with open(directory_path + filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fieldnames)  # Write header
        for product in inventory:
            csv_writer.writerow([product.product_id, product.barcode, product.name, product.price, product.quantity, product.cost])

def substract_sale_from_inventory(shoppingCart):
    for product in shoppingCart:
        for item in inventory:
            if product.barcode == item.barcode:
                item.quantity -= product.quantity
                return