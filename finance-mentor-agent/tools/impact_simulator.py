from typing import Dict, Any

class ImpactSimulator:
    """
    Deterministic engine that simulates "What happens if I buy this?".
    """
    
    @staticmethod
    def assess_transaction(
        current_discretionary_balance: float, 
        current_savings: float,
        savings_goal: float,
        item_cost: float
    ) -> Dict[str, Any]:
        """
        Returns a structured risk assessment.
        Status: SAFE | CAUTION | DANGER
        """
        remaining_balance = current_discretionary_balance - item_cost
        
        # Rule 1: Can we even afford it?
        if remaining_balance < 0:
            return {
                "status": "DANGER",
                "reason": "Insufficient funds. This purchase puts you in debt.",
                "remaining_balance": remaining_balance,
                "impact_on_savings": "N/A"
            }
        
        # Rule 2: Does it eat into savings?
        # Assuming current_discretionary_balance already excludes "Must Save" amounts.
        # But if the user is dipping into savings...
        
        risk_level = "SAFE"
        advice = "You have enough budget for this."
        
        # Heuristic: If this purchase takes up > 50% of remaining free cash
        if item_cost > (current_discretionary_balance * 0.5):
            risk_level = "CAUTION"
            advice = "This uses more than 50% of your remaining monthly 'fun money'."

        return {
            "status": risk_level,
            "reason": advice,
            "remaining_balance": remaining_balance,
            "cost_percentage_of_free_cash": (item_cost / current_discretionary_balance) * 100
        }
