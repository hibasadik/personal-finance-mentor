from agents.state_agent import FinancialStateAgent
from tools.impact_simulator import ImpactSimulator
from typing import Dict, Any

class PurchaseImpactAgent:
    """
    Agent responsible for answering: "Can I buy X?"
    """
    def __init__(self, state_agent: FinancialStateAgent):
        self.state_agent = state_agent
        self.simulator = ImpactSimulator()

    def analyze_purchase(self, item_name: str, cost: float, category: str = "wants") -> Dict[str, Any]:
        """
        Runs the simulation flow.
        """
        # 1. Get Context
        state = self.state_agent.get_todays_state()
        discretionary_income = state["free_cash_flow"] # Simplified for now
        savings_goal = state["savings_goal"]
        
        # 2. Run Deterministic Simulation
        assessment = self.simulator.assess_transaction(
            current_discretionary_balance=discretionary_income,
            current_savings=0.0, # Not tracking actual savings balance yet, simplified
            savings_goal=savings_goal,
            item_cost=cost
        )
        
        # 3. Enhance Report
        assessment["item"] = item_name
        assessment["cost"] = cost
        
        return assessment

    def confirm_purchase(self, item_name: str, cost: float, category: str):
        """
        Commits the purchase to the state.
        """
        self.state_agent.log_transaction(item_name, cost, category)
