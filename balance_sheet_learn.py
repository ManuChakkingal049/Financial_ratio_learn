import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Balance Sheet Learning Lab", layout="wide")

st.title("📒 Balance Sheet Learning Lab")
st.markdown(
    """
Learn the **structure and components of a balance sheet** interactively.
Adjust numbers and see how total assets, liabilities, and equity relate.
"""
)

# ---------------------------
# Assets Section
# ---------------------------
st.header("🟢 Assets")
st.subheader("Current Assets")
cash = st.number_input("Cash & Cash Equivalents", value=200000.0, step=1000.0, help="Cash or assets that can be quickly converted to cash")
accounts_receivable = st.number_input("Accounts Receivable", value=150000.0, step=1000.0, help="Money owed by customers")
inventory = st.number_input("Inventory", value=100000.0, step=1000.0, help="Goods ready for sale")

st.subheader("Non-Current Assets")
ppe = st.number_input("Property, Plant & Equipment (PPE)", value=500000.0, step=1000.0, help="Long-term tangible assets")
intangible_assets = st.number_input("Intangible Assets", value=50000.0, step=1000.0, help="Patents, trademarks, goodwill, etc.")

total_assets = cash + accounts_receivable + inventory + ppe + intangible_assets
st.metric("Total Assets", f"{total_assets:,.0f}", delta_color="normal")

# ---------------------------
# Liabilities Section
# ---------------------------
st.header("🔴 Liabilities")
st.subheader("Current Liabilities")
accounts_payable = st.number_input("Accounts Payable", value=80000.0, step=1000.0, help="Money owed to suppliers")
short_term_debt = st.number_input("Short-term Debt", value=70000.0, step=1000.0, help="Debt due within one year")

st.subheader("Non-Current Liabilities")
long_term_debt = st.number_input("Long-term Debt", value=300000.0, step=1000.0, help="Debt due after one year")

total_liabilities = accounts_payable + short_term_debt + long_term_debt
st.metric("Total Liabilities", f"{total_liabilities:,.0f}", delta_color="inverse")

# ---------------------------
# Equity Section
# ---------------------------
st.header("🟡 Equity")
share_capital = st.number_input("Share Capital", value=300000.0, step=1000.0, help="Capital invested by owners")
retained_earnings = st.number_input("Retained Earnings", value=150000.0, step=1000.0, help="Profits kept in the business")

total_equity = share_capital + retained_earnings
st.metric("Total Equity", f"{total_equity:,.0f}", delta_color="normal")

# ---------------------------
# Balance Check
# ---------------------------
st.header("⚖️ Balance Sheet Check")
liabilities_plus_equity = total_liabilities + total_equity
balance_check = total_assets - liabilities_plus_equity

if balance_check == 0:
    st.success("✅ Balanced! Total Assets = Total Liabilities + Equity")
else:
    st.error(f"⚠️ Not Balanced! Difference = {balance_check:,.0f}")

# ---------------------------
# Visualization
# ---------------------------
st.header("📊 Balance Sheet Visualization")
fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Assets"],
    y=[total_assets],
    name="Assets",
    marker_color="green"
))
fig.add_trace(go.Bar(
    x=["Liabilities + Equity"],
    y=[liabilities_plus_equity],
    name="Liabilities + Equity",
    marker_color="orange"
))

fig.update_layout(
    barmode='group',
    title="Balance Sheet Overview",
    yaxis_title="Amount",
)
st.plotly_chart(fig)

# ---------------------------
# Scenario Simulation Sliders
# ---------------------------
st.header("🔄 Scenario Simulation")
st.write("Experiment with numbers and see how the balance sheet changes:")

cash_sim = st.slider("Cash & Cash Equivalents", 0, int(total_assets*2), int(cash))
accounts_receivable_sim = st.slider("Accounts Receivable", 0, int(total_assets*2), int(accounts_receivable))
inventory_sim = st.slider("Inventory", 0, int(total_assets*2), int(inventory))
ppe_sim = st.slider("PPE", 0, int(total_assets*2), int(ppe))
intangible_sim = st.slider("Intangible Assets", 0, int(total_assets*2), int(intangible_assets))

accounts_payable_sim = st.slider("Accounts Payable", 0, int(total_liabilities*2), int(accounts_payable))
short_term_debt_sim = st.slider("Short-term Debt", 0, int(total_liabilities*2), int(short_term_debt))
long_term_debt_sim = st.slider("Long-term Debt", 0, int(total_liabilities*2), int(long_term_debt))

share_capital_sim = st.slider("Share Capital", 0, int(total_equity*2), int(share_capital))
retained_earnings_sim = st.slider("Retained Earnings", 0, int(total_equity*2), int(retained_earnings))

# Recalculate totals for simulation
total_assets_sim = cash_sim + accounts_receivable_sim + inventory_sim + ppe_sim + intangible_sim
total_liabilities_sim = accounts_payable_sim + short_term_debt_sim + long_term_debt_sim
total_equity_sim = share_capital_sim + retained_earnings_sim
liabilities_plus_equity_sim = total_liabilities_sim + total_equity_sim
balance_check_sim = total_assets_sim - liabilities_plus_equity_sim

st.subheader("Simulation Results")
st.metric("Total Assets", f"{total_assets_sim:,.0f}")
st.metric("Total Liabilities + Equity", f"{liabilities_plus_equity_sim:,.0f}")

if balance_check_sim == 0:
    st.success("✅ Balanced!")
else:
    st.error(f"⚠️ Not Balanced! Difference = {balance_check_sim:,.0f}")

# Update visualization dynamically
fig_sim = go.Figure()
fig_sim.add_trace(go.Bar(
    x=["Assets"],
    y=[total_assets_sim],
    name="Assets",
    marker_color="green"
))
fig_sim.add_trace(go.Bar(
    x=["Liabilities + Equity"],
    y=[liabilities_plus_equity_sim],
    name="Liabilities + Equity",
    marker_color="orange"
))
fig_sim.update_layout(barmode='group', title="Balance Sheet Simulation", yaxis_title="Amount")
st.plotly_chart(fig_sim)
