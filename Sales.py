from math import prod
from Inventory import *
from tkinter import messagebox, simpledialog
from datetime import * 
import pyperclip
import csv
import os

#Title for window showing all sales.
show_sales_title = "Ventas del dia."
#Message if no sales are present.
show_sales_no_sales = "No hay ventas registradas hoy."
#Message before showing all sales. Default: 'Sales: \n'
show_sales_sales = "Ventas Registradas: \n"

#Directory Path for Sales files.
sales_directory_path = "./sales/"
#Filename for sales files.
sales_filename = "Ventas " + str(date.today()) + ".csv"
#Field names for resulting saved file.
sales_fieldnames = ['Producto', 'Cantidad', 'Metodo de Pago']

#Message for clipboard message was copied. Default: "Sale copied to clipboard. \nDon't forget to paste it in spreadsheet!"
clipboard_copied_message = "Venta copiada al portapapeles. \nNo olvides pegarlo en sheets!"

#Total to pay message. Default: "The total to pay is: $X.XX"
total_to_pay_message = "El total a pagar es: $"
#Payment kind info message. Default: "What kind of payment will it be? (Cash, Card, etc.)"
payment_kind_info = "\nIngrese el metodo de pago:\ne. Efectivo\nd. Debito\nc. Credito\ntr. Transferencia\n\n0. Cancelar compra\n"
#Window Title for Payment input dialog. Default: "Total to pay"
payment_window_title = "Total a Pagar"    



class Sale:
    def __init__(self, product_name, price, kindOfPayment, time_of_sale = datetime.now().strftime("%H:%M:%S")):
        self.product_name = product_name
        self.price = price
        self.kindOfPayment = kindOfPayment
        self.time_of_sale = time_of_sale

    def getProductName(self):
        return self.product_name
    def getPrice(self):
        return self.price
    def getKindOfPayment(self):
        return self.kindOfPayment
    def getTimeOfSale(self):
        return self.time_of_sale
    def getProducts(self):
        return self.product_name
    

#Load sale file into memory.
def load_sales_file():
    if os.path.exists(sales_directory_path + sales_filename):
        return process_sales_file(sales_directory_path + sales_filename)
    else:
        with open(sales_directory_path + sales_filename, mode='x', newline='', encoding='utf-8') as salesfile:
            salesfile.write("Venta, Productos, Metodo de Pago, Monto, Hora\n")
        return process_sales_file(sales_directory_path + sales_filename)

def process_sales_file(file_path):
    sales = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            product_names = row[0].strip().split(" + ")
            products = []
            for name in product_names:
                for product in inventory:  # Assuming inventory is available globally
                    if product.getName() == name:
                        products.append(product)
                        break
            ammount = float(row[1].strip())
            kind_of_payment = row[2].strip()
            try:
                time_of_sale = row[3].strip()
            except IndexError:
                time_of_sale = None
            sale = Sale(products, ammount, kind_of_payment, time_of_sale)
            sales.append(sale)
    print("Returning sales from process sales file.")
    print(sales)
    return sales

#Adds a sale to the sales list.
def add_to_sales(saleToAdd, sales):
    sales.append(saleToAdd)
    return sales

#Shows all sales for the day in a messagebox.
def return_sales(sales):
    if not sales:
        messagebox.showinfo(show_sales_title, show_sales_no_sales)
        return
    total_sales = sum(sale.getPrice() for sale in sales)
    sales_name_list = "\n\n".join([f"Venta: {sale.getPrice()} - Metodo: {sale.getKindOfPayment()}" for sale in sales])
    messagebox.showinfo(show_sales_title, f"{show_sales_sales}{sales_name_list}\n\nTotal: {total_sales}")

#Saves all sales to a reloadable CSV file.
def save_sales_file(sales):
    with open(sales_directory_path + sales_filename, mode='w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(sales_fieldnames)  # Write header
        for sale in sales:
            csv_writer.writerow([sale.getProductName(), sale.getPrice(), sale.getKindOfPayment()])

#Copies the names, prices and method of pay to the clipboard to pase onto another spreadsheet software.
def sold_cart_to_clipboard(sale):
    names = " + ".join([product.getName() for product in sale.getProducts()])
    total = sale.getPrice()
    payment_method = sale.getKindOfPayment()
    clipboard_text = names + "\t" + payment_method + "\t" + str(total)
    pyperclip.copy(clipboard_text)
    return clipboard_copied_message

def buy_shopping_cart(shoppingCart, sales):
    total = 0
    for product in shoppingCart:
        ammount = product.getPrice().replace("$", "").replace(".", "").replace(",", "")
        total += float(ammount)
    price_to_pay = total_to_pay_message + str(total)
    payment_done = False
    while not payment_done:
        payment_method = simpledialog.askstring(payment_window_title, price_to_pay)
        if payment_method == '0':
            return False
        elif payment_method not in ['e', 'd', 'c', 'tr']:
            messagebox.showerror("Error", "Metodo de pago invalido.")
        else:
            payment_done = True
    sale_name = " + ".join([product.getName() for product in shoppingCart])
    sale = Sale(sale_name, total, payment_method, datetime.now().strftime("%H:%M:%S"))
    sales = add_to_sales(sale, sales)
    sold_cart_to_clipboard(sale)
    return sales

def closing_statement(sales):
    if not sales:
        messagebox.showinfo("Cierre de Caja", "No hay ventas registradas hoy.")
        return
    total_sales = 0
    for sale in sales:
        total_sales += sale.getPrice()
    sales_list = "\n".join([f"Venta: {sale.getPrice()} - Metodo: {sale.getKindOfPayment()}" for sale in sales])
    messagebox.showinfo("Ventas Registradas", f"Ventas:\n{sales_list}\n\nTotal: {total_sales}")