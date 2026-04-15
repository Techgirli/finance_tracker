from datetime import datetime
from transaction import Transaction, TransactionType, Category
from database import FinanceDatabase
from budget import BudgetManager
from visualizer import FinanceVisualizer


class FinanceTracker:
    def __init__(self):
        """Initialize the finance tracker"""
        self.db = FinanceDatabase()
        self.budget_manager = BudgetManager(self.db)
        self.visualizer = FinanceVisualizer(self.db)

    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*50)
        print("        PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. View Transactions by Date Range")
        print("4. Delete Transaction")
        print("5. Set Budget")
        print("6. View Budget Status")
        print("7. Generate Reports")
        print("8. Exit")
        print("="*50)

    def get_category_choice(self, transaction_type):
        """Let user choose a category"""
        if transaction_type == TransactionType.INCOME:
            categories = [cat for cat in Category if 'INCOME' in cat.name or cat.name ==
                          'SALARY' or cat.name == 'FREELANCE' or cat.name == 'INVESTMENT']
        else:
            categories = [cat for cat in Category if 'EXPENSE' in cat.name or cat.name in [
                'FOOD', 'TRANSPORT', 'UTILITIES', 'ENTERTAINMENT', 'SHOPPING', 'HEALTHCARE']]

        print("\nSelect Category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat.value}")

        while True:
            try:
                choice = int(input("Enter choice: "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a number.")

    def add_transaction(self):
        """Add a new transaction"""
        print("\n--- Add Transaction ---")

        # Get transaction type
        print("1. Income")
        print("2. Expense")
        type_choice = input("Select type (1-2): ")

        transaction_type = TransactionType.INCOME if type_choice == '1' else TransactionType.EXPENSE

        # Get amount
        while True:
            try:
                amount = float(input("Enter amount: $"))
                if amount > 0:
                    break
                print("Amount must be positive.")
            except ValueError:
                print("Please enter a valid number.")

        # Get category
        category = self.get_category_choice(transaction_type)

        # Get description
        description = input("Enter description (optional): ")

        # Get date
        date_input = input(
            "Enter date (YYYY-MM-DD) or press Enter for today: ")
        if date_input:
            try:
                date = datetime.strptime(date_input, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Using today's date.")
                date = datetime.now()
        else:
            date = datetime.now()

        # Create and save transaction
        transaction = Transaction(
            amount, category, transaction_type, description, date)
        result = self.db.add_transaction(transaction)

        if result:
            print(f"\n✓ Transaction added successfully! (ID: {result.id})")
        else:
            print("\n✗ Failed to add transaction.")

    def view_all_transactions(self):
        """Display all transactions"""
        print("\n--- All Transactions ---")
        transactions = self.db.get_all_transactions()

        if not transactions:
            print("No transactions found.")
            return

        total_income = sum(
            t.amount for t in transactions if t.transaction_type == TransactionType.INCOME)
        total_expenses = sum(
            t.amount for t in transactions if t.transaction_type == TransactionType.EXPENSE)

        print(
            f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<20} {'Amount':<12} {'Description'}")
        print("-" * 90)

        for trans in transactions:
            trans_type = "Income" if trans.transaction_type == TransactionType.INCOME else "Expense"
            amount_str = f"${trans.amount:.2f}"
            print(f"{trans.id:<5} {trans.date.strftime('%Y-%m-%d'):<12} {trans_type:<10} {trans.category.value:<20} {amount_str:<12} {trans.description}")

        print("-" * 90)
        print(f"\nTotal Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net: ${total_income - total_expenses:.2f}")

    def view_transactions_by_date(self):
        """View transactions within a date range"""
        print("\n--- View Transactions by Date ---")

        try:
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")

            start_date = datetime.strptime(start, '%Y-%m-%d')
            end_date = datetime.strptime(end, '%Y-%m-%d')

            transactions = self.db.get_transactions_by_date_range(
                start_date, end_date)

            if not transactions:
                print("No transactions found in this date range.")
                return

            print(
                f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<20} {'Amount':<12} {'Description'}")
            print("-" * 90)

            for trans in transactions:
                trans_type = "Income" if trans.transaction_type == TransactionType.INCOME else "Expense"
                amount_str = f"${trans.amount:.2f}"
                print(f"{trans.id:<5} {trans.date.strftime('%Y-%m-%d'):<12} {trans_type:<10} {trans.category.value:<20} {amount_str:<12} {trans.description}")

        except ValueError:
            print("Invalid date format.")

    def delete_transaction(self):
        """Delete a transaction by ID"""
        print("\n--- Delete Transaction ---")

        try:
            trans_id = int(input("Enter transaction ID to delete: "))
            confirm = input(
                f"Are you sure you want to delete transaction {trans_id}? (yes/no): ")

            if confirm.lower() == 'yes':
                if self.db.delete_transaction(trans_id):
                    print("✓ Transaction deleted successfully!")
                else:
                    print("✗ Failed to delete transaction.")
        except ValueError:
            print("Invalid ID.")

    def set_budget(self):
        """Set budget for a category"""
        print("\n--- Set Budget ---")

        category = self.get_category_choice(TransactionType.EXPENSE)

        while True:
            try:
                amount = float(
                    input(f"Enter monthly budget for {category.value}: $"))
                if amount > 0:
                    break
                print("Amount must be positive.")
            except ValueError:
                print("Please enter a valid number.")

        month = input(
            "Enter month (YYYY-MM) or press Enter for current month: ")
        if not month:
            month = None

        if self.budget_manager.set_budget(category, amount, month):
            print("✓ Budget set successfully!")
        else:
            print("✗ Failed to set budget.")

    def view_budget_status(self):
        """View budget vs spending comparison"""
        print("\n--- Budget Status ---")

        month = input(
            "Enter month (YYYY-MM) or press Enter for current month: ")
        if not month:
            month = None

        comparison = self.budget_manager.get_spending_vs_budget(month)

        if not comparison:
            print("No budgets set for this month.")
            return

        print(
            f"\n{'Category':<20} {'Budget':<12} {'Spent':<12} {'Remaining':<12} {'%Used':<10} {'Status'}")
        print("-" * 85)

        for category, data in comparison.items():
            status = "⚠ OVER" if data['status'] == 'over' else "✓ OK"
            print(
                f"{category:<20} ${data['budget']:<11.2f} ${data['spent']:<11.2f} ${data['remaining']:<11.2f} {data['percentage']:<9.1f}% {status}")

    def generate_reports(self):
        """Generate visual reports"""
        print("\n--- Generate Reports ---")
        print("1. Spending by Category (Pie Chart)")
        print("2. Income vs Expenses Over Time")
        print("3. Budget Progress")
        print("4. All Reports")

        choice = input("Select report (1-4): ")

        month = input("Enter month (YYYY-MM) or press Enter for current: ")
        if not month:
            month = None

        if choice == '1':
            self.visualizer.plot_spending_by_category(
                month, f'reports/spending_by_category_{month or datetime.now().strftime("%Y-%m")}.png')
            print("✓ Report saved to reports/ folder")
        elif choice == '2':
            self.visualizer.plot_income_vs_expenses(
                save_path=f'reports/income_vs_expenses.png')
            print("✓ Report saved to reports/ folder")
        elif choice == '3':
            self.visualizer.plot_budget_progress(
                self.budget_manager, month, f'reports/budget_progress_{month or datetime.now().strftime("%Y-%m")}.png')
            print("✓ Report saved to reports/ folder")
        elif choice == '4':
            self.visualizer.plot_spending_by_category(
                month, f'reports/spending_by_category_{month or datetime.now().strftime("%Y-%m")}.png')
            self.visualizer.plot_income_vs_expenses(
                save_path=f'reports/income_vs_expenses.png')
            self.visualizer.plot_budget_progress(
                self.budget_manager, month, f'reports/budget_progress_{month or datetime.now().strftime("%Y-%m")}.png')
            print("✓ All reports saved to reports/ folder")

    def run(self):
        """Main application loop"""
        print("\nWelcome to Personal Finance Tracker!")

        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ")

            if choice == '1':
                self.add_transaction()
            elif choice == '2':
                self.view_all_transactions()
            elif choice == '3':
                self.view_transactions_by_date()
            elif choice == '4':
                self.delete_transaction()
            elif choice == '5':
                self.set_budget()
            elif choice == '6':
                self.view_budget_status()
            elif choice == '7':
                self.generate_reports()
            elif choice == '8':
                print("\nThank you for using Finance Tracker!")
                self.db.close()
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = FinanceTracker()
    app.run()
