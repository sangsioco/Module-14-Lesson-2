from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BakeryItem(db.Model):
    __tablename__ = 'bakery_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __init__(self, name, quantity, price, category):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.category = category

    def __repr__(self):
        return f'<BakeryItem {self.name}>'
