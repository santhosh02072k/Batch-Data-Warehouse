"""
Generate Sample E-Commerce Data
Creates realistic orders, customers, and products datasets
for the batch data warehouse pipeline.
"""

import csv
import random
import os
from datetime import datetime, timedelta

OUTPUT_DIR = "data/raw"
NUM_CUSTOMERS = 500
NUM_PRODUCTS = 100
NUM_ORDERS = 10000

REGIONS = ['UAE', 'KSA', 'Egypt', 'Kuwait', 'Bahrain', 'Oman', 'Qatar']
CATEGORIES = ['Electronics', 'Clothing', 'Home', 'Sports', 'Books', 'Food', 'Beauty']
PLATFORMS = ['mobile', 'web', 'app']


def generate_customers():
    """Generate customer dimension data."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "customers.csv")

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['customer_id', 'name', 'email', 'region', 'signup_date', 'platform'])

        for i in range(1, NUM_CUSTOMERS + 1):
            signup = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 730))
            writer.writerow([
                f"CUST_{i:05d}",
                f"Customer_{i}",
                f"customer_{i}@email.com",
                random.choice(REGIONS),
                signup.strftime('%Y-%m-%d'),
                random.choice(PLATFORMS)
            ])

    print(f"Generated {NUM_CUSTOMERS} customers at {filepath}")


def generate_products():
    """Generate product dimension data."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "products.csv")

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['product_id', 'name', 'category', 'price', 'brand'])

        for i in range(1, NUM_PRODUCTS + 1):
            category = random.choice(CATEGORIES)
            price = round(random.uniform(5, 500), 2)
            writer.writerow([
                f"PROD_{i:05d}",
                f"Product_{category}_{i}",
                category,
                price,
                f"Brand_{random.randint(1, 20)}"
            ])

    print(f"Generated {NUM_PRODUCTS} products at {filepath}")


def generate_orders():
    """Generate order fact data."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, "orders.csv")

    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'order_id', 'customer_id', 'product_id', 'quantity',
            'unit_price', 'total_amount', 'order_date', 'status'
        ])

        statuses = ['completed', 'completed', 'completed', 'pending', 'cancelled']

        for i in range(1, NUM_ORDERS + 1):
            customer_id = f"CUST_{random.randint(1, NUM_CUSTOMERS):05d}"
            product_id = f"PROD_{random.randint(1, NUM_PRODUCTS):05d}"
            quantity = random.randint(1, 5)
            unit_price = round(random.uniform(5, 500), 2)
            total = round(quantity * unit_price, 2)
            order_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))

            writer.writerow([
                f"ORD_{i:06d}",
                customer_id,
                product_id,
                quantity,
                unit_price,
                total,
                order_date.strftime('%Y-%m-%d'),
                random.choice(statuses)
            ])

    print(f"Generated {NUM_ORDERS} orders at {filepath}")


if __name__ == "__main__":
    print("Generating sample e-commerce data...")
    generate_customers()
    generate_products()
    generate_orders()
    print("Done! Data ready for ETL pipeline.")
