window_title_search = "Buscar Producto"
search_prompt = "Ingrese el codigo de barras o nombre a buscar."

def look_up_menu():
    search_term = simpledialog.askstring(window_title_search, search_prompt)
    
def look_up_barcode(barcode):
    for product in inventory:
        if product.getBarcode() == barcode:
            return product
    return None

def look_up_name(name):
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
            product = look_up_barcode(search_term)
            if product:
                messagebox.showinfo(window_title_search, f"Producto encontrado:\n\nNombre: {product.getName()}\nPrecio: {product.getPrice()}\nCantidad: {product.getQuantity()}")
            else:
                messagebox.showerror(window_title_search, "Producto no encontrado.")
        else:
            products = look_up_name(search_term)
            if products:
                product_list = "\n\n".join([f"Nombre: {prod.getName()} - Precio: {prod.getPrice()} - Cantidad: {prod.getQuantity()}" for prod in products])
                messagebox.showinfo(window_title_search, f"Productos encontrados:\n\n{product_list}")
            else:
                messagebox.showerror(window_title_search, "Producto no encontrado.")
