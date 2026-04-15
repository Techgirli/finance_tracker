from datetime import datetime
from enum import Enum


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Category(Enum):
    # Expense categories
    FOOD = "Food & Dining"
    TRANSPORT = "Transportation"
    UTILITIES = "Utilities"
    ENTERTAINMENT = "Entertainment"
    SHOPPING = "Shopping"
    HEALTHCARE = "Healthcare"
    OTHER_EXPENSE = "Other Expense"

    # Income categories
    SALARY = "Salary"
    FREELANCE = "Freelance"
    INVESTMENT = "Investment"
    OTHER_INCOME = "Other Income"


class Transaction:
    def __init__(self, amount, category, transaction_type, description="", date=None):
        """
        Initialize a transaction

        Args:
            amount (float): Transaction amount
            category (Category): Transaction category
            transaction_type (TransactionType): INCOME or EXPENSE
            description (str): Optional description
            date (datetime): Transaction date (defaults to now)
        """
        self.id = None  # Will be set by database
        self.amount = float(amount)
        self.category = category
        self.transaction_type = transaction_type
        self.description = description
        self.date = date if date else datetime.now()

    def to_dict(self):
        """Convert transaction to dictionary for storage"""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category.value,
            'transaction_type': self.transaction_type.value,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S')
        }

    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary"""
        transaction = cls(
            amount=data['amount'],
            category=Category(data['category']),
            transaction_type=TransactionType(data['transaction_type']),
            description=data['description'],
            date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M:%S')
        )
        transaction.id = data['id']
        return transaction

    def __str__(self):
        sign = "+" if self.transaction_type == TransactionType.INCOME else "-"
        return f"{self.date.strftime('%Y-%m-%d')} | {sign}${self.amount:.2f} | {self.category.value} | {self.description}"
