from contextlib import closing
from json import load
import csv, os, pyperclip
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import date, timedelta

#orden csv entrante: codigo, nombre, precio, inventario, descripcion, siniva, coniva, venta, final

#Startup - Creacion de Variables

onDevelopmentBranch = True
directory_path = "./inventories/"
current_date = date.today()
previous_date = current_date - timedelta(days=1)
filename = "Inventario " + str(current_date) + ".csv"
filename_previous = "Inventario " + str(previous_date) + ".csv"
shoppingCart = []
sale = None


def openInventoryFile():
    if os.path.exists(directory_path + filename):
        processInventoryFile(directory_path + filename)
    elif os.path.exists(directory_path + filename_previous):
        processInventoryFile(directory_path + filename_previous)
    else:
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

Sales = []
class Sale:
    def __init__(self, products, ammount, kindOfPayment):
        self.products = products
        self.ammount = ammount
        self.kindOfPayment = kindOfPayment
    
    def getProducts(self):
        return self.products
    def getAmmount(self):
        return self.ammount
    def getKindOfPayment(self):
        return self.kindOfPayment
    
def addToSales(sale):
    Sales.append(sale)

def returnAllSales(Sales):
    #returns a size-editable messagebox with all sales with the following format:
    # Numero Venta - Producto1 + Producto2 + ... - Metodo de Pago - Monto
    # enumerar ventas junto a "Venta 1: Producto1 + Producto2 + ... - Metodo de Pago - Monto"
    #no incluir titulos, solo los resultados
    if not Sales:
        messagebox.showinfo("Ventas", "No hay ventas registradas.")
        return
    sales_list = "\n\n".join([f"{idx+1}: {', '.join([prod.getName() for prod in sale.getProducts()])} - {sale.getKindOfPayment()} - {sale.getAmmount()}" for idx, sale in enumerate(Sales)])
    messagebox.showinfo("Ventas Registradas", f"Ventas:\n\n{sales_list}")

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
    #mode 1: show info, then close function
    #mode 2: show list of products that match, then let user choose one to add to cart
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        if mode == 1:
            product_list = "\n".join([f"{prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for prod in found_products])
            messagebox.showinfo("Productos Encontrados", f"Productos que coinciden con '{name}':\n{product_list}")
        elif mode == 2:
            product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(found_products)])
            choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}':\n{product_list}\nIngrese el numero del producto a añadir al carrito:")
            if choice and choice.isdigit() and 1 <= int(choice) <= len(found_products):
                selected_product = found_products[int(choice)-1]
                addToCart(selected_product)
            else:
                messagebox.showwarning("No Valido", "Seleccion invalida.")

def quickAddToCart(name):
    #show list of products that match, then let user choose one to add to cart
    found_products = [product for product in Products if name.lower() in product.getName().lower()]
    if found_products:
        product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(found_products)])
        choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}':\n{product_list}\n\nEscape o Cancelar para salir\n\nPara añadir al carrito ingrese numero:")
        if choice and choice.isdigit() and 1 <= int(choice) <= len(found_products):
            selected_product = found_products[int(choice)-1]
            addToCart(selected_product)

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
    if name != "":
        #mostrar lista de productos que coincidan, luego dejar escoger entre coincidencias para escoger el final a añadir
        found_products = [product for product in Products if name.lower() in product.getName().lower()]
        if found_products:
            product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(found_products)])
            choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{name}':\n{product_list}\nIngrese el numero del producto a añadir al carrito:")
            if choice and choice.isdigit() and 1 <= int(choice) <= len(found_products):
                selected_product = found_products[int(choice)-1]
                addToCart(selected_product)
            else:
                messagebox.showwarning("No Valido", "Seleccion invalida.")

def addToCartFromBarcode(barcode):
    if barcode != "":
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

def substractProductsFromInventory():
    for prod in shoppingCart:
        for item in Products:
            if prod.getBarcode() == item.getBarcode():
                item.removeOne()
                break

def viewCart():
    cart_contents = "\n".join([f"{prod.getName()} - {prod.getPrice()}" for prod in shoppingCart])
    messagebox.showinfo("Carrito de Compras", f"Productos en el carrito:\n{cart_contents}")

def transformPriceToInt(price):
    ammount = price.replace("$", "")
    ammount = ammount.replace(".", "")
    return int(ammount)

def buyShoppingCart():
    total = 0
    for prod in shoppingCart:
        ammount = prod.getPrice()
        ammount = ammount.replace("$", "")
        ammount = ammount.replace(".", "")
        total += (int(ammount))
    payment_info = f"El total a pagar es: ${total:,}"
    payment_kind_info = "\nIngrese el metodo de pago:\ne. Efectivo\nd. Debito\nc. Credito\ntr. Transferencia\n"
    payment = payment_info + "\n" + payment_kind_info
    payment_method = simpledialog.askstring("Total a Pagar", payment)
    if payment_method not in ['e', 'd', 'c', 'tr']:
        messagebox.showwarning("Metodo Invalido", "Metodo de pago invalido. Compra cancelada.")
        return False
    sale = Sale(shoppingCart.copy(), total, payment_method)
    addToSales(sale)
    addSoldCartToClipboard(sale)
    return True

def addCustomProductToCart():
    name = simpledialog.askstring("Nombre del Producto", "Ingrese el nombre del producto:", initialvalue="Cartas Sueltas")
    price = simpledialog.askstring("Precio del Producto", "Ingrese el precio del producto:", initialvalue="$1000")
    if name and price:
        product = Product('', name, price, 1, "Producto Personalizado", "", "", "", "")
        addToCart(product)

