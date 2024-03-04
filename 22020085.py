import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta  # Importing datetime and timedelta modules

# Initialize Faker library
fake = Faker()

# Define a list of common product categories
product_categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys', 'Beauty', 'Sports & Outdoors']

# Connect to SQLite database
conn = sqlite3.connect('online_retail.db')
c = conn.cursor()

# Create Customers table with the 'address' column
c.execute('''CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                email TEXT,
                phone_number TEXT,
                address TEXT,  
                city TEXT,
                country TEXT
            )''')

# Create Orders table
c.execute('''CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT,
                total_amount REAL,
                shipping_address TEXT,
                shipping_city TEXT,
                shipping_country TEXT,
                FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
            )''')

# Create Products table
c.execute('''CREATE TABLE IF NOT EXISTS Products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT,
                category TEXT,
                price REAL,
                description TEXT,
                stock_quantity INTEGER,
                supplier TEXT
            )''')

# Generate and insert random data for Customers
for _ in range(1000):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    phone_number = fake.phone_number()
    address = fake.street_address()
    city = fake.city()
    country = fake.country()
    
    c.execute("INSERT INTO Customers (first_name, last_name, email, phone_number, address, city, country) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (first_name, last_name, email, phone_number, address, city, country))

# Generate and insert random data for Products
for _ in range(100):
    product_name = fake.word()
    category = random.choice(product_categories)  # Select a random product category
    price = round(random.uniform(10, 1000), 2)
    description = fake.sentence()
    stock_quantity = random.randint(1, 100)
    supplier = fake.company()
    
    c.execute("INSERT INTO Products (product_name, category, price, description, stock_quantity, supplier) VALUES (?, ?, ?, ?, ?, ?)",
              (product_name, category, price, description, stock_quantity, supplier))

# Generate and insert random data for Orders
for _ in range(1000):
    customer_id = random.randint(1, 1000)
    order_date = fake.date_time_between(start_date='-1y', end_date='now')
    total_amount = round(random.uniform(10, 1000), 2)
    shipping_address = fake.street_address()
    shipping_city = fake.city()
    shipping_country = fake.country()
    
    c.execute("INSERT INTO Orders (customer_id, order_date, total_amount, shipping_address, shipping_city, shipping_country) VALUES (?, ?, ?, ?, ?, ?)",
              (customer_id, order_date.strftime('%Y-%m-%d'), total_amount, shipping_address, shipping_city, shipping_country))



# Execute the SQL query
c.execute("SELECT * FROM Customers LIMIT 5")

# Fetch and print the results
rows = c.fetchall()
for row in rows:
    print(row)
    

# Commit changes and close connection
conn.commit()
conn.close()