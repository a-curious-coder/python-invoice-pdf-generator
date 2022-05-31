""" Product class"""


class Product:
    """ Return the product name and price """
    def __init__(self, name, price):
        """ Initialize product """
        self.name = name
        self.price = price

    def __str__(self):
        """ Return the product name and price """
        return f"{self.name} {str(self.price)}"

    def __eq__(self, other):
        """ Override the default Equals behavior """
        return self.name == other.name and self.price == other.price