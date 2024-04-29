from flask_wtf import FlaskForm
from wtforms import Form, StringField, DateTimeField,\
    BooleanField, SubmitField, FloatField, validators
from wtforms.fields import html5 as h5fields
from wtforms.widgets import html5 as h5widgets
from wtforms.validators import InputRequired, Optional
from wtforms.compat import iteritems
from wtforms_sqlalchemy.fields import QuerySelectField
from models import ProductList

class AllForms(FlaskForm):
    def validate(self, extra_validators=None):
        """
        Validates the form by calling `validate` on each field.

        :param extra_validators:
            If provided, is a dict mapping field names to a sequence of
            callables which will be passed as extra validators to the field's
            `validate` method.

        Returns `True` if no errors occur.
        """
        self._errors = None
        success = True
        for name, field in iteritems(self._fields):
            if extra_validators is not None and name in extra_validators:
                extra = extra_validators[name]
            else:
                extra = tuple()
            if not field.validate(self, extra):
                success = False
        return success
    
class PartyDetailsForm(Form):
    name = StringField("Name", validators=[InputRequired(), validators.length(max=150)])
    address = StringField("Full Address", validators=[InputRequired(), validators.length(max=150)])
    pannumber = StringField("PAN Number")
    phonenumber = h5fields.IntegerField("Phone Number", widget=h5widgets.NumberInput(min=6000000000, max=10000000000))
    gstin = StringField("GSTIN / UIN")
    submit = SubmitField("Submit")

class InvoiceDetailsForm(Form):
    invoicenumber = StringField("Invoice Number", validators=[InputRequired(), validators.length(max=20)])
    invoicedate = DateTimeField("Invoice Date", validators=[InputRequired()], format='%Y-%m-%d')
    dateofsupply = DateTimeField("Date of Supply", validators=[Optional()], format='%Y-%m-%d')
    placeofsupply = StringField("Place of Supply", validators=[validators.length(max=50)])
    reversecharge = BooleanField("Reverse Charge Applicable", default=False)
    transportmode = StringField("Transport Mode")
    vehiclenumber = StringField("Vehicle Number", validators=[validators.length(min=10, max=10)])
    submit = SubmitField("Submit")

class ProductDeatilsForm(AllForms):
    productname = QuerySelectField("Select Product",
                                   query_factory=lambda: ProductList.query.order_by(ProductList.product_name).all(),
                                   allow_blank=True, get_label="product_name", validators=[InputRequired()])
    producthsn = StringField("HSN", validators=[Optional()])
    productrate = FloatField("Rate", validators=[InputRequired()])
    productquantity = h5fields.IntegerField("Quantity", widget=h5widgets.NumberInput(min=1, max=30), validators=[InputRequired()])
    productprice = FloatField("Price", validators=[InputRequired()])
    productdiscount = FloatField("Discount", validators=[Optional()], default=0)
    productvalue = FloatField("Taxable Value", validators=[InputRequired()])
    productgst = FloatField("Aggregate GST", validators=[InputRequired()])
    productamount = FloatField("Amount", validators=[InputRequired()])
    addproduct = SubmitField("Add")