""" Invoice class """

from order import Order


class Invoice:
    """Invoice data class"""

    def __init__(self, name, date, orders):
        """Initialize invoice"""
        self.name = name
        self.date = date
        self.orders = orders

    def __str__(self):
        """Return a string representation of the invoice"""
        # print date in dd/mm/yyyy format
        date = self.date.strftime("%d/%m/%Y")
        details = f"{self.name}\t{date}\n{'-' * 40}\n"
        details += f" {'Product':<10} {'Quantity':<10} {'Cost':<10} {'Date':<15} \n"
        for order in self.orders:
            details += f"{order}\n"
        return f"{details}"

    def __eq__(self, other):
        """ Override the default Equals behavior

        Args:
            other (Invoice): other invoice object
        """
        return self.name == other.name and \
            self.date == other.date and \
            self.orders == other.orders

    def add_order(self, name, order_date, quantity, product):
        """Add order to invoice"""
        order = Order(name, quantity, order_date, product)
        self.orders.append(order)
