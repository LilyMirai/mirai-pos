from tkinter import messagebox, simpledialog
from Inventory import *
import Sales

def empty_shopping_cart(shoppingCart):
    shoppingCart = []
    return shoppingCart

def add_to_cart(product, shoppingCart):
    shoppingCart.append(product)
    return shoppingCart

def remove_from_cart(product, shoppingCart):
    if product in shoppingCart:
        shoppingCart.remove(product)
    return shoppingCart

def view_cart(shoppingCart):
    cart_contents = "\n".join([f"{product.getName()} - {product.getPrice()}" for product in shoppingCart])
    messagebox.showinfo("Carrito de Compras", f"Productos en el carrito:\n{cart_contents}")

def add_custom_product_to_cart(shoppingCart):
    name = simpledialog.askstring("Producto Personalizado", "Ingrese el nombre del producto:", initialvalue="Cartas Sueltas")
    price = simpledialog.askstring("Producto Personalizado", "Ingrese el precio del producto:", initialvalue="$1000")
    if name is None or name == '' or price is None or price == '':
        return
    product = Product('', name, price, 1, "Producto Personalizado", "", "", "", "")
    shoppingCart = add_to_cart(product, shoppingCart)
    return shoppingCart

def price_to_int(price):
    ammount = price.replace("$", "").replace(".", "").replace(",", "")
    return int(ammount)

def buy_shopping_cart(shopping_cart, sales):
    total = 0
    for product in shopping_cart:
        amount = product.getPrice()
        amount = amount.replace("$", "")
        amount = amount.replace(".", "")
        total += (int(amount))
    payment_info = f"El total a pagar es: ${total:,}"
    payment_kind_info = "\nIngrese el metodo de pago:\ne. Efectivo\nd. Debito\nc. Credito\ntr. Transferencia\n\n0. Cancelar compra\n"
    payment = payment_info + "\n" + payment_kind_info
    payment_done = False
    while not payment_done:
        payment_method = simpledialog.askstring("Total a Pagar", payment)
        if payment_method == '0':
            return False
        if payment_method not in ['e', 'd', 'c', 'tr']:
            messagebox.showwarning("Metodo Invalido", "Metodo de pago invalido. Ingrese metodo valido.")
            payment_done = False
        else:
            payment_done = True
    sale = Sales.Sale(shopping_cart.copy(), total, payment_method)
    sales = Sales.add_to_sales(sale, sales)
    Sales.sold_cart_to_clipboard(sale)
    print(sales)
    return sales