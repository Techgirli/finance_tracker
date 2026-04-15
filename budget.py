from datetime import datetime
from calendar import monthrange  # Add this import at the top
from transaction import Category


class BudgetManager:
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database

    def set_budget(self, category, amount, month=None):
        """Set budget for a category for a specific month"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')

        try:
            self.db.cursor.execute('''
                INSERT OR REPLACE INTO budgets (category, amount, month)
                VALUES (?, ?, ?)
            ''', (category.value, amount, month))
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Error setting budget: {e}")
            return False

    def get_budget(self, category, month=None):
        """Get budget for a category"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')

        self.db.cursor.execute('''
            SELECT amount FROM budgets 
            WHERE category = ? AND month = ?
        ''', (category.value, month))

        result = self.db.cursor.fetchone()
        return result[0] if result else None

    def get_spending_vs_budget(self, month=None):
        """Compare actual spending to budgets"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')

        # Get all budgets for the month
        self.db.cursor.execute(
            'SELECT category, amount FROM budgets WHERE month = ?', (month,))
        budgets = {row[0]: row[1] for row in self.db.cursor.fetchall()}

        # Get actual spending - FIXED DATE CALCULATION
        year, month_num = map(int, month.split('-'))

        # Get the first day of the month
        start_date = datetime(year, month_num, 1)

        # Get the last day of the month using monthrange
        last_day = monthrange(year, month_num)[1]
        end_date = datetime(year, month_num, last_day, 23, 59, 59)

        transactions = self.db.get_transactions_by_date_range(
            start_date, end_date)

        spending = {}
        for trans in transactions:
            if trans.transaction_type.value == 'expense':
                cat = trans.category.value
                spending[cat] = spending.get(cat, 0) + trans.amount

        # Compare
        comparison = {}
        for category, budget_amount in budgets.items():
            actual = spending.get(category, 0)
            remaining = budget_amount - actual
            percentage = (actual / budget_amount *
                          100) if budget_amount > 0 else 0

            comparison[category] = {
                'budget': budget_amount,
                'spent': actual,
                'remaining': remaining,
                'percentage': percentage,
                'status': 'over' if remaining < 0 else 'under'
            }

        return comparison
