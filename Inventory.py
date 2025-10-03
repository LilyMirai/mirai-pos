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
        self.product_id = product_id
        self.barcode = barcode
        self.name = name
        self.price = price
        self.quantity = quantity
        self.cost = cost

current_date = date.today()
previous_date = current_date - timedelta(days=1)
directory_path = "./inventories/"
filename = "Inventario " + str(current_date) + ".csv"
previous_filename = "Inventario " + str(previous_date) + ".csv"
fieldnames = ['ID', 'Barcode', 'Name', 'Price', 'Quantity', 'Cost']

def load_inventory():
    if os.path.exists(directory_path + filename):
        processInventoryFile(directory_path + filename)
    elif os.path.exists(directory_path + previous_filename):
        processInventoryFile(directory_path + previous_filename)
    else:
        print(error_no_inventory)
        fileToProcess = filedialog.askopenfilename(
            title = open_inventory_file_dialog,
            filetypes = [("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        processInventoryFile(fileToProcess)
    
def processInventoryFile(filePath):
    with open(filePath, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            product_id = row[0].strip()
            barcode = row[1].strip()
            name = row[2].strip()
            price = float(row[3].strip())
            quantity = int(row[4].strip())
            cost = float(row[5].strip())
            product = Product(product_id, barcode, name, price, quantity, cost)
            inventory.append(product)
    print(message_loaded_inventory)

def save_inventory():
    with open(directory_path + filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(fieldnames)  # Write header
        for product in inventory:
            csv_writer.writerow([product.product_id, product.barcode, product.name, product.price, product.quantity, product.cost])

