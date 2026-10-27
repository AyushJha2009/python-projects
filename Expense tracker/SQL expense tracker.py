
import sqlite3

# Connect to the database
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()

# Create tables if they do not already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS budget (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    amount REAL NOT NULL
)
""")

conn.commit()


def add_budget():
    amount = float(input("Enter your budget: "))

    if amount <= 0:
        print("Please enter a budget greater than zero.")
        return

    cursor.execute(
        "INSERT INTO budget (amount) VALUES (?)",
        (amount,)
    )
    conn.commit()
    print("Budget saved successfully!")


def add_expense():
    print("\nChoose the type of expense")
    print("1) Food")
    print("2) Grocery")
    print("3) Entertainment")

    choice = input("Choose operation: ")

    categories = {
        "1": "Food",
        "2": "Grocery",
        "3": "Entertainment"
    }

    if choice not in categories:
        print("Invalid category!")
        return

    amount = float(input("Enter expense amount: "))

    if amount <= 0:
        print("Expense must be greater than zero.")
        return

    category = categories[choice]

    cursor.execute(
        "INSERT INTO expenses (category, amount) VALUES (?, ?)",
        (category, amount)
    )
    conn.commit()

    print("Expense saved successfully!")


def total_expense():
    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    rows = cursor.fetchall()
    total = 0

    for category, amount in rows:
        print(f"{category}: ₹{amount:.2f}")
        total += amount

    print(f"Total expenses: ₹{total:.2f}")


def total_budget():
    cursor.execute("SELECT SUM(amount) FROM budget")
    result = cursor.fetchone()[0]
    print(f"Total budget: ₹{result or 0:.2f}")


def remaining_budget():
    cursor.execute("SELECT SUM(amount) FROM budget")
    budget_total = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM expenses")
    expense_total = cursor.fetchone()[0] or 0

    remaining = budget_total - expense_total
    print(f"Remaining budget: ₹{remaining:.2f}")


while True:
    print("\n===== EXPENSE TRACKER =====")
    print("1) Add budget")
    print("2) Add expenses")
    print("3) Total expenses")
    print("4) Total budget")
    print("5) Remaining budget")
    print("6) Exit")

    answer = input("Enter operation number: ")

    try:
        if answer == "1":
            add_budget()
        elif answer == "2":
            add_expense()
        elif answer == "3":
            total_expense()
        elif answer == "4":
            total_budget()
        elif answer == "5":
            remaining_budget()
        elif answer == "6":
            print("Thank you for using Expense Tracker!")
            break
        else:
            print("Invalid operation. Choose 1 to 6.")

    except ValueError:
        print("Please enter a valid numeric amount.")

conn.close()
