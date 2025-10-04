from re import search
from tkinter import messagebox, simpledialog
from .Inventory import inventory
from tkinter import simpledialog, messagebox

window_title_search = "Buscar Producto"
search_prompt = "Ingrese el codigo de barras o nombre a buscar."

def look_up_menu():
    search_term = simpledialog.askstring(window_title_search, search_prompt)
    return search_term
    
def search_by_barcode(barcode):
    for product in inventory:
        if product.getBarcode() == barcode:
            return product
    return None

def search_by_name(name):
    found_products = [product for product in inventory if name.lower() in product.getName().lower()]
    if found_products:
        return found_products
    return None

def identify_barcode(search_term):
    try:
        barcode = int(search_term)
        return True
    except ValueError:
        return False
    
def search_product(search_term):
    if search_term != "":
        if identify_barcode(search_term):
            product = search_by_barcode(search_term)
            if product:
                messagebox.showinfo(window_title_search, f"Producto encontrado:\n\nNombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}")
                return product
            else:
                messagebox.showerror(window_title_search, "Producto no encontrado.")
                return None
        else:
            products = search_by_name(search_term)
            if products:
                product_list = "\n\n".join([f"Nombre: {prod.getName()} - Precio: {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for prod in products])
                messagebox.showinfo(window_title_search, f"Productos encontrados:\n\n{product_list}")
                return products
            else:
                messagebox.showerror(window_title_search, "Producto no encontrado.")
                return None

def quick_add_to_cart_by_name(search_term):
    MAX_ELEMENTS_PAGE = 40
    if search_term is None or search_term == "":
        return None
    found_products = search_by_name(search_term)
    if found_products:
        current_page = 0
        pages = [found_products[i:i+MAX_ELEMENTS_PAGE] for i in range (0, len(found_products), MAX_ELEMENTS_PAGE)]

        while True:
            product_list = "\n".join([f"{idx+1}. {prod.getName()} - {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for idx, prod in enumerate(pages[current_page])])
            choice = simpledialog.askstring("Seleccionar Producto", f"Productos que coinciden con '{search_term}' (Pagina '{current_page + 1} de {len(pages)}):\n\n{product_list}\n\nIngrese el numero del producto para agregar al carrito, 's' para siguiente pagina, 'a' para pagina anterior, o '0' para cancelar.")
            if choice is None or choice == '0':
                return None
            elif choice.isdigit() == False:
                if choice.lower() == 'a' or choice.lower() == 'anterior':
                    current_page = max(0, current_page - 1)
                elif choice.lower() == 's' or choice.lower() == 'siguiente':
                    current_page = min(len(pages) - 1, current_page + 1)
                elif choice.lower() == 'escape' or choice.lower() == 'e':
                    return None
            if choice.isdigit() and 1 <= int(choice) <= len(found_products):
                selected_product = found_products[int(choice) - 1]
                return selected_product
            
def search(search_term):
    if search_term is None or search_term == "":
        return None
    elif identify_barcode(search_term) == True:
        return search_by_barcode(search_term)
    elif identify_barcode(search_term) == False:
        return quick_add_to_cart_by_name(search_term)
    else:
        return None