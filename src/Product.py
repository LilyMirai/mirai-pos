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