def addShoppingCartToClipboard(shoppingCart):
    #crea 2 campos de texto copiables con el formato para excel "Juego1 + Juego2 + Juego3" y "Precio Total"
    names = " + ".join([prod.getName() for prod in shoppingCart])
    total = 0
    for prod in shoppingCart:
        ammount = prod.getPrice()
        ammount = ammount.replace("$", "")
        ammount = ammount.replace(".", "")
        total += (int(ammount))
    total_string = names + '\t' + str(total)
    pyperclip.copy(total_string)

def addSoldCartToClipboard(sale):
    #crea 3 campos de textos en clipboard con formato "Juego1 + Juego2 + Juego3 \t Metodo de Pago \t Precio Total"
    names = " + ".join([prod.getName() for prod in sale.getProducts()])
    total = sale.getAmmount()
    payment_method = sale.getKindOfPayment()
    total_string = names + '\t' + payment_method + '\t' + str(total)
    pyperclip.copy(total_string)

def defineKindOfSearch(input):
    if input.isdigit() == False:
        quickAddToCart(input)
        return True
    elif int(input) > 5:
        quickLookUpProduct(input)
        return True
    return False

def saveSalesFile():
    #create a file called "Ventas {current_date}.csv" in the inventories folder with the following format:
    #venta, producto1 + producto2 + ..., metodo de pago, monto
    sales_filename = "Ventas " + str(current_date) + ".csv"
    with open(directory_path + sales_filename, mode='w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Venta", "Productos", "Metodo de Pago", "Monto"])
        for idx, sale in enumerate(Sales):
            products = " + ".join([prod.getName() for prod in sale.getProducts()])
            csv_writer.writerow([idx+1, products, sale.getKindOfPayment(), sale.getAmmount()])

def loadSalesFile():
    #if theres a file with "Ventas {current_date}.csv" in the sales folder, load it into Sales
    sales_filename = "Ventas " + str(current_date) + ".csv"
    sales_path = "./sales/"
    try:
        if os.path.exists(sales_path + sales_filename):
            with open(sales_path + sales_filename, mode='r', encoding='utf-8-sig') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)  # Skip header row if present
                for row in csv_reader:
                    products_names = row[1].strip().split(" + ")
                    products = []
                    for name in products_names:
                        for prod in Products:
                            if prod.getName() == name:
                                products.append(prod)
                                break
                    ammount = int(row[3].strip())
                    kindOfPayment = row[2].strip()
                    saleToAdd = Sale(products, ammount, kindOfPayment)
                    Sales.append(saleToAdd)
            print("Archivo de ventas cargado exitosamente.")
    except Exception as e:
        pass

def closingStatement():
    if not Sales:
        messagebox.showinfo("Ventas", "No hay ventas registradas.")
        return

    sales_list = "\n".join([f"Venta: {sale.getAmmount()} - Metodo: {sale.getKindOfPayment()}" for sale in Sales])
    messagebox.showinfo("Ventas Registradas", f"Ventas:\n{sales_list}")

def saveInventoryFile():
    with open(directory_path + filename, mode='w', newline='', encoding='utf-8-sig') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Codigo", "Nombre", "Precio", "Inventario", "Descripcion", "SinIVA", "ConIVA", "Venta", "Final"])
        for product in Products:
            csv_writer.writerow([product.getBarcode(), product.getName(), product.getPrice(), product.getQuantity(), product.getDescription(), product.siniva, product.coniva, product.venta, product.final])

menuString = "Seleccione una accion:\n\n1. Añadir producto al carrito. \n2. Añadir producto personalizado al carrito.\n3. Ver Carrito \n4. Vaciar Carrito\n5. Comprar Carrito\n\n6. Ver Ventas\n\n8. Guardar\n9. Guardar y salir\n0. Salir sin guardar\n"
addInstructions = "\n- Para buscar, ingresa un nombre o codigo de barra -\n"



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
        
        if action == '': #if empty, loop
            continue
        elif action == '0': #exit
            #ask for confirmation, go back to menu if not confirmed
            if messagebox.askyesno("Salir sin guardar", "¿Está seguro que desea salir sin guardar?"):
                break
        elif action == '9': #save and exit
            #ask for confirmation, go back to menu if not confirmed
            if not messagebox.askyesno("Guardar y salir", "¿Está seguro que desea guardar y salir?"):
                continue
            closingStatement()
            saveInventoryFile()
            break
        elif action == '8': #just save
            #ask for confirmation
            if not messagebox.askyesno("Guardar", "¿Está seguro que desea guardar?"):
                continue
            closingStatement()
            saveInventoryFile()
            continue
        elif action == '1':
            search = simpledialog.askstring("Añadir al Carrito", "Ingrese el codigo de barras o nombre del producto a añadir:")
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
            if buyShoppingCart() != False:
                substractProductsFromInventory()
                shoppingCart = emptyShoppingCart(shoppingCart)
                messagebox.showinfo("Compra Exitosa", "Gracias por su compra.\nPega el contenido del portapapeles en la hoja de calculo.")
                saveInventoryFile()
                saveSalesFile()
                sale = None
            else:
                continue
        elif action == '6': #Ver Ventas
            returnAllSales(Sales)
        elif defineKindOfSearch(action): #if the input was a search, search, then skip the rest of the loop
            continue



openInventoryFile()
loadSalesFile()
menu()


