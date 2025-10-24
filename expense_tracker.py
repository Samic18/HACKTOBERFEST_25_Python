import json
import os
from datetime import datetime
import matplotlib.pyplot as plt

DATA_FILE = "expenses.json"

class Expense:
    def __init__(self, amount, category, description="", date=None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now().isoformat()

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.load_expenses()

    def load_expenses(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for item in data:
                    self.expenses.append(Expense(**item))

    def save_expenses(self):
        with open(DATA_FILE, "w") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=2)

    def add_expense(self):
        try:
            amount = float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount!")
            return
        category = input("Enter category (Food, Transport, Bills, etc.): ").strip()
        description = input("Enter description (optional): ").strip()
        expense = Expense(amount, category, description)
        self.expenses.append(expense)
        self.save_expenses()
        print("✅ Expense added successfully!")

    def list_expenses(self):
        if not self.expenses:
            print("No expenses yet!")
            return
        print("\n=== Expenses ===")
        for i, e in enumerate(sorted(self.expenses, key=lambda x: x.date), 1):
            print(f"{i}. {e.date} - {e.category}: ${e.amount} ({e.description})")

    def summary_by_category(self):
        summary = {}
        for e in self.expenses:
            summary[e.category] = summary.get(e.category, 0) + e.amount
        print("\n=== Summary by Category ===")
        for cat, amt in summary.items():
            print(f"{cat}: ${amt}")
        return summary

    def plot_summary(self):
        summary = self.summary_by_category()
        if not summary:
            return
        categories = list(summary.keys())
        amounts = list(summary.values())
        plt.figure(figsize=(8,6))
        plt.bar(categories, amounts, color='skyblue')
        plt.title("Expenses by Category")
        plt.ylabel("Amount ($)")
        plt.show()

    def run(self):
        while True:
            print("\n=== Personal Expense Tracker ===")
            print("1. Add Expense")
            print("2. List Expenses")
            print("3. Summary by Category")
            print("4. Plot Summary")
            print("5. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.list_expenses()
            elif choice == "3":
                self.summary_by_category()
            elif choice == "4":
                self.plot_summary()
            elif choice == "5":
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()
