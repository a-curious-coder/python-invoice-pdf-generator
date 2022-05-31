#!/usr/bin/env python
import csv
import datetime
import os
import pickle
import random
import time
import unittest
from multiprocessing import Pool

from invoice import Invoice
from invoice_pdf import PdfInvoice
from order import Order
from product import Product


def get_names():
    """Read in names from file"""
    # Read data/100_random_names.csv
    with open("data/names.csv", "r") as f:
        reader = csv.reader(f)
        names = list(reader)
    return names


def get_date_range(numweeks):
    """Generates a date range for a given number of weeks

    Args:
        numweeks (int): number of weeks

    Returns:
        list: list of dates within numweeks range from today
    """
    numdays = numweeks * 7
    # Get today's date
    base = datetime.date.today()
    return [base - datetime.timedelta(days=x) for x in range(numdays)]


def delete_all_invoices():
    """Delete all invoices"""
    for filename in os.listdir("invoices"):
        # if filename ends with pdf
        if filename.endswith(".pdf"):
            os.remove(f"invoices/{filename}")


def get_invoice_objects(num_invoices):
    """Generates invoice objects

    Args:
        num_invoices (int): number of invoice objects we want to create

    Returns:
        invoice_objects: list of invoices
    """
    random.seed(10)
    names = random.sample(get_names(), num_invoices)
    invoice_objects = []
    for name in names:
        # Generate random invoice
        # Format name
        name = " ".join(name)
        dates = get_date_range(numweeks=2)

        # Generate random products
        product_names = ["Milk", "Eggs", "Bread", "Cheese", "Butter", "Coffee"]
        products = []
        for _ in range(random.randint(1, 5)):
            product_name = random.choice(product_names)
            # Random price between 1-5 with .5
            price = round(random.uniform(1, 5), 2)
            products.append(Product(product_name, price))

        orders = []
        # Generate random number of orders with random quantities/costs
        for _ in range(random.randint(1, 5)):
            # Generate a date within the last two weeks
            date = random.choice(dates)
            # Get random product
            product = random.choice(products)
            # Generate order
            order = Order(name, random.randint(1, 10), date, product)

            orders.append(order)
        # Sort orders by date
        orders.sort(key=lambda x: x.order_date)
        # Add invoice to list
        invoice_objects.append(Invoice(name, date, orders))
    return invoice_objects


def save_invoice_objects(objs, filename):
    """Save objects to file

    Args:
        objs (list): list of invoice objects
        filename (str): file name representing file to save objects to
    """
    with open(filename, "wb") as outp:  # Overwrites any existing file.
        for obj in objs:
            pickle.dump(obj, outp, pickle.HIGHEST_PROTOCOL)


def load_invoice_objects(filename):
    """Load objects from file

    Args:
        filename (str): filename of file to load objects from

    Returns:
        list: invoice objects
    """
    with open(filename, "rb") as inp:
        objs = []
        while True:
            try:
                objs.append(pickle.load(inp))
            except EOFError:
                break
    return objs


def invoice_to_pdf(invoice_object):
    """Generate single invoice object to pdf file"""
    generate = PdfInvoice(invoice_object)
    generate.invoice_to_pdf()


def generate_invoice_pdf_files(invoice_objects):
    """Generate invoices"""
    for invoice in invoice_objects:
        generate = PdfInvoice(invoice)
        generate.invoice_to_pdf()


def generate_invoice_pdf_files_multithread(invoice_objects):
    """Generate invoices using multiprocessing"""
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(invoice_to_pdf, invoice_objects)
        pool.close()


# Test class for generating invoices
class TestGenerator(unittest.TestCase):
    """Test generate invoices"""

    def setUp(self):
        self.start = time.time()
        num_invoices = 3
        # If invoices folder doesn't exist, make one
        if not os.path.exists("invoices"):
            os.mkdir("invoices")
        # Get invoice objects
        self.invoices = get_invoice_objects(num_invoices)
        self.validation_invoices = []
        # Get todays date as dd/mm/yyyy
        today = datetime.date.today().strftime("%d_%m_%Y")
        # Invoices pkl filename
        self.filename = f"invoices/{num_invoices}_invoices_{today}.pkl"

    def tearDown(self) -> None:
        # t = time.time() - self.start
        # print("%s: %.3f" % (self.id(), t))
        delete_all_invoices()
        return super().tearDown()

    def test_invoices_generated(self):
        """Initialize test class"""
        # If invoices pkl file doesn't exist
        if not os.path.exists(self.filename):
            # Save generated objects to file
            save_invoice_objects(self.invoices, self.filename)
        # Load invoices in for validation
        self.validation_invoices = load_invoice_objects(self.filename)
        # Compare generated invoices to validation invoices
        self.assertEqual(self.invoices, self.validation_invoices)

    def test_delete_invoices(self):
        """Delete all invoices"""
        # Delete all invoices
        delete_all_invoices()
        # Count pdf files in invoices folder
        num_pdfs = len([f for f in os.listdir("invoices") if f.endswith(".pdf")])
        # If there are no pdf files in invoices folder
        self.assertEqual(num_pdfs, 0)

    def test_generate_invoice_pdf_files_singlethread(self):
        """Generate invoices using single thread"""
        # Generate invoices
        generate_invoice_pdf_files(self.invoices)
        num_pdfs = len([f for f in os.listdir("invoices") if f.endswith(".pdf")])
        self.assertEqual(len(self.invoices), num_pdfs)

    def test_generate_invoice_pdf_files_multithread(self):
        """Generate invoices using multiprocessing"""
        # Generate invoices
        generate_invoice_pdf_files_multithread(self.invoices)
        num_pdfs = len([f for f in os.listdir("invoices") if f.endswith(".pdf")])
        self.assertEqual(len(self.invoices), num_pdfs)


if __name__ == "__main__":
    unittest.main()
