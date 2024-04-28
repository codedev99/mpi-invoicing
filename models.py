from extensions import db

class ProductList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    rate = db.Column(db.Float(), nullable=False)
    hsn = db.Column(db.String(10), nullable=True)
    gst = db.Column(db.Float(), nullable=False)

class ItemsList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    hsn = db.Column(db.String(150), nullable=True)
    rate = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(), nullable=False)
    discount = db.Column(db.Float(), nullable=True)
    value = db.Column(db.Float(), nullable=False)
    gst = db.Column(db.Float(), nullable=False)
    amount = db.Column(db.Float(), nullable=False)