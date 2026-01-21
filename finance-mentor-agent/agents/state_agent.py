from memory.storage import StorageEngine
from typing import Dict, Any

class FinancialStateAgent:
    """
    Agent responsible for maintaining the user's financial 'Truth'.
    Wraps the storage engine with semantic business logic.
    """
    def __init__(self, db_path: str = "finance_data.json"):
        self.storage = StorageEngine(db_path)

    def get_profile(self) -> Dict[str, Any]:
        return self.storage.get_user_profile()

    def update_profile(self, income: float, savings_goal: float):
        self.storage.update_user_profile(income, savings_goal)

    def add_fixed_expense(self, name: str, amount: float):
        self.storage.add_fixed_expense(name, amount)

    def get_total_fixed_expenses(self) -> float:
        expenses = self.storage.get_fixed_expenses()
        return sum(e["amount"] for e in expenses)

    def log_transaction(self, item_name: str, amount: float, category: str):
        """
        Logs a confirmed purchase into the persistent record.
        """
        from datetime import datetime
        transaction = {
            "date": datetime.now().isoformat(),
            "description": item_name,
            "amount": amount,
            "category": category,
            "type": "expense"
        }
        self.storage.log_transaction(transaction)

    def get_todays_state(self) -> Dict[str, Any]:
        """Returns a snapshot of the current financial state."""
        profile = self.get_profile()
        fixed = self.get_total_fixed_expenses()
        
        # Calculate total variable expenses (spending)
        transactions = self.storage.get_transactions()
        variable_spend = sum(t['amount'] for t in transactions if t.get('type') == 'expense')
        
        return {
            "income": profile.get("monthly_income", 0),
            "total_fixed_expenses": fixed,
            "variable_expenses": variable_spend,
            "savings_goal": profile.get("savings_goal", 0),
            "free_cash_flow": profile.get("monthly_income", 0) - fixed - variable_spend
        }
