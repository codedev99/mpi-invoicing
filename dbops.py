from extensions import db
from models import ProductList
import csv

def fill_table(file):
    arr = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            arr.append(ProductList(product_name = row[0],
                                   rate = row[1],
                                   hsn = row[2]))
    return arr