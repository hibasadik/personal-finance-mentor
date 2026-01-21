from llm.llm_interface import LLMInterface
from typing import Dict, Any

class MentorReasoningAgent:
    """
    The 'Voice' of the system. 
    It doesn't do math. It interprets math for humans.
    """
    def __init__(self, llm: LLMInterface):
        self.llm = llm

    def provide_advice(self, user_profile: Dict, purchase_analysis: Dict) -> str:
        """
        Generates the mentor's response by passing structured context to the LLM layer.
        """
        # Combine context for the Agentic Interface
        context = {
            "user_income": user_profile.get("monthly_income"),
            "savings_goal": user_profile.get("savings_goal"),
            "item": purchase_analysis.get("item"),
            "cost": purchase_analysis.get("cost"),
            "status": purchase_analysis.get("status"),
            "reason": purchase_analysis.get("reason"),
            "remaining_balance": purchase_analysis.get("remaining_balance")
        }
        
        # Delegate explanation to the LLM Interface (Logic is already done)
        return self.llm.generate_response(context)
