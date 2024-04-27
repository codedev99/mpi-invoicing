from extensions import db

class ProductList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    rate = db.Column(db.Float(), nullable=False)
    hsn = db.Column(db.String(10), nullable=True)