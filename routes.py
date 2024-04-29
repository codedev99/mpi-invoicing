from flask import Blueprint, render_template, request, url_for, redirect
from extensions import db
from forms import PartyDetailsForm, InvoiceDetailsForm, ProductDeatilsForm
from models import ProductList, ItemsList
from utils import FormData, generateInvoice, getSubtotals

main = Blueprint("main", __name__)
global formdata
formdata = FormData()

@main.route('/', methods=["GET", "POST"])
def partyDetailsPage():
    form = PartyDetailsForm(request.form)
    formdata = FormData()
    if request.method == "POST":
        formdata.valuelist[formdata.keylist[0]] = " " if form.name.data == "" else form.name.data
        formdata.valuelist[formdata.keylist[1]] = " " if form.address.data == "" else form.address.data
        formdata.valuelist[formdata.keylist[2]] = " " if form.pannumber.data == "" else form.pannumber.data
        phno = form.phonenumber.data
        formdata.valuelist[formdata.keylist[3]] = " " if phno is None else str(phno)
        formdata.valuelist[formdata.keylist[4]] = " " if form.gstin.data == "" else form.gstin.data

        return redirect('/invoice-details')
    
    return render_template('party-details.html.j2', form=form)

@main.route('/invoice-details', methods=["GET", "POST"])
def invoiceDetailsPage():
    form = InvoiceDetailsForm(request.form)
    if request.method == "POST":
        formdata.valuelist[formdata.keylist[5]] = " " if form.invoicenumber.data == "" else form.invoicenumber.data
        formdata.valuelist[formdata.keylist[6]] = " " if form.invoicedate.data is None else str(form.invoicedate.data.strftime("%d/%m/%Y"))
        dos = form.dateofsupply.data
        formdata.valuelist[formdata.keylist[7]] = " " if dos is None else str(dos.strftime("%d/%m/%Y"))
        formdata.valuelist[formdata.keylist[8]] = " " if form.placeofsupply.data == "" else form.placeofsupply.data
        formdata.valuelist[formdata.keylist[9]] = "Y" if form.reversecharge.data else "N"
        formdata.valuelist[formdata.keylist[10]] = " " if form.transportmode.data == "" else form.transportmode.data
        formdata.valuelist[formdata.keylist[11]] = " " if form.vehiclenumber.data == "" else form.vehiclenumber.data

        return redirect('/product-details')

    return render_template('invoice-details.html.j2', form=form)

@main.route('/product-details', methods=["GET", "POST"])
def productDetailsPage():
    form = ProductDeatilsForm(request.form)

    if form.validate_on_submit():
        new_item = ItemsList(name= form.productname.data.product_name, hsn= form.producthsn.data,
                             rate= form.productrate.data, quantity= form.productquantity.data,
                             price= form.productprice.data, discount= form.productdiscount.data,
                             value= form.productvalue.data, gst= form.productgst.data,
                             amount= form.productamount.data)
        db.session.add(new_item)
        db.session.commit()
        return redirect('/product-details')
    
    itemslist = ItemsList.query.all()
    subtotals = [0., 0., 0., 0.]
    if len(itemslist) > 0:
        subtotals = getSubtotals()
    return render_template('product-details.html.j2', form=form, itemslist=itemslist, subtotals=subtotals)

def fetchValues():
    fields = [{"key":"productname", "type":int}, {"key":"producthsn", "type":str},
              {"key":"productrate", "type":float}, {"key":"productquantity", "type":int},
              {"key":"productprice", "type":float}, {"key":"productdiscount", "type":float},
              {"key":"productvalue", "type":float}, {"key":"productgst", "type":float},
              {"key":"productamount", "type":float}]
    values = []
    for fieldarg in fields:
        values.append(request.args.get(**fieldarg))
    
    return values

def calcValues(values):
    if values[2] != None and values[3] != None and values[7] != None:
        values[4] = values[2] * values[3]
        values[6] = values[4]
        if values[5] != None:
            values[6] -= values[5]
        values[8] = values[6] * (1 + values[7]/100)
    else:
        values[4] = None
        values[6] = None
        values[8] = None
    
    return values

@main.route('/productname-revalidate')
def productnameRevalidate():
    values = fetchValues()
    product = ProductList.query.filter_by(id=values[0]).first()
    values[1] = product.hsn
    values[2] = product.rate
    values[7] = product.gst
    values = calcValues(values)

    return render_template("rerender-product-details.html.j2", values=values)

@main.route('/productfields-revalidate')
def productFieldsRevalidate():
    values = fetchValues()
    values = calcValues(values)

    return render_template("rerender-product-details.html.j2", values=values)

@main.route('/generate-invoice')
def generateInvoicePage():
    formdata.parsed_template = generateInvoice(formdata)

    return redirect('/render-invoice')

@main.route('/render-invoice', methods=["GET", "POST"])
def renderInvoicePage():
    message = ""
    if request.method == "POST":
        filename = request.form["content"].split('/')[-1].split('.')[0]
        filename = "./tax-invoice/" + filename + ".htm"
        with open(filename, 'w') as page:
            page.write(formdata.parsed_template)
        message = "File saved to " + filename + ". Open and PRINT AS PDF to save."
    
    return render_template('render-invoice.html.j2', message=message)

@main.route('/delete/<int:id>')
def deleteItem(id):
    item_to_delete = ItemsList.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/product-details')
    except:
        return "Error deleting item"