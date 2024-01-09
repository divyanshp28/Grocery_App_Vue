from base64 import b64encode
from sqlalchemy import ForeignKey, ForeignKeyConstraint, Enum
from src import db, app
from datetime import datetime, date
from sqlalchemy.orm.exc import NoResultFound


#----------------- CREATING ADMIN -------------------------------------------

def create_admin():
    user = User.query.filter(User.username == "admin").scalar()
    if not user:
        admin = User(username = "admin", full_name = "Admin Chaudhary", mobile = "9523878991", email = "admin@gmail.com", password = "admin", role = "admin")
        db.session.add(admin)
        db.session.commit()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    full_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(12), nullable = False)
    role = db.Column(db.String(), nullable = False)
    # cnfPassword = db.Column(db.String(12), nullable=True)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    is_store_admin = db.Column(db.Boolean, default=False)
    requests = db.relationship('Request', back_populates='user')
    orders = db.relationship('Order', back_populates='user')

    @property
    def output(self):
        return{
            "id":self.id,
            "username":self.username,
            "mobile":self.mobile,
            "full_name":self.full_name,
            "email":self.email,
            "role":self.role,
            "is_store_admin": self.is_store_admin
        }
    

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True)
    products = db.relationship("Product", back_populates="category")
    requests = db.relationship('Request', back_populates='category')

    @property
    def output(self):
        return {
            "id": self.id,
            "category_name": self.category_name
        }


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True)
    # product_image = db.Column(db.String())
    product_image = db.Column(db.LargeBinary())
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    mfg_date = db.Column(db.DateTime())
    exp_date = db.Column(db.DateTime())
    rate_per_unit = db.Column(db.Float(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='products')
    orders = db.relationship("Order", back_populates="product")



    @property
    def output(self):
        try:
            product_name = self.product.product_name if self.product else None
        except NoResultFound:
            product_name = None
        return {
            "id": self.id,
            # "product_image":self.product_image,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "mfg_date": self.mfg_date.strftime("%d-%m-%Y") if self.mfg_date else None,
            "exp_date": self.exp_date.strftime("%d-%m-%Y") if self.exp_date else None,
            "rate_per_unit": self.rate_per_unit,
            "category_id":self.category_id,
        }
    
    def get_product_image_data(self):
        if self.product_image:
            product_image_data = b64encode(self.product_image).decode("utf-8")
            return product_image_data
        return None


class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('cart', lazy='dynamic'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    product = db.relationship('Product', backref=db.backref('carts', lazy='dynamic'))
    quantity = db.Column(db.Integer)


    @property
    def output(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "product_id":self.product_id,
            "quantity":self.quantity
        }


class CartItem(db.Model):
    __tablename__ = 'cart_items'
    id = db.Column(db.Integer(), primary_key=True, unique=True)
    cart_id = db.Column(db.Integer(), db.ForeignKey('carts.id'))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    rate_per_unit = db.Column(db.Float(), nullable=False)
    quantity = db.Column(db.Integer())

    @property
    def output(self):
        return {
            "id": self.id,
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "rate_per_unit": self.rate_per_unit,
            "quantity": self.quantity
        }


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer())
    order_date = db.Column(db.DateTime(), default=datetime.utcnow)
    user = db.relationship("User", back_populates="orders")
    product = db.relationship("Product", back_populates="orders")

    
    @property
    def output(self):
        return {
            "id":self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            # "product_name": self.product.name,
            "quantity":self.quantity,
            "order_date":self.order_date.strftime("%d-%m-%Y, %H:%M") if self.order_date else None,
        }

class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category_name = db.Column(db.String(500))
    request_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    user = db.relationship('User', back_populates='requests')
    category = db.relationship('Category', back_populates='requests')

    @property
    def output(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "category_name": self.category_name,
            "request_type": self.request_type,
            "status": self.status
        }
