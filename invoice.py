""" Invoice data class """
from typing import List


class Invoice:
    """Invoice data class"""x

    name: str
    date: str
    items: List[dict]

    def __init__(self, name, date, items):
        """Initialize invoice"""
        self.name = name
        self.date = date
        self.items = items

    def __str__(self):
        """Return a string representation of the invoice"""
        details = f"{self.name}\n{self.date}"
        item_list = "".join(
            f"{item['name']}\t{item['quantity']}\t£{item['unit_cost']:.2f}\n"
            for item in self.items
        )

        return f"{details}\n{item_list}"

    def add_item(self, product, purchase_date, quantity, unit_cost):
        """Add item to invoice"""
        self.items.append(
            {
                "name": f"{product} ({purchase_date})",
                "quantity": quantity,
                "unit_cost": unit_cost,
            }
        )
