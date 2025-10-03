from Inventory import *
from tkinter import messagebox
from datetime import date

show_sales_title = "Ventas del dia."
show_sales_no_sales = "No hay ventas registradas hoy."
show_sales_sales = "Ventas Registradas: \n"

sales_directory_path = "./sales/"
sales_filename = "Ventas " + str(date.today()) + ".csv"
sales_fieldnames = ['Producto', 'Cantidad', 'Metodo de Pago']

class Sale:
    def __init__(self, product_name, ammount, kindOfPayment):
        self.product_name = product_name
        self.ammount = ammount
        self.kindOfPayment = kindOfPayment

    def getProductName(self):
        return self.product_name

    def getAmmount(self):
        return self.ammount

    def getKindOfPayment(self):
        return self.kindOfPayment
    
Sales = []

def add_to_sales(saleToAdd):
    Sales.append(saleToAdd)

def return_sales(sales):
    if not sales:
        messagebox.showinfo(show_sales_title, show_sales_no_sales)
        return
    total_sales = sum(sale.getAmmount() for sale in sales)
    sales_name_list = "\n\n".join([f"Venta: {sale.getAmmount()} - Metodo: {sale.getKindOfPayment()}" for sale in sales])
    messagebox.showinfo(show_sales_title, f"{show_sales_sales}{sales_name_list}\n\nTotal: {total_sales}")

def save_sales_file(sales):
    with open(sales_directory_path + sales_filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(sales_fieldnames)  # Write header
        for sale in sales:
            csv_writer.writerow([sale.getProductName(), sale.getAmmount(), sale.getKindOfPayment()])