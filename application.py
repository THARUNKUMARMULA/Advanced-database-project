# application.py

import sqlite3
from bottle import Bottle, run, template, request, redirect

app = Bottle()

# SQLite3 Database Connection
db_path = "database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create tables if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS car_rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_model TEXT NOT NULL,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers(id)
    )
""")

# Sample data insertion for testing
cursor.execute("INSERT INTO customers (name, email) VALUES ('John Doe', 'john@example.com')")
cursor.execute("INSERT INTO customers (name, email) VALUES ('Jane Smith', 'jane@example.com')")
cursor.execute("INSERT INTO car_rentals (car_model, customer_id) VALUES ('Toyota Camry', 1)")
cursor.execute("INSERT INTO car_rentals (car_model, customer_id) VALUES ('Honda Accord', 2)")
conn.commit()

# CRUD Operations

# Create
@app.route('/add')
def add_form():
    return template('add_form')

@app.route('/add', method='POST')
def add_submit():
    name = request.forms.get('name')
    email = request.forms.get('email')
    car_model = request.forms.get('car_model')

    # Check if customer already exists
    cursor.execute("SELECT id FROM customers WHERE email=?", (email,))
    customer_id = cursor.fetchone()

    if not customer_id:
        # If customer does not exist, create a new one
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
        customer_id = cursor.lastrowid
    else:
        customer_id = customer_id[0]

    # Create car rental entry
    cursor.execute("INSERT INTO car_rentals (car_model, customer_id) VALUES (?, ?)", (car_model, customer_id))
    conn.commit()

    redirect('/')

# Read with Search
@app.route('/')
def index():
    search_term = request.query.get('search', '').strip()

    try:
        if search_term:
            cursor.execute("""
                SELECT car_rentals.id, car_rentals.car_model, customers.name, customers.email
                FROM car_rentals
                INNER JOIN customers ON car_rentals.customer_id = customers.id
                WHERE customers.name LIKE ?
            """, ('%' + search_term + '%',))
        else:
            cursor.execute("""
                SELECT car_rentals.id, car_rentals.car_model, customers.name, customers.email
                FROM car_rentals
                INNER JOIN customers ON car_rentals.customer_id = customers.id
            """)
        result = cursor.fetchall()
    except Exception as e:
        # Print the exception details for debugging
        print(f"Error: {e}")
        result = []

    return template('index', rows=result, search_term=search_term)

# Update
@app.route('/edit/<id>')
def edit_form(id):
    cursor.execute("""
        SELECT car_rentals.id, car_rentals.car_model, customers.name, customers.email
        FROM car_rentals
        INNER JOIN customers ON car_rentals.customer_id = customers.id
        WHERE car_rentals.id=?
    """, (id,))
    result = cursor.fetchone()

    return template('edit_form', row=result)

@app.route('/edit/<id>', method='POST')
def edit_submit(id):
    car_model = request.forms.get('car_model')

    cursor.execute("UPDATE car_rentals SET car_model=? WHERE id=?", (car_model, id))
    conn.commit()

    redirect('/')

# Delete
@app.route('/delete/<id>')
def delete_confirm(id):
    cursor.execute("""
        SELECT car_rentals.id, car_rentals.car_model, customers.name, customers.email
        FROM car_rentals
        INNER JOIN customers ON car_rentals.customer_id = customers.id
        WHERE car_rentals.id=?
    """, (id,))
    result = cursor.fetchone()

    return template('delete_confirm', row=result)

@app.route('/delete/<id>', method='POST')
def delete_submit(id):
    cursor.execute("DELETE FROM car_rentals WHERE id=?", (id,))
    conn.commit()

    redirect('/')

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
