from typing import Dict

class BudgetCalculator:
    """
    Pure logic class for calculating budget splits.
    Default strategy: 50% Needs, 30% Wants, 20% Savings.
    """
    
    @staticmethod
    def calculate_50_30_20(income: float) -> Dict[str, float]:
        """
        Returns a dictionary with allocations.
        """
        return {
            "needs": income * 0.50,
            "wants": income * 0.30,
            "savings": income * 0.20
        }

    @staticmethod
    def calculate_remaining_after_fixed(income: float, fixed_expenses_total: float) -> Dict[str, float]:
        """
        More realistic approach:
        Income - Fixed Expenses = Discretionary Income.
        Then split Discretionary into Savings/Wants.
        """
        discretionary = income - fixed_expenses_total
        if discretionary < 0:
            return {
                "status": "deficit",
                "discretionary": 0.0,
                "needs_gap": abs(discretionary)
            }
        
        # Suggest split of discretionary
        return {
            "status": "surplus",
            "needs_total": fixed_expenses_total,
            "discretionary_total": discretionary,
            "recommended_savings": discretionary * 0.40, # Save 40% of what's left
            "recommended_wants": discretionary * 0.60
        }
