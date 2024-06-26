from flask import Flask
from extensions import db
from routes import main
from models import ProductList, ItemsList
from utils import fill_table

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///current_invoice_table.db'
    db.init_app(app)
    app.config['SECRET_KEY'] = 'mpi@123'
    app.register_blueprint(main)

    return app

def add_data():
    try:
        ProductList.__table__.drop(db.engine)
    except Exception as e:
        print(e)
    try:
        ItemsList.__table__.drop(db.engine)
    except Exception as e:
        print(e)
    db.session.commit()

    db.create_all()
    arr = fill_table("product-list.csv")
    db.session.add_all(arr)
    db.session.commit()