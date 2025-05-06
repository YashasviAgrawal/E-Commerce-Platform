# E-commerce REST API

A robust RESTful API for an e-commerce platform built with Flask and SQLAlchemy. This API provides endpoints for managing products and orders, making it suitable for building e-commerce applications.

## 🚀 Features

- **Product Management**
  - Create, read, update, and delete products
  - Track product inventory
  - Manage product details (name, description, price, stock)

- **Order Management**
  - Create new orders
  - View order history
  - Track order items and quantities
  - Automatic stock management

## 🛠️ Technology Stack

- **Backend Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **API Style**: RESTful
- **Data Format**: JSON

## 📋 Prerequisites

- Python 3.7+
- pip (Python package manager)

## 🔧 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ecommerce-website
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. The API will be available at `http://localhost:5000`

## 📚 API Documentation

### Products Endpoints

#### List All Products
- **GET** `/products`
- Returns a list of all products

#### Get Single Product
- **GET** `/products/<product_id>`
- Returns details of a specific product

#### Create Product
- **POST** `/products`
- Request Body:
```json
{
    "name": "Product Name",
    "description": "Product Description",
    "price": 99.99,
    "stock": 100
}
```

#### Update Product
- **PUT** `/products/<product_id>`
- Request Body: Same as Create Product

#### Delete Product
- **DELETE** `/products/<product_id>`

### Orders Endpoints

#### Create Order
- **POST** `/orders`
- Request Body:
```json
{
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "items": [
        {
            "product_id": 1,
            "quantity": 2
        }
    ]
}
```

#### List All Orders
- **GET** `/orders`
- Returns a list of all orders with their items

## 💾 Database Schema

### Product
- `id`: Integer (Primary Key)
- `name`: String (100)
- `price`: Integer
- `description`: String (500)
- `stock`: Integer

### Order
- `id`: Integer (Primary Key)
- `customer_name`: String (80)
- `customer_email`: String (120)
- `created_at`: DateTime

### OrderItem
- `id`: Integer (Primary Key)
- `order_id`: Integer (Foreign Key)
- `product_id`: Integer (Foreign Key)
- `quantity`: Integer

## 🔒 Error Handling

The API implements proper error handling for:
- Invalid requests
- Missing required fields
- Resource not found
- Insufficient stock
- Database errors

## 🧪 Testing

To run tests (when implemented):
```bash
python -m pytest
```

## 📝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Yashasvi Agrawal

## 🙏 Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- REST API best practices
