# Agentic AI–Powered Personal Finance Mentor

**For First-Time Earners**

## 🧠 Problem Statement
Entering the workforce brings the challenge of managing a salary for the first time. Many beginners struggle with:
- Understanding how much they can actually afford to spend.
- Balancing immediate wants with long-term savings.
- Avoiding the "lifestyle creep" trap.
- Making decisions without understanding the financial aftermath.

This project is **not a chatbot**. It is an **Agentic AI System** designed to be a proactive financial mentor. It maintains your financial state, enforces budgeting rules, and simulates the impact of every purchase before you make it.

## 🏗 Agentic Architecture
This system creates a "Council of Agents" to assist the user. It uses an LLM only for reasoning and explanation, while core financial logic is deterministic and safe.

### The 5-Agent System
1.  **Financial State Agent**: The "Memory". It holds the single source of truth for income, expenses, and transaction history.
2.  **Budget Planning Agent**: The "Strategist". It proactively creates a budget plan (e.g., 50/30/20) based on your income.
3.  **Purchase Impact Agent**: The "Simulator". When you want to buy something, it runs a simulation to see if you can afford it without breaking your budget or savings goals.
4.  **Mentor Reasoning Agent**: The "Voice". It takes the mathematical output from the simulator and explains it in plain English, offering advice and alternatives.
5.  **Reflection Agent**: The "Coach". It reviews historical spending data to surface behavioral patterns and long-term insights (e.g., “You tend to overspend on weekends”).

## ⚠️ ETHICAL & SAFETY DISCLAIMER
> [!WARNING]
> **Educational Use Only**
> This system provides educational financial guidance only.
> - **No Investment Advice**: This system does not recommend stocks, crypto, or assets.
> - **No Legal/Tax Advice**: Consult a professional for tax or legal matters.
> - **No Guarantees**: Financial decisions are ultimately the user's responsibility.

## 🧠 LLM Integration Philosophy

The system is intentionally designed so that:
- All financial calculations and decisions are deterministic and explainable.
- The LLM is used only for reasoning, explanation, and coaching-style feedback.
- If external LLM inference is unavailable (e.g., Hugging Face free-tier limits), the system gracefully falls back to a deterministic mock mode without loss of core functionality.

## 🛠 Setup & Run
### Prerequisites
- Python 3.9+
- Hugging Face Token (Recommended for real LLM reasoning)

### Installation
1. Clone the repository.
2. Navigate to the project directory:
   ```bash
   cd finance-mentor-agent
   ```
3. Install dependencies:
   ```bash
   pip install streamlit
   ```
4. Set your Token (Optional but Recommended):
   ```bash
   # Windows PowerShell
   $env:HF_TOKEN="your-hf-token-here"
   # Linux/Mac
   export HF_TOKEN="your-hf-token-here"
   ```
   *Note: If no token is set, the system runs in **Mock Mode** using deterministic templates.*

### Running the Mentor
```bash
streamlit run app.py
```
