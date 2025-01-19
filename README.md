# Flask CRM Application

This is a Customer Relationship Management (CRM) application built with Flask. The application provides functionalities to manage users, products, customers, sales, and roles. It supports user authentication, role-based access control, and various data import/export features.

## Features

- User Authentication and Role-Based Access Control
- Manage Users, Products, Customers, and Sales
- Import and Export Data in CSV and JSON formats
- Search Functionality for Users, Products, Customers, and Sales

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/flask-crm.git
    cd flask-crm
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the configuration in `config.py`.

5. Initialize the database:
    ```bash
    flask db upgrade
    ```

6. Run the application:
    ```bash
    flask run
    ```

## Configuration

The application uses a `Config` class for configuration settings. You can customize the settings in the `config.py` file.

## Usage

### User Management

- Add, update, delete, and search for users.
- Assign roles to users to control access permissions.

### Product Management

- Add, update, delete, and search for products.
- Import and export product data in CSV and JSON formats.

### Customer Management

- Add, update, delete, and search for customers.
- export customer data in CSV and JSON formats.

### Sales Management

- Add, update, delete, and search for sales.
- Import and export sale data in CSV and JSON formats.

## Routes

### Auth Routes

- `/` (GET, POST): Login page.
- `/logout` (GET): Logout the current user.

### Main Routes

- `/main` (GET): Dashboard showing counts of users, customers, products, and sales.

### Sales Routes

- `/sales` (GET): View sales.
- `/sales/search_sale/` (GET, POST): Search for sales.
- `/sales/add_sale/` (GET, POST): Add a new sale.
- `/sales/info_sale/<int:id>` (GET): View information about a single sale.
- `/sales/delete_sale/<int:id>` (GET): Delete a sale.
- `/sales/update_sale/<int:id>` (GET, POST): Update a sale.
- `/sales/download_sales` (GET): Download sale data in CSV or JSON format.
- `/sales/upload_sales` (GET, POST): Upload sale data from a CSV or JSON file.

### User Routes

- `/users` (GET): View users.
- `/users/search_user/` (GET, POST): Search for users.
- `/users/add_user/` (GET, POST): Add a new user.
- `/users/info_user/<int:id>` (GET): View information about a single user.
- `/users/delete_user/<int:id>` (GET): Delete a user.
- `/users/update_user/<int:id>` (GET, POST): Update a user.

### Product Routes

- `/products` (GET): View products.
- `/products/search_product/` (GET, POST): Search for products.
- `/products/add_product/` (GET, POST): Add a new product.
- `/products/info_product/<int:id>` (GET): View information about a single product.
- `/products/delete_product/<int:id>` (GET): Delete a product.
- `/products/update_product/<int:id>` (GET, POST): Update a product.
- `/products/download_products` (GET): Download product data in CSV or JSON format.
- `/products/upload_product` (GET, POST): Upload product data from a CSV or JSON file.

### Customer Routes

- `/customers` (GET): View customers.
- `/customers/search_customer/` (GET, POST): Search for customers.
- `/customers/download_customers` (GET): Download customer data in CSV or JSON format.


## Contact

For any inquiries, please contact [amiragamal098@gmail.com].

