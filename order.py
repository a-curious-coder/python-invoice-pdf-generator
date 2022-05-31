""" Order class """


class Order:
    """Order data class"""
    def __init__(self, name, quantity, order_date, product):
        """ Initialize order """
        self.name = name
        self.quantity = quantity
        self.order_date = order_date
        self.product = product
        self.cost = self.calculate_cost()

    def calculate_cost(self):
        """ Calculate cost of purchase and force 2 decimal places"""
        return round(self.quantity * self.product.price, 2)

    def get_date(self):
        """ Return the order date """
        return self.order_date.strftime("%d/%m/%Y")

    def __str__(self):
        """ Return a string representation of the order"""
        # self.cost to string to 2dp
        cost = f"{self.cost:.2f}"
        return f" {self.product.name:<10} {self.quantity:<10} {cost:<10} {self.get_date():<15}"
    
    def __eq__(self, other):
        """ Override the default Equals behavior"""
        return self.name == other.name and \
                self.quantity == other.quantity and \
                self.order_date == other.order_date and \
                self.product == other.product and \
                self.cost == other.cost