import json
import os
from typing import Dict, List, Any, Optional

class StorageEngine:
    """
    Handles persistent storage for the Finance Mentor Agent using a simple JSON file.
    Acts as the 'Memory' for the Financial State Agent.
    """
    def __init__(self, db_path: str = "finance_data.json"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Creates the JSON structure if it doesn't exist."""
        if not os.path.exists(self.db_path):
            initial_data = {
                "user_profile": {
                    "monthly_income": 0.0,
                    "savings_goal": 0.0,
                    "currency": "₹"
                },
                "fixed_expenses": [], # List of {name, amount}
                "transactions": [],   # List of {date, description, amount, category, type}
                "budget_plan": {},    # Store the calculated budget
            }
            self._save_data(initial_data)

    def _load_data(self) -> Dict[str, Any]:
        """Reads data from the JSON file."""
        with open(self.db_path, 'r') as f:
            return json.load(f)

    def _save_data(self, data: Dict[str, Any]):
        """Writes data to the JSON file."""
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=4)

    # --- CRUD Operations ---

    def update_user_profile(self, income: float, savings_goal: float):
        data = self._load_data()
        data["user_profile"]["monthly_income"] = income
        data["user_profile"]["savings_goal"] = savings_goal
        self._save_data(data)

    def get_user_profile(self) -> Dict[str, Any]:
        return self._load_data().get("user_profile", {})

    def add_fixed_expense(self, name: str, amount: float):
        data = self._load_data()
        # Remove if exists to avoid duplicates
        data["fixed_expenses"] = [e for e in data["fixed_expenses"] if e["name"] != name]
        data["fixed_expenses"].append({"name": name, "amount": amount})
        self._save_data(data)

    def get_fixed_expenses(self) -> List[Dict[str, Any]]:
        return self._load_data().get("fixed_expenses", [])

    def log_transaction(self, transaction: Dict[str, Any]):
        """
        Logs a transaction (Expense or Income).
        tx format: {date, description, amount, category, type="expense"|"income"}
        """
        data = self._load_data()
        data["transactions"].append(transaction)
        self._save_data(data)

    def get_transactions(self) -> List[Dict[str, Any]]:
        return self._load_data().get("transactions", [])
        
    def save_budget_plan(self, plan: Dict[str, Any]):
        data = self._load_data()
        data["budget_plan"] = plan
        self._save_data(data)
        
    def get_budget_plan(self) -> Dict[str, Any]:
        return self._load_data().get("budget_plan", {})
