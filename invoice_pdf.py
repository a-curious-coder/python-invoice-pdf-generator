#!/usr/bin/env python
import datetime
import os

from fpdf import FPDF
from PIL import Image
from io import BytesIO
import requests

DEBUG = False


class PdfInvoice:
    """Invoice PDF"""

    def __init__(self):
        """Initialize invoice"""
        # Customer values
        # Read in address from file
        with open("data/address.txt", "r") as f:
            self.address = f.read()
            # Read notes
        with open("data/notes.txt", "r") as f:
            self.notes = f.read()
        # Read payment_terms
        with open("data/payment_terms.txt", "r") as f:
            self.payment_terms = f.read()
        # Settings
        self.folder = "invoices"
        self.logo_url = ""
        self.width = 216.04
        self.height = 279.39
        self.create_blank_pdf()

    def create_blank_pdf(self):
        """Create blank pdf"""
        self.pdf = FPDF("P", "mm", (self.width, self.height))
        self.pdf.add_page()
        self.enable_grid(False)
        self.pdf.set_text_color(65, 65, 65)
        self.pdf.set_font("helvetica", "", 29)

    def enable_grid(self, grid):
        """Enable grid"""
        if grid:
            grid_size = 20
            for i in range(0, 300, grid_size):
                # if i % 10 == 0:
                #     self.draw_vertical_line(i, 0, 2000, color=True)
                #     self.draw_horizontal_line(0, i, 2000, color=True)
                # else:
                self.draw_vertical_line(i, 0, 2000)
                self.draw_horizontal_line(0, i, 2000)

    def invoice_to_pdf(self, inv):
        """Generate invoice to pdf"""
        name = inv.name
        items = inv.items
        # Calculate total income from items
        total_income = sum(item["quantity"] * item["unit_cost"] for item in items)
        total_income = f"{total_income:.2f}"

        # NOTE: INVOICE CAPTION
        self.pdf.set_xy(119, 14)
        self.pdf.cell(ln=0, h=0, align="R", w=85, txt="INVOICE", border=0)
        dprint("[INFO] Caption added")
        # NOTE: LOGO
        # If logo url has not been provided, download logo from url to images
        if self.logo_url == "" and os.path.isfile("data/logo_url.txt"):
            with open("data/logo_url.txt", "r") as f:
                self.logo_url = f.read()
            if self.logo_url:
                r = requests.get(self.logo_url)
                if r.status_code == 200:
                    with open("images/logo.png", "wb") as f:
                        f.write(r.content)
                    dprint(f"[INFO] Logo downloaded from {self.logo_url}")
                else:
                    dprint(f"[ERROR] Failed to download logo from {self.logo_url}")
            else:
                dprint("[INFO] No logo url provided; Referring to local path")
        # If images/main_logo.png does not exist, create it
        if not os.path.isfile("images/main_logo.png"):
            self.compress_image("images/logo.png")
        self.load_image("main_logo.png", 12.8, 5, 30, 30)
        dprint("[INFO] Logo added")
        # NOTE: DATE
        #  Get today's date in Month, Date, Year format
        today = datetime.date.today()
        # Reset font size
        self.pdf.set_font("helvetica", "", 10.0)
        # Set font color to grey
        self.pdf.set_xy(153, 37)
        self.pdf.set_text_color(95, 95, 95)
        self.pdf.cell(ln=0, h=0, align="L", w=0, txt="Date:", border=0)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.set_xy(177.5, 37)
        self.pdf.cell(
            ln=0, h=0, align="L", w=0, txt=f"{today.strftime('%B %d, %Y')}", border=0
        )
        dprint("[INFO] Date added")
        # NOTE: FROM ADDRESS
        # Reset font
        self.pdf.set_xy(16.28, 42)
        # for each new line in self.address
        for _, line in enumerate(self.address.splitlines()):
            self.pdf.set_font("helvetica", "", 10.0)
            if _ == 0:
                self.pdf.set_font("helvetica", "B", 10.0)
            # Set font color to grey
            self.pdf.cell(ln=0, h=22.0, align="L", w=85, txt=line, border=0)
            self.pdf.set_xy(16.28, self.pdf.get_y() + 4.3)
        dprint("[INFO] From address added")
        # NOTE: BILL TO
        # Reset font
        self.pdf.set_font("helvetica", "", 10.0)
        self.pdf.set_xy(16.28, 60.43)
        self.pdf.cell(ln=0, h=22.0, align="L", w=85, txt="Bill To:", border=0)
        # Reset font
        self.pdf.set_font("helvetica", "B", 10.0)
        self.pdf.set_xy(16.28, 66.175)
        self.pdf.cell(ln=0, h=22.0, align="L", w=85, txt=f"{name}", border=0)
        dprint("[INFO] Bill to added")
        rect_height = 7.4
        # NOTE: ADDING RECTANGLE FOR BALANCE DUE
        # Add rectangle and fill with color
        self.load_image(image="balance_bar.png", x=112.5, y=42, w=95, h=8.8)
        dprint("[INFO] Rectangle added")
        # NOTE: BALANCE DUE
        # Reset font
        self.pdf.set_font("helvetica", "B", 12.0)
        self.pdf.set_xy(92, 46.4)
        self.pdf.set_text_color(65, 65, 65)
        self.pdf.cell(
            ln=0,
            h=0,
            align="C",
            w=0,
            txt="Balance Due:",
            border=0,
        )
        self.pdf.set_xy(183, 46.4)
        self.pdf.cell(
            ln=0,
            h=0,
            align="C",
            w=0,
            txt=f"£{total_income}",
            border=0,
        )
        dprint("[INFO] Balance due added")
        # NOTE: ADDING TABLE
        self.load_image(image="table_bar.png", x=10.5, y=93.75, w=195, h=7.6)
        self.draw_vertical_line(124.5, 93.85, rect_height)
        self.draw_vertical_line(151.5, 93.85, rect_height)
        self.draw_vertical_line(179, 93.85, rect_height)
        dprint("[INFO] Table added")
        # NOTE: ADDING TABLE HEADER
        text_height = 97.5
        # Reset font
        self.pdf.set_font("helvetica", "", 10.0)
        self.pdf.set_xy(15.15, text_height)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt="Item", border=0)
        self.pdf.set_xy(129, text_height)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt="Quantity", border=0)
        self.pdf.set_xy(165, text_height)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt="Rate", border=0)
        self.pdf.set_xy(187, text_height)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt="Amount", border=0)
        dprint("[INFO] Table header added")
        # NOTE: ADDING ITEMS
        row = 107
        for i in items:
            item = f"{i['name']}"
            quantity = i["quantity"]
            quantity_str = ""
            # If quantity has 2dp
            if quantity % 1 == 0:
                quantity_str = f"{quantity:.0f}"
            # if quantity has 1dp
            elif quantity % 1 == 0.5:
                quantity_str = f"{quantity:.1f}"
            # if quantity has 2dp
            elif quantity % 1 == 0.25:
                quantity_str = f"{quantity:.2f}"
            unit_cost = i["unit_cost"]
            amount = quantity * unit_cost
            # Reset font
            self.pdf.set_font("helvetica", "B", 10.0)
            self.pdf.set_text_color(0, 0, 0)
            # Item
            self.pdf.set_xy(15.1, row)
            self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"{item}", border=0)
            # reset font
            self.pdf.set_font("helvetica", "", 10.0)
            # Quantity
            self.pdf.set_xy(129, row)
            self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"{quantity_str}", border=0)
            # Rate
            self.pdf.set_xy(165, row)
            self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"£{unit_cost:.2f}", border=0)
            # Amount
            self.pdf.set_xy(187, row)
            self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"£{amount:.2f}", border=0)
            row += 8
        dprint("[INFO] Items added")
        # NOTE: ADDING TOTAL
        self.pdf.set_font("helvetica", "", 10.0)
        self.pdf.set_xy(153, row + 15)
        # set text color light gray
        self.pdf.set_text_color(145, 145, 145)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt="Total:", border=0)

        self.pdf.set_xy(187, row + 15)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"£{total_income}", border=0)
        dprint("[INFO] Total added")
        # NOTE: FINAL NOTES in bottom left corner
        self.write_sentences("Notes", self.notes, row)
        dprint("[INFO] Notes added")
        row += 50
        self.write_sentences("Terms", self.payment_terms, row)
        dprint("[INFO] Terms added")
        self.pdf.output(f"{self.folder}/{name}'s_invoice.pdf", "F")
        dprint("[INFO] PDF generated")

    def write_sentences(self, header, notes, row):
        """Write sentences to pdf"""
        self.pdf.set_font("helvetica", "", 10.0)
        self.pdf.set_xy(16, row + 30)
        # Set text color gray
        self.pdf.set_text_color(145, 145, 145)
        self.pdf.cell(ln=0, h=0, align="L", w=85, txt=f"{header}:", border=0)
        self.pdf.set_xy(16, self.pdf.get_y() + 7.5)

        self.pdf.set_text_color(55, 55, 55)
        self.pdf.set_font("helvetica", "", 10.0)
        for _, line in enumerate(notes.splitlines()):
            # Set font color to grey
            self.pdf.cell(ln=0, h=0, align="L", w=85, txt=line, border=0)
            self.pdf.set_xy(16, self.pdf.get_y() + 5)

    def draw_vertical_line(self, x, y, h, color=False):
        """Draw vertical line"""
        if color:
            self.pdf.set_draw_color(255, 0, 0)
        else:
            self.pdf.set_draw_color(95, 95, 95)
        # Vertical line
        x1, y1 = x, y
        x2, y2 = x, y1 + h
        # X1, Y1, X2, Y2
        self.pdf.line(x1, y1, x2, y2)

    def draw_horizontal_line(self, x, y, w, color=False):
        """Draw horizontal line"""
        if color:
            self.pdf.set_draw_color(255, 0, 0)
        else:
            self.pdf.set_draw_color(175, 175, 175)
        # Vertical line
        x1, y1 = x, y
        x2, y2 = x1 + w, y
        # X1, Y1, X2, Y2
        self.pdf.line(x1, y1, x2, y2)

    def load_image(self, image, x, y, w, h):
        """Load image from file"""
        self.pdf.image(f"images/{image}", x, y, w, h)

    def compress_image(self, image_path):
        """reduce dimensions of image"""
        img = Image.open(image_path)
        img.thumbnail((600, 600), Image.ANTIALIAS)
        img.save("images/main_logo.png", "PNG")


def dprint(msg):
    """Debug print"""
    if DEBUG:
        print(msg)
