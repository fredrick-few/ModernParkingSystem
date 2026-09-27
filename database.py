import sqlite3
from datetime import datetime

DB_NAME = "parking_system.db"

def init_db():
    """Initializes SQLite database schemas for active tickets and completed transactions."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Active Parked Vehicles Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT NOT NULL,
            slot_id INTEGER NOT NULL,
            entry_time TEXT NOT NULL
        )
    ''')

    # Financial Audit Transactions Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            plate_number TEXT NOT NULL,
            slot_id INTEGER NOT NULL,
            entry_time TEXT NOT NULL,
            exit_time TEXT NOT NULL,
            duration_minutes REAL NOT NULL,
            fee_charged REAL NOT NULL,
            payment_method TEXT NOT NULL,
            payment_status TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def save_active_ticket(plate_number: str, slot_id: int, entry_time: datetime) -> int:
    """Saves a newly parked vehicle to active_tickets table and returns generated ticket_id."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO active_tickets (plate_number, slot_id, entry_time)
        VALUES (?, ?, ?)
    ''', (plate_number, slot_id, entry_time.isoformat()))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return ticket_id

def get_active_ticket(plate_number: str):
    """Retrieves active ticket data for a vehicle attempting to exit."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ticket_id, plate_number, slot_id, entry_time 
        FROM active_tickets 
        WHERE plate_number = ?
    ''', (plate_number,))
    ticket = cursor.fetchone()
    conn.close()
    return ticket

def remove_active_ticket(ticket_id: int):
    """Removes a ticket from active_tickets upon successful exit and payment."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM active_tickets WHERE ticket_id = ?', (ticket_id,))
    conn.commit()
    conn.close()

def log_transaction(plate_number: str, slot_id: int, entry_time: str, exit_time: str,
                    duration_minutes: float, fee_charged: float, payment_method: str, payment_status: str):
    """Logs a completed parking transaction to the permanent audit log."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transactions (plate_number, slot_id, entry_time, exit_time, duration_minutes, fee_charged, payment_method, payment_status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (plate_number, slot_id, entry_time, exit_time, duration_minutes, fee_charged, payment_method, payment_status))
    conn.commit()
    conn.close()