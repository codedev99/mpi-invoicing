from extensions import db
from models import ProductList, ItemsList
import csv

def fill_table(file):
    arr = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            arr.append(ProductList(product_name = row[0],
                                   rate = row[1],
                                   hsn = row[2],
                                   gst = row[3]))
    return arr

class FormData():
    keylist = ["partyname", "address", "pannumber", "phonenumber", "gstin",
                "invoicenumber", "invoicedate", "dateofsupply", "placeofsupply",
                "reversecharge", "transportmode", "vehiclenumber"]
    valuelist = {}
    def __init__(self):
        for key in self.keylist:
            self.valuelist[key] = ""