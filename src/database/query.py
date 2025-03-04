"""
Functions for querying the database
"""

import sqlite3
import json
from src.utils.config import get_config


def get_db_connection():
    """Get a connection to the SQLite database"""
    config = get_config()
    db_path = config['database']['path']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_knowledge_base():
    """Get all knowledge base items"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get products
    cursor.execute('SELECT * FROM products')
    products = [dict(row) for row in cursor.fetchall()]

    # Get complaints
    cursor.execute('SELECT * FROM complaints')
    complaints = [dict(row) for row in cursor.fetchall()]

    # Get FAQs
    cursor.execute('SELECT * FROM faqs')
    faqs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        'products': products,
        'complaints': complaints,
        'faqs': faqs
    }


def get_product_by_id(product_id):
    """Get a product by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    conn.close()

    return dict(product) if product else None


def get_complaints_by_product(product_id):
    """Get complaints for a specific product"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM complaints WHERE product_id = ?', (product_id,))
    complaints = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return complaints


def get_faqs_by_product(product_id):
    """Get FAQs for a specific product"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM faqs WHERE product_id = ?', (product_id,))
    faqs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return faqs


def log_interaction(user_query, response, feedback=None):
    """Log user interaction for analysis"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create interactions table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        query TEXT,
        response TEXT,
        feedback TEXT
    )
    ''')

    # Insert new interaction
    cursor.execute(
        'INSERT INTO interactions (query, response, feedback) VALUES (?, ?, ?)',
        (user_query, response, feedback)
    )

    conn.commit()
    conn.close()
