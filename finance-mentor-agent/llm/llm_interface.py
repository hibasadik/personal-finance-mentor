import os
import json
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """
    Abstract Base Class for LLM Providers.
    Ensures all providers (Mock, Hugging Face, OpenAI) adhere to the same contract.
    The system is Agentic: it creates the context, the LLM only explains it.
    """
    @abstractmethod
    def generate_response(self, context: Dict[str, Any]) -> str:
        pass

class MockLLMProvider(LLMProvider):
    """
    Deterministic Mock Provider.
    Used by default if no API tokens are found.
    Generates 'Safety' focused explanations based strictly on the input context.
    Does NOT call any external API.
    """
    def generate_response(self, context: Dict[str, Any]) -> str:
        # Extract structured data
        item_name = context.get('item', 'Item')
        cost = context.get('cost', 0.0)
        status = context.get('status', 'UNKNOWN')
        reason = context.get('reason', 'No reason provided.')
        remaining = context.get('remaining_balance', 0.0)
        
        # Deterministic Templates based on Risk Status
        if status == "DANGER":
            return (
                f"🚫 **Mentor Advice**: I strongly advise against buying the **{item_name}** (₹{cost}).\n\n"
                f"**Why?** {reason}\n"
                f"Buying this would leave you with only ₹{remaining:.2f}, which is financially dangerous."
                "\n\n**Recommendation**: Wait until next month or look for a cheaper alternative."
            )
        elif status == "CAUTION":
            return (
                f"⚠️ **Mentor Advice**: Proceed with caution regarding the **{item_name}** (₹{cost}).\n\n"
                f"**Why?** {reason}\n"
                f"You can afford it, but it might stretch your budget. You will have ₹{remaining:.2f} left."
                "\n\n**Recommendation**: If this is a 'Want', maybe sleep on it for 24 hours."
            )
        elif status == "SAFE":
            return (
                f"✅ **Mentor Advice**: This purchase of **{item_name}** (₹{cost}) is within your budget.\n\n"
                f"**Analysis**: {reason}\n"
                f"You will still have ₹{remaining:.2f} available."
                "\n\n**Recommendation**: Enjoy your purchase guilt-free!"
            )
        else:
            return "I cannot assess this purchase without a valid risk status."

class HuggingFaceProvider(LLMProvider):
    """
    Provider for Hugging Face Inference API.
    Model: Qwen/Qwen2.5-0.5B-Instruct
    
    Why this model?
    - Qwen2.5-0.5B is a lightweight, highly efficient model.
    - Optimized for instruction following with very low latency.
    - Great for rapid prototyping and runs easily on free inference tiers.
    
    Role:
    - This provider acts ONLY as an explanation layer.
    - It receives strict mathematical context from agents.
    - It does not calculate; it articulates.
    """
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.api_url = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-0.5B-Instruct"

    def generate_response(self, context: Dict[str, Any]) -> str:
        """
        Calls the HF Inference API with a structured prompt.
        """
        system_instruction = (
            "You are a helpful, strict, but kind financial mentor for a beginner. "
            "You receive a structured risk assessment from a deterministic calculation engine. "
            "Your job is to explain this assessment to the user in natural language. "
            "Do NOT second-guess the math. "
            "If status is DANGER, be firm. "
            "If status is CAUTION, be careful. "
            "If status is SAFE, be encouraging. "
            "Keep it concise. Use Indian Rupee (₹) for currency."
        )
        
        # Flatten context for the prompt
        user_prompt = (
            f"Purchase Risk Assessment:\n"
            f"- Item: {context.get('item')}\n"
            f"- Cost: ₹{context.get('cost')}\n"
            f"- Risk Status: {context.get('status')}\n"
            f"- Math Reason: {context.get('reason')}\n"
            f"- Remaining Balance: ₹{context.get('remaining_balance')}\n\n"
            "Explain this to the user as a mentor."
        )
        
        # Qwen-2.5 Instruct Format: ChatML
        # <|im_start|>system\n{system}\n<|im_end|>\n<|im_start|>user\n{user}\n<|im_end|>\n<|im_start|>assistant\n
        full_prompt = (
            f"<|im_start|>system\n{system_instruction}<|im_end|>\n"
            f"<|im_start|>user\n{user_prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        payload = {
            "inputs": full_prompt,
            "parameters": {
                "max_new_tokens": 250,
                "temperature": 0.7,
                "return_full_text": False
            }
        }

        try:
            req = urllib.request.Request(self.api_url)
            req.add_header('Authorization', f'Bearer {self.api_token}')
            req.add_header('Content-Type', 'application/json')
            
            data = json.dumps(payload).encode('utf-8')
            
            with urllib.request.urlopen(req, data=data) as response:
                result = json.load(response)
                # HF Inference API returns a list of dicts, usually [{"generated_text": "..."}]
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
                elif isinstance(result, dict) and "error" in result:
                    return f"HF API Error: {result['error']}"
                else:
                    return "Error: Unexpected response format from Hugging Face."
                    
        except urllib.error.HTTPError as e:
            return f"Error calling Hugging Face API: {e.code} {e.reason}"
        except Exception as e:
            return f"Error: {str(e)}"

class OpenAIProvider(LLMProvider):
    """
    [LEGACY] Optional Adapter for OpenAI.
    Preserved for backward compatibility.
    To use this, you must manually instantiate this provider in the code.
    Automatic selection has been disabled to prioritize Free/Open-Source models.
    """
    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate_response(self, context: Dict[str, Any]) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            system_prompt = "You are a helpful, strict, but kind financial mentor."
            user_message = f"Context: {context}. Give advice."

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

class LLMInterface:
    """
    Facade for the AI Layer.
    Automatically selects the best available provider in this order:
    1. Hugging Face (via HF_TOKEN) - Primary External Option
    2. Mock (Default) - Deterministic Fallback
    
    Note: OpenAI is no longer automatically selected to ensure free-tier compatibility.
    """
    def __init__(self):
        # Load environment variables from .env if present
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass # python-dotenv might not be installed, purely optional
        
        self._provider = self._select_provider()

    def _select_provider(self) -> LLMProvider:
        """
        Logic to determine which provider to use.
        """
        # Priority 1: Hugging Face (Qwen2.5-0.5B)
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            print("LLM Interface: Using Hugging Face Provider (Qwen2.5-0.5B)")
            return HuggingFaceProvider(hf_token)
            
        # Priority 2: Mock Provider (Default)
        # Note: We intentionally do NOT auto-select OpenAI even if a key is present,
        # to strictly enforce the 'Free/Open' agentic design pattern by default.
        print("LLM Interface: Using Mock Provider (Default - Safe & Deterministic)")
        return MockLLMProvider()

    def generate_response(self, context: Dict[str, Any]) -> str:
        """
        The unified entry point for getting mentor advice.
        Accepts structured data, returns a string explanation.
        """
        return self._provider.generate_response(context)
