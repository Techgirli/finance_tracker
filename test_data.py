from datetime import datetime, timedelta
from transaction import Transaction, TransactionType, Category
from database import FinanceDatabase

db = FinanceDatabase()

# Add sample income
transactions = [
    Transaction(3000, Category.SALARY, TransactionType.INCOME,
                "Monthly salary", datetime.now() - timedelta(days=25)),
    Transaction(500, Category.FREELANCE, TransactionType.INCOME,
                "Freelance project", datetime.now() - timedelta(days=20)),

    # Add sample expenses
    Transaction(800, Category.UTILITIES, TransactionType.EXPENSE,
                "Rent", datetime.now() - timedelta(days=24)),
    Transaction(150, Category.FOOD, TransactionType.EXPENSE,
                "Groceries", datetime.now() - timedelta(days=22)),
    Transaction(45, Category.TRANSPORT, TransactionType.EXPENSE,
                "Gas", datetime.now() - timedelta(days=20)),
    Transaction(60, Category.ENTERTAINMENT, TransactionType.EXPENSE,
                "Movie and dinner", datetime.now() - timedelta(days=18)),
    Transaction(120, Category.FOOD, TransactionType.EXPENSE,
                "Restaurants", datetime.now() - timedelta(days=15)),
    Transaction(200, Category.SHOPPING, TransactionType.EXPENSE,
                "Clothes", datetime.now() - timedelta(days=10)),
    Transaction(75, Category.UTILITIES, TransactionType.EXPENSE,
                "Electric bill", datetime.now() - timedelta(days=8)),
    Transaction(50, Category.HEALTHCARE, TransactionType.EXPENSE,
                "Pharmacy", datetime.now() - timedelta(days=5)),
]

for trans in transactions:
    db.add_transaction(trans)
    print(f"Added: {trans}")

print("\nSample data added successfully!")
db.close()
