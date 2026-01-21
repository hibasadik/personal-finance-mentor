from agents.state_agent import FinancialStateAgent
from typing import List

class ReflectionAgent:
    """
    Agent responsible for looking back at history to find patterns.
    """
    def __init__(self, state_agent: FinancialStateAgent):
        self.state_agent = state_agent

    def generate_monthly_review(self) -> str:
        """
        Simple reflection logic (Stub for now).
        """
        transactions = self.state_agent.storage.get_transactions()
        if not transactions:
            return "No transaction history to review yet."
        
        # Logic to find spending patterns would go here
        count = len(transactions)
        return f"I notice you have logged {count} transactions. Keep tracking to get better insights!"
