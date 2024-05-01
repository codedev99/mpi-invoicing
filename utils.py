from extensions import db
from models import ProductList, ItemsList
import csv
from jinja2 import Template, Environment, FileSystemLoader
from sqlalchemy.sql import functions

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
    parsed_template = None

    def __init__(self):
        for key in self.keylist:
            self.valuelist[key] = ""

def numToFig(num: int):
    units = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
    tens = ["Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninty"]
    teens = ["Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Ninteen"]
    if num == 0:
        return "Zero"
    if num <= 10:
        return units[num-1]
    if num <= 19:
        return teens[num-11]
    if num <= 99:
        ret = tens[int(num/10)-2]
        if num % 10 != 0:
            ret = ret + " " + numToFig(num%10)
        return ret
    if num <= 999:
        ret = numToFig(int(num/100)) + " Hundred"
        if num % 100 != 0:
            ret = ret + " " + numToFig(num%100)
        return ret
    if num <= 99999:
        ret = numToFig(int(num/1000)) + " Thousand"
        if num % 1000 != 0:
            ret = ret + " " + numToFig(num%1000)
            return ret
    else:
        raise Exception("Number to Figure: number out of range") 

def rupeesInFigures(num: str):
    sp = num.split('.')
    intg = sp[0]
    decm = sp[1]
    assert len(intg) <= 5 and len(decm) <= 2
    figures = "Rupees " + numToFig(int(intg)) + " and Paise " + numToFig(int(decm)) + " Only"
    return figures

def generateInvoice(formdata: FormData):
    formvalues = []
    for i in range(len(formdata.keylist)):
        formvalues.append(formdata.valuelist[formdata.keylist[i]])

    itemlist = ItemsList.query.all()
    items = []
    for item in itemlist:
        arr = []
        arr.append(item.name)
        arr.append(item.hsn)
        arr.append("%.2f"%item.rate)
        arr.append(str(item.quantity))
        arr.append("%.2f"%item.price)
        arr.append("%.2f"%item.discount)
        arr.append("%.2f"%item.value)
        gstamount = round(item.amount, 2) - round(item.value, 2)
        arr.append("%.2f"%(gstamount/2) + " " + "(%.2f%s)"%(item.gst/2, '%')) # divide by 2 for cgst and sgst components
        arr.append("%.2f"%(gstamount/2) + " " + "(%.2f%s)"%(item.gst/2, '%'))
        arr.append("%.2f"%item.amount)
        items.append(arr)
    
    finalvalues = getSubtotals()
    
    finalvalues.append(finalvalues[-1])
    finalvalues.append(rupeesInFigures(finalvalues[-1]))

    env = Environment(loader=FileSystemLoader('./templates'))
    invoice_template = env.get_template('taxinvoicetemplate.html.j2')
    parsed_template = invoice_template.render(formvalues=formvalues, items=items, finalvalues=finalvalues)

    return parsed_template

def getSubtotals():
    subtotals = [db.session.query(functions.sum(ItemsList.discount)).scalar(),
                db.session.query(functions.sum(ItemsList.value)).scalar(),
                0.0,
                0.0,
                db.session.query(functions.sum(ItemsList.amount)).scalar()]
    itemlist = ItemsList.query.all()
    items = []
    totgst = 0.0
    for item in itemlist:
        gstamount = round(item.amount, 2) - round(item.value, 2)
        totgst += gstamount
    
    subtotals[2] = totgst/2
    subtotals[3] = totgst/2
    for i in range(len(subtotals)):
        subtotals[i] = "%.2f"%subtotals[i]

    return subtotals