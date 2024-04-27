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
    return render_template('product-details2.html', form=form)

@main.route('/has-product-name')
def hasProductName():
    print("here1")
    id = request.args.get("productname", type=int)
    product = ProductList.query.filter_by(id=id).first()
    print(product.hsn, product.rate)

    return render_template('has-product-name.html', hsn = product.hsn, rate=product.rate)

@main.route('/has-product-quantity')
def hasProductQuantity():
    print("here2")
    rate = request.args.get("productrate", type=float)
    quantity = request.args.get("productquantity", type=int)
    price = rate * quantity
    print(price)

    return render_template('has-product-quantity.html', price=price)