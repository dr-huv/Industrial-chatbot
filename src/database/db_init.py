import sqlite3
import json
import os


def initialize_database():
    """Initialize the database with tables for products, complaints, and FAQs"""
    conn = sqlite3.connect('data/industrial_knowledge.db')
    cursor = conn.cursor()

    # Create tables for products, complaints, and FAQs
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category TEXT,
        description TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        issue_type TEXT,
        description TEXT,
        solution TEXT,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY,
        product_id INTEGER,
        question TEXT,
        answer TEXT,
        category TEXT,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    ''')

    # Load sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        load_sample_data(conn, cursor)

    conn.commit()
    return conn


def load_sample_data(conn, cursor):
    """Load sample data from JSON files"""
    # Load products
    with open('data/products.json', 'r') as f:
        products = json.load(f)
        cursor.executemany(
            'INSERT INTO products (id, name, category, description) VALUES (?, ?, ?, ?)',
            [(p['id'], p['name'], p['category'], p['description'])
             for p in products]
        )

    # Load complaints
    with open('data/complaints.json', 'r') as f:
        complaints = json.load(f)
        cursor.executemany(
            'INSERT INTO complaints (id, product_id, issue_type, description, solution) VALUES (?, ?, ?, ?, ?)',
            [(c['id'], c['product_id'], c['issue_type'],
              c['description'], c['solution']) for c in complaints]
        )

    # Load FAQs
    with open('data/faqs.json', 'r') as f:
        faqs = json.load(f)
        cursor.executemany(
            'INSERT INTO faqs (id, product_id, question, answer, category) VALUES (?, ?, ?, ?, ?)',
            [(q['id'], q['product_id'], q['question'],
              q['answer'], q['category']) for q in faqs]
        )

    conn.commit()


if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    initialize_database()
