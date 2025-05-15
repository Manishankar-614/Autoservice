from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize the database if not already present
def init_db():
    conn = sqlite3.connect('autoservice.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_type TEXT NOT NULL,
            service_date TEXT NOT NULL,
            service_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Insert a booking into the database
def insert_booking(service_type, service_date, service_time):
    conn = sqlite3.connect('autoservice.db')
    c = conn.cursor()
    c.execute('INSERT INTO bookings (service_type, service_date, service_time) VALUES (?, ?, ?)',
              (service_type, service_date, service_time))
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint to book a service
@app.route('/api/book', methods=['POST'])
def book_service():
    data = request.json
    required_fields = ['serviceType', 'serviceDate', 'serviceTime']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    insert_booking(data['serviceType'], data['serviceDate'], data['serviceTime'])
    return jsonify({'message': 'Booking confirmed!'}), 200

# API endpoint to get all bookings
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    conn = sqlite3.connect('autoservice.db')
    c = conn.cursor()
    c.execute('SELECT id, service_type, service_date, service_time FROM bookings')
    rows = c.fetchall()
    conn.close()
    bookings = [
        {'id': row[0], 'service_type': row[1], 'service_date': row[2], 'service_time': row[3]}
        for row in rows
    ]
    return jsonify(bookings)

# Main entry point
if __name__ == '__main__':
    init_db()
    app.run(debug=True)

