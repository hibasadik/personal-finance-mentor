import streamlit as st
from agents.state_agent import FinancialStateAgent
from agents.budget_agent import BudgetPlanningAgent
from agents.purchase_agent import PurchaseImpactAgent
from agents.mentor_agent import MentorReasoningAgent
from agents.reflection_agent import ReflectionAgent
from llm.llm_interface import LLMInterface

# Page Config
st.set_page_config(page_title="Wallet Mom", page_icon="💰", layout="wide")

# --- Initialization ---
@st.cache_resource
def get_agents():
    # Initialize Core
    state_agent = FinancialStateAgent()
    
    # Initialize Logic Agents
    budget_agent = BudgetPlanningAgent(state_agent)
    purchase_agent = PurchaseImpactAgent(state_agent)
    
    # Initialize LLM & Mentor
    llm = LLMInterface()
    mentor_agent = MentorReasoningAgent(llm)
    
    reflection_agent = ReflectionAgent(state_agent)
    
    return state_agent, budget_agent, purchase_agent, mentor_agent, reflection_agent

state_agent, budget_agent, purchase_agent, mentor_agent, reflection_agent = get_agents()

# --- Sidebar: User Profile ---
with st.sidebar:
    st.header("Hiba's Wallet")
    
    current_profile = state_agent.get_profile()
    
    # Simple Onboarding / Settings
    income = st.number_input("Monthly Income (₹)", min_value=0.0, value=float(current_profile.get("monthly_income", 0.0)))
    savings_goal = st.number_input("Total Savings Goal (₹)", min_value=0.0, value=float(current_profile.get("savings_goal", 0.0)))
    
    if st.button("Update Profile"):
        state_agent.update_profile(income, savings_goal)
        st.success("Profile Updated!")
        st.rerun() # Refresh app to reflect changes

    st.divider()
    st.header("📉 Fixed Expenses")
    exp_name = st.text_input("Expense Name (e.g., Rent)")
    exp_amount = st.number_input("Amount (₹)", min_value=0.0)
    
    if st.button("Add Expense"):
        state_agent.add_fixed_expense(exp_name, exp_amount)
        st.success(f"Added {exp_name}!")
        st.rerun()

    st.subheader("Current Fixed Expenses")
    for exp in state_agent.storage.get_fixed_expenses():
        st.write(f"- {exp['name']}: ₹{exp['amount']}")

    st.divider()
    st.subheader("Recent Purchases (Variable)")
    transactions = state_agent.storage.get_transactions()
    if transactions:
        # Show last 5
        for tx in transactions[-5:]:
             st.write(f"- {tx['description']}: ₹{tx['amount']} ({tx['date'][:10]})")
    else:
        st.caption("No purchases logged yet.")

# --- Main Content ---
st.title("Wallet Mom")

# Dashboard
todays_state = state_agent.get_todays_state()
budget_plan = budget_agent.create_budget_plan()

col1, col2, col3 = st.columns(3)
col1.metric("Monthly Income", f"₹{todays_state['income']}")
col1.metric("Fixed Expenses", f"₹{todays_state['total_fixed_expenses']}")
col2.metric("Free Cash Flow", f"₹{todays_state['free_cash_flow']}")

# Visual Budget Plan
if budget_plan["plan_details"].get("status") == "surplus":
    st.info(f"💡 Budget Strategy: {budget_plan['strategy']}")
    rec_savings = budget_plan['plan_details']['recommended_savings']
    rec_wants = budget_plan['plan_details']['recommended_wants']
    
    col3.metric("Rec. Savings", f"₹{rec_savings:.2f}")
    col3.metric("Safe to Spend (Wants)", f"₹{rec_wants:.2f}")
else:
    st.error("⚠️ Warning: Your expenses exceed your income!")

st.divider()

# Purchase Decision Simulator
st.header("🛒 Can I Buy This?")
st.write("Ask your mentor before making a purchase.")

col_buy1, col_buy2 = st.columns([1, 2])

with col_buy1:
    item_name = st.text_input("Item Name")
    item_cost = st.number_input("Cost (₹)", min_value=0.0)
    category = st.selectbox("Category", ["Wants", "Needs", "Unexpected"])
    
    analyze_btn = st.button("Analyze Purchase")

with col_buy2:
    if analyze_btn:
        if item_cost > 0:
            with st.spinner("Simulating impact..."):
                # 1. Run Probability/Math Simulation
                analysis = purchase_agent.analyze_purchase(item_name, item_cost, category)
                
                # 2. Get Reasoning from LLM
                advice = mentor_agent.provide_advice(state_agent.get_profile(), analysis)
                
                # 3. Store in Session State for Confirmation
                st.session_state['current_analysis'] = analysis
                st.session_state['current_advice'] = advice
                st.session_state['analysis_done'] = True
        else:
            st.warning("Please enter a valid cost.")

    # --- Display Result & Confirmation ---
    if st.session_state.get('analysis_done'):
        analysis = st.session_state['current_analysis']
        advice = st.session_state['current_advice']
        
        # Display Status
        if analysis["status"] == "DANGER":
            st.error(f"🚨 RISK ASSESSMENT: {analysis['status']}")
        elif analysis["status"] == "CAUTION":
            st.warning(f"⚠️ RISK ASSESSMENT: {analysis['status']}")
        else:
            st.success(f"✅ RISK ASSESSMENT: {analysis['status']}")
        
        st.markdown(f"**Mentor's Advice:**\n\n{advice}")
        
        st.markdown("---")
        st.subheader("Decision")
        
        col_confirm, col_cancel = st.columns(2)
        
        with col_confirm:
            if st.button("✅ I bought this"):
                purchase_agent.confirm_purchase(analysis['item'], analysis['cost'], category)
                st.success(f"Purchase of {analysis['item']} logged! Budget updated.")
                # Clear state and rerun to show updated Free Cash Flow
                del st.session_state['analysis_done']
                st.rerun()
                
        with col_cancel:
            if st.button("❌ I changed my mind"):
                st.info("Good choice! Money saved.")
                del st.session_state['analysis_done']
                st.rerun()

        st.markdown("**Simulation Data:**")
        st.json(analysis)

st.divider()
st.caption("⚠️ DISCLAIMER: This is an AI educational tool. Not financial advice.")
