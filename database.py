import sqlite3
from datetime import datetime
from transaction import Transaction, TransactionType, Category


class FinanceDatabase:
    def __init__(self, db_path='data/finance.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to SQLite database"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                month TEXT NOT NULL,
                UNIQUE(category, month)
            )
        ''')
        self.conn.commit()

    def add_transaction(self, transaction):
        """Add a new transaction to database"""
        try:
            self.cursor.execute('''
                INSERT INTO transactions (amount, category, transaction_type, description, date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                transaction.amount,
                transaction.category.value,
                transaction.transaction_type.value,
                transaction.description,
                transaction.date.strftime('%Y-%m-%d %H:%M:%S')
            ))
            self.conn.commit()
            transaction.id = self.cursor.lastrowid
            return transaction
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")
            return None

    def get_all_transactions(self):
        """Retrieve all transactions"""
        self.cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
        rows = self.cursor.fetchall()

        transactions = []
        for row in rows:
            trans_dict = {
                'id': row[0],
                'amount': row[1],
                'category': row[2],
                'transaction_type': row[3],
                'description': row[4],
                'date': row[5]
            }
            transactions.append(Transaction.from_dict(trans_dict))

        return transactions

    def get_transactions_by_date_range(self, start_date, end_date):
        """Get transactions within a date range"""
        self.cursor.execute('''
            SELECT * FROM transactions 
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC
        ''', (
            start_date.strftime('%Y-%m-%d 00:00:00'),
            end_date.strftime('%Y-%m-%d 23:59:59')
        ))

        rows = self.cursor.fetchall()
        transactions = []
        for row in rows:
            trans_dict = {
                'id': row[0],
                'amount': row[1],
                'category': row[2],
                'transaction_type': row[3],
                'description': row[4],
                'date': row[5]
            }
            transactions.append(Transaction.from_dict(trans_dict))

        return transactions

    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID"""
        try:
            self.cursor.execute(
                'DELETE FROM transactions WHERE id = ?', (transaction_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting transaction: {e}")
            return False

    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
