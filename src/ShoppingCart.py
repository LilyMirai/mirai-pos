from tkinter import messagebox, simpledialog
from .Inventory import *
from .Product import Product
from .Sales import *
from datetime import *

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
    product = Product('', '', name, price, 1, '')
    shoppingCart = add_to_cart(product, shoppingCart)
    return shoppingCart

def price_to_int(price):
    price = str(price)
    amount = price.replace("$", "").replace(".", "").replace(",", "")
    return int(amount)

def total_cart_price(shoppingCart):
    total = 0
    for item in shoppingCart:
        if hasattr(item, 'getPrice'):
            amount = item.getPrice()
            amount = amount.replace("$", "").replace(".", "").replace(",", "")
            total += int(amount)
    return total

def buy_shopping_cart(shopping_cart, sales):
    total = 0
    for item in shopping_cart:
        # Debug: Check what type of object we're dealing with
        print(f"Item type: {type(item)}, Item: {item}")
        
        # Only process if it's a Product object, not a Sale object
        if hasattr(item, 'getPrice') and hasattr(item, 'getName'):
            amount = item.getPrice()
            amount = amount.replace("$", "")
            amount = amount.replace(".", "")
            amount = amount.replace(",", "")
            total += (int(amount))
        else:
            print(f"Warning: Unexpected object type in shopping cart: {type(item)}")
    
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
    
    # Filter shopping_cart to only include Product objects for sale_name
    products_only = [item for item in shopping_cart if hasattr(item, 'getName') and not isinstance(item, Sale)]
    sale_name = " + ".join([product.getName() for product in products_only])
    
    sale = Sale(sale_name, total, payment_method, datetime.now().strftime("%H:%M:%S"))
    sales = add_to_sales(sale, sales)
    sold_cart_to_clipboard(sale)
    print(f"Sales after adding: {sales}")
    return sales

def add_ammount_discount_to_cart(shoppingCart):
    discount_str = simpledialog.askstring("Descuento", "Ingrese el monto del descuento:", initialvalue="$0")
    if discount_str is None or discount_str == '':
        return shoppingCart  # No discount applied, return original cart
    
    try:
        discount_amount = price_to_int(discount_str)
    except ValueError:
        messagebox.showwarning("Descuento Invalido", "El descuento debe ser un numero entero.")
        return shoppingCart  # Invalid discount, return original cart
    
    if discount_amount <= 0:
        messagebox.showwarning("Descuento Invalido", "El descuento debe ser mayor que cero.")
        return shoppingCart  # Non-positive discount, return original cart
    
    if total_cart_price(shoppingCart) <= discount_amount:
        messagebox.showwarning("Descuento Invalido", "El descuento no puede ser mayor o igual al total del carrito.")
        return shoppingCart  # Discount exceeds or equals total, return original cart

    # Create a special Product to represent the discount
    discount_product = Product('', '', 'Descuento', f"-${discount_amount:,}", 1, '')
    shoppingCart.append(discount_product)
    return shoppingCart

def add_percentage_discount_to_product(shoppingCart):
    #prompt the user with the items in cart with their price, ask which product to discount
    MAX_ELEMENTS_PAGE = 40
    if shoppingCart == []:
        messagebox.showwarning("Carrito Vacio", "El carrito esta vacio.")
        return shoppingCart
    current_page = 0
    pages = [shoppingCart[i:i+MAX_ELEMENTS_PAGE] for i in range (0, len(shoppingCart), MAX_ELEMENTS_PAGE)]
    while True:
        product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()}" for idx, prod in enumerate(pages[current_page])])
        choice = simpledialog.askstring("Seleccionar Producto", f"Productos en el carrito (Pagina '{current_page + 1} de {len(pages)}):\n\n{product_list}\n\nIngrese el numero del producto para aplicar descuento, 's' para siguiente pagina, 'a' para pagina anterior, o '0' para cancelar.")
        if choice is None or choice == '0':
            return shoppingCart
        elif choice.lower() == 's':
            if current_page < len(pages) - 1:
                current_page += 1
            else:
                messagebox.showinfo("Ultima Pagina", "Ya estas en la ultima pagina.")
        elif choice.lower() == 'a':
            if current_page > 0:
                current_page -= 1
            else:
                messagebox.showinfo("Primera Pagina", "Ya estas en la primera pagina.")
        else:
            try:
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(pages[current_page]):
                    selected_product = pages[current_page][choice_idx]
                    break
                else:
                    messagebox.showwarning("Seleccion Invalida", "Numero fuera de rango. Intente de nuevo.")
            except ValueError:
                messagebox.showwarning("Seleccion Invalida", "Entrada invalida. Intente de nuevo.")
    #prompt the user for the percentage of discount to apply
    percentage_str = simpledialog.askstring("Descuento", "Ingrese el porcentaje de descuento aplicar (sin el simbolo %):", initialvalue="10")
    if percentage_str is None or percentage_str == '':
        return shoppingCart  # No discount applied, return original cart

    try:
        percentage = int(percentage_str)
    except ValueError:
        messagebox.showwarning("Descuento Invalido", "El porcentaje debe ser un numero entero.")
        return shoppingCart  # Invalid percentage, return original cart

    if percentage <= 0:
        messagebox.showwarning("Descuento Invalido", "El porcentaje debe ser mayor que cero.")
        return shoppingCart  # Non-positive percentage, return original cart

    if percentage >= 100:
        messagebox.showwarning("Descuento Invalido", "El porcentaje debe ser menor que 100.")
        return shoppingCart  # Percentage exceeds or equals 100, return original cart

    # Apply the percentage discount to the selected product
    selected_product.setPrice(price_to_int(selected_product.getPrice()) * (1 - percentage / 100))
    return shoppingCart