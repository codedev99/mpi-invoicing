from flask import Blueprint, render_template, request, url_for, redirect
from extensions import db
from forms import PartyDetailsForm, InvoiceDetailsForm, ProductDeatilsForm
from models import ProductList

main = Blueprint("main", __name__)

@main.route('/', methods=["GET", "POST"])
def partyDetailsPage():
    form = PartyDetailsForm(request.form)
    if request.method == "POST":
        print(form.name.data)
        print(form.address.data)
        print(form.pannumber.data)
        print(form.phonenumber.data)
        print(form.gstin.data)

        return redirect('/invoice-details')
    
    return render_template('party-details.html', form=form)

@main.route('/invoice-details', methods=["GET", "POST"])
def invoiceDetailsPage():
    form = InvoiceDetailsForm(request.form)
    if request.method == "POST":
        print(form.invoicenumber.data)
        print(form.invoicedate.data)
        print(form.dateofsupply.data)
        print(form.placeofsupply.data)
        print(form.reversecharge.data)
        print(form.transportmode.data)
        print(form.vehiclenumber.data)

        return redirect('/product-details')

    return render_template('invoice-details.html', form=form)

@main.route('/product-details', methods=["GET", "POST"])
def productDetailsPage():
    form = ProductDeatilsForm(request.form)

    if request.method == "POST":
        print("here3")
        print(form.productname.data.product_name)
        print(form.productrate.data)
    return render_template('product-details.html', form=form)

@main.route('/has-product-quantity')
def hasProductQuantity():
    print("here2")
    rate = request.args.get("productrate", type=float)
    quantity = request.args.get("productquantity", type=int)
    price = rate * quantity
    print(price)

    return render_template('has-product-quantity.html', price=price)

def fetchValues():
    print("Here")
    fields = [{"key":"productname", "type":int}, {"key":"producthsn", "type":str},
              {"key":"productrate", "type":float}, {"key":"productquantity", "type":int},
              {"key":"productprice", "type":float}, {"key":"productdiscount", "type":float},
              {"key":"productvalue", "type":float}]
    values = []
    for fieldarg in fields:
        values.append(request.args.get(**fieldarg))
    
    return values

def calcValues(values):
    if values[2] != None and values[3] != None:
        values[4] = values[2] * values[3]
        values[6] = values[4]
        if values[5] != None:
            values[6] -= values[5]
    else:
        values[4] = None
        values[6] = None
    
    return values

@main.route('/productname-revalidate')
def productnameRevalidate():
    values = fetchValues()
    product = ProductList.query.filter_by(id=values[0]).first()
    values[1] = product.hsn
    values[2] = product.rate
    values = calcValues(values)

    return render_template("rerender-product-details.html", values=values)

@main.route('/productrate-revalidate')
def productrateRevalidate():
    values = fetchValues()
    values = calcValues(values)

    render_template("rerender-product-details.html", values=values)
