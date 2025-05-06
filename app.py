from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db=SQLAlchemy(app)

# Create tables when the application starts
with app.app_context():
    db.create_all()

class Product (db.Model):
    id= db.Column(db.Integer, primary_key= True)
    name= db.Column(db.String(100), nullable = False)
    price= db.Column(db.Integer, default=0)
    description= db.Column(db.String(500), nullable= False)
    stock = db.Column(db.Integer, default=0)

class Order(db.Model):
    """Order model to store customer orders."""
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(80), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_items = db.relationship('OrderItem', backref='order', lazy=True)


class OrderItem(db.Model):
    """OrderItem model to store the products and quantities in an order."""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/products", methods= ["GET"])
def list_products():
    products = Product.query.all()
    result = [{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    } for product in products]
    return jsonify(result), 200

@app.route('/products', methods=['POST'])
def add_product():
    """Add a new product to the database."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock', 0)
    if not name or price is None:
        return jsonify({'error': 'Name and price are required fields.'}), 400
    new_product = Product(name=name, description=description, price=price, stock=stock)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully', 'product_id': new_product.id}), 201


@app.route("/products/<int:product_id>", methods = ["GET"])
def get_product(product_id):
    """Get details of a specific product by ID."""
    product = Product.query.get_or_404(product_id)
    result = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock
    }
    return jsonify(result), 200


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product."""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product from the database."""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200

# ------------------------------
# Order API Endpoints
# ------------------------------

@app.route('/orders', methods=['POST'])
def create_order():
    """Create a new order with one or more products."""
    data = request.get_json()
    customer_name = data.get('customer_name')
    customer_email = data.get('customer_email')
    items = data.get('items')  # Expecting a list of dicts with product_id and quantity

    if not customer_name or not customer_email or not items:
        return jsonify({'error': 'Customer name, email, and order items are required.'}), 400

    order = Order(customer_name=customer_name, customer_email=customer_email)
    db.session.add(order)
    db.session.commit()  # Commit to assign an order ID

    for item in items:
        product_id = item.get('product_id')
        quantity = item.get('quantity', 1)
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Product with id {product_id} not found.'}), 404
        if product.stock < quantity:
            return jsonify({'error': f'Insufficient stock for product {product.name}.'}), 400
        
        # Deduct the quantity from the product stock
        product.stock -= quantity
        
        order_item = OrderItem(order_id=order.id, product_id=product_id, quantity=quantity)
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'Order created successfully', 'order_id': order.id}), 201

@app.route('/orders', methods=['GET'])
def list_orders():
    """Retrieve a list of all orders with their items."""
    orders = Order.query.all()
    result = []
    for order in orders:
        items = [{
            'product_id': item.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.product.price
        } for item in order.order_items]
        result.append({
            'order_id': order.id,
            'customer_name': order.customer_name,
            'customer_email': order.customer_email,
            'created_at': order.created_at.isoformat(),
            'items': items
        })
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
