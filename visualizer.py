import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict
from transaction import TransactionType


class FinanceVisualizer:
    def __init__(self, database):
        """Initialize with database connection"""
        self.db = database

    def plot_spending_by_category(self, month=None, save_path=None):
        """Create pie chart of spending by category"""
        if month is None:
            month = datetime.now().strftime('%Y-%m')

        start_date = datetime.strptime(f"{month}-01", '%Y-%m-%d')
        end_date = datetime.strptime(f"{month}-31", '%Y-%m-%d')

        transactions = self.db.get_transactions_by_date_range(
            start_date, end_date)

        # Aggregate spending by category
        spending = defaultdict(float)
        for trans in transactions:
            if trans.transaction_type == TransactionType.EXPENSE:
                spending[trans.category.value] += trans.amount

        if not spending:
            print("No expenses found for this period")
            return

        # Create pie chart
        categories = list(spending.keys())
        amounts = list(spending.values())

        plt.figure(figsize=(10, 8))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title(f'Spending by Category - {month}')
        plt.axis('equal')

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

        plt.close()

    def plot_income_vs_expenses(self, months=6, save_path=None):
        """Plot income vs expenses over time"""
        # Get transactions for last N months
        end_date = datetime.now()
        start_date = datetime(end_date.year, end_date.month - months + 1, 1)

        transactions = self.db.get_transactions_by_date_range(
            start_date, end_date)

        # Aggregate by month
        monthly_income = defaultdict(float)
        monthly_expenses = defaultdict(float)

        for trans in transactions:
            month_key = trans.date.strftime('%Y-%m')
            if trans.transaction_type == TransactionType.INCOME:
                monthly_income[month_key] += trans.amount
            else:
                monthly_expenses[month_key] += trans.amount

        # Sort months
        all_months = sorted(
            set(list(monthly_income.keys()) + list(monthly_expenses.keys())))

        income_values = [monthly_income[m] for m in all_months]
        expense_values = [monthly_expenses[m] for m in all_months]

        # Create bar chart
        x = range(len(all_months))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar([i - width/2 for i in x], income_values, width,
               label='Income', color='green', alpha=0.7)
        ax.bar([i + width/2 for i in x], expense_values,
               width, label='Expenses', color='red', alpha=0.7)

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_title('Income vs Expenses Over Time')
        ax.set_xticks(x)
        ax.set_xticklabels(all_months, rotation=45)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

        plt.close()

    def plot_budget_progress(self, budget_manager, month=None, save_path=None):
        """Visualize budget vs actual spending"""
        comparison = budget_manager.get_spending_vs_budget(month)

        if not comparison:
            print("No budget data available")
            return

        categories = list(comparison.keys())
        budgets = [comparison[c]['budget'] for c in categories]
        spent = [comparison[c]['spent'] for c in categories]

        x = range(len(categories))
        width = 0.35

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar([i - width/2 for i in x], budgets, width,
               label='Budget', color='blue', alpha=0.7)
        ax.bar([i + width/2 for i in x], spent, width,
               label='Spent', color='orange', alpha=0.7)

        # Add warning color for over-budget
        for i, cat in enumerate(categories):
            if comparison[cat]['status'] == 'over':
                ax.bar(i + width/2, spent[i], width, color='red', alpha=0.7)

        ax.set_xlabel('Category')
        ax.set_ylabel('Amount ($)')
        ax.set_title(
            f'Budget vs Actual Spending - {month or datetime.now().strftime("%Y-%m")}')
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

        plt.close()
