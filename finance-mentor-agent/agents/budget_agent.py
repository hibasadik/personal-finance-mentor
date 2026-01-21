from agents.state_agent import FinancialStateAgent
from tools.budget_calculator import BudgetCalculator
from typing import Dict, Any

class BudgetPlanningAgent:
    """
    Agent responsible for generating a budget plan.
    Triggers: When user profile is updated or app opens.
    """
    def __init__(self, state_agent: FinancialStateAgent):
        self.state_agent = state_agent
        self.calculator = BudgetCalculator()

    def create_budget_plan(self) -> Dict[str, Any]:
        """
        Fetches state and calculates the optimal budget.
        """
        state = self.state_agent.get_todays_state()
        income = state["income"]
        fixed_expenses = state["total_fixed_expenses"]

        # Strategy: Strict Needs First
        plan = self.calculator.calculate_remaining_after_fixed(income, fixed_expenses)
        
        # Save plan to memory (via generic storage for now, or just return)
        #Ideally state_agent would have a set_plan method, ignoring for simplicity
        
        return {
            "income": income,
            "fixed_expenses": fixed_expenses,
            "plan_details": plan,
            "strategy": "Needs-First Allocation"
        }
