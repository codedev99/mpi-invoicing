from flask import Blueprint, render_template, request, url_for, redirect
from extensions import db
from forms import PartyDetailsForm, InvoiceDetailsForm, ProductDeatilsForm
from models import ProductList, ItemsList
from utils import FormData

main = Blueprint("main", __name__)
formdata = FormData()

@main.route('/', methods=["GET", "POST"])
def partyDetailsPage():
    form = PartyDetailsForm(request.form)
    formdata = FormData()
    if request.method == "POST":
        formdata.valuelist[formdata.keylist[0]] = form.name.data
        formdata.valuelist[formdata.keylist[1]] = form.address.data
        formdata.valuelist[formdata.keylist[2]] = form.pannumber.data
        phno = form.phonenumber.data
        formdata.valuelist[formdata.keylist[3]] = "" if phno is None else str(phno)
        formdata.valuelist[formdata.keylist[4]] = form.gstin.data

        return redirect('/invoice-details')
    
    return render_template('party-details.html', form=form)

@main.route('/invoice-details', methods=["GET", "POST"])
def invoiceDetailsPage():
    form = InvoiceDetailsForm(request.form)
    if request.method == "POST":
        formdata.valuelist[formdata.keylist[5]] = form.invoicenumber.data
        formdata.valuelist[formdata.keylist[6]] = str(form.invoicedate.data.strftime("%d/%m/%Y"))
        dos = form.dateofsupply.data
        formdata.valuelist[formdata.keylist[7]] = "" if dos is None else str(dos.strftime("%d/%m/%Y"))
        formdata.valuelist[formdata.keylist[8]] = form.placeofsupply.data
        formdata.valuelist[formdata.keylist[9]] = "Y" if form.reversecharge.data else "N"
        formdata.valuelist[formdata.keylist[10]] = form.transportmode.data
        formdata.valuelist[formdata.keylist[11]] = form.vehiclenumber.data

        return redirect('/product-details')

    return render_template('invoice-details.html', form=form)

@main.route('/product-details', methods=["GET", "POST"])
def productDetailsPage():
    for key in formdata.keylist:
        print(key, ":  ", formdata.valuelist[key])
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
    return render_template('product-details.html', form=form, itemslist=itemslist)

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

    return render_template("rerender-product-details.html", values=values)

@main.route('/productfields-revalidate')
def productFieldsRevalidate():
    values = fetchValues()
    values = calcValues(values)

    return render_template("rerender-product-details.html", values=values)

@main.route('/render-invoice')
def renderInvoicePage():
    return "Pass"