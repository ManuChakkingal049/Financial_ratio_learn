import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Ratio Learning Lab", layout="wide")

st.title("📊 Financial Ratio Learning Lab")
st.markdown(
    "Learn and explore **Liquidity**, **Leverage**, and **Profitability Ratios** interactively from Balance Sheet and P&L data."
)

# ---------------------------
# Input Section: Balance Sheet
# ---------------------------
st.header("🧾 Balance Sheet Inputs")
with st.expander("Assets"):
    current_assets = st.number_input("Current Assets", value=1000000.0, step=1000.0, help="Short-term assets like cash, receivables, inventory.")
    inventory = st.number_input("Inventory", value=200000.0, step=1000.0, help="Part of current assets that can’t be quickly converted to cash.")
    total_assets = st.number_input("Total Assets", value=2000000.0, step=1000.0, help="Sum of all assets (current + non-current).")

with st.expander("Liabilities & Equity"):
    current_liabilities = st.number_input("Current Liabilities", value=500000.0, step=1000.0, help="Obligations due within one year.")
    total_liabilities = st.number_input("Total Liabilities", value=1200000.0, step=1000.0, help="All debts including short-term and long-term.")
    equity = st.number_input("Equity", value=800000.0, step=1000.0, help="Owner's capital in the business.")

# ---------------------------
# Input Section: P&L
# ---------------------------
st.header("💵 P&L Statement Inputs")
with st.expander("Revenue & Expenses"):
    revenue = st.number_input("Revenue", value=1500000.0, step=1000.0)
    cogs = st.number_input("COGS (Cost of Goods Sold)", value=800000.0, step=1000.0)
    operating_expenses = st.number_input("Operating Expenses", value=300000.0, step=1000.0)
    interest_expense = st.number_input("Interest Expense", value=50000.0, step=1000.0)
    tax_expense = st.number_input("Tax Expense", value=100000.0, step=1000.0)
    net_income = st.number_input("Net Income", value=250000.0, step=1000.0)

# ---------------------------
# Tabs for Ratios
# ---------------------------
tabs = st.tabs(["Liquidity Ratios", "Leverage Ratios", "Profitability Ratios"])

# ---------------------------
# Liquidity Ratios
# ---------------------------
with tabs[0]:
    st.subheader("💧 Liquidity Ratios")
    current_ratio = current_assets / current_liabilities
    quick_ratio = (current_assets - inventory) / current_liabilities

    def color_ratio(val, optimal=1.5):
        if val >= optimal:
            return "🟢"
        elif val >= 1:
            return "🟡"
        else:
            return "🔴"

    st.metric("Current Ratio", f"{current_ratio:.2f}", delta=f"{color_ratio(current_ratio)} Optimal >1.5")
    st.metric("Quick Ratio", f"{quick_ratio:.2f}", delta=f"{color_ratio(quick_ratio,1):.0s} Optimal >1")

    st.plotly_chart(
        go.Figure(
            go.Bar(
                x=["Current Ratio", "Quick Ratio"],
                y=[current_ratio, quick_ratio],
                marker_color=["green" if current_ratio>=1.5 else "red","green" if quick_ratio>=1 else "red"]
            )
        )
    )

    st.expander("Learn More: Liquidity Ratios").write(
        """
        - **Current Ratio**: Ability to pay short-term obligations. Optimal >1.5
        - **Quick Ratio**: Ability to pay short-term obligations excluding inventory. Optimal >1
        """
    )

# ---------------------------
# Leverage Ratios
# ---------------------------
with tabs[1]:
    st.subheader("⚖️ Leverage Ratios")
    debt_to_equity = total_liabilities / equity
    debt_to_assets = total_liabilities / total_assets

    st.metric("Debt to Equity", f"{debt_to_equity:.2f}", delta="Lower is safer")
    st.metric("Debt to Assets", f"{debt_to_assets:.2f}", delta="Lower is safer")

    st.plotly_chart(
        go.Figure(
            go.Bar(
                x=["Debt/Equity", "Debt/Assets"],
                y=[debt_to_equity, debt_to_assets],
                marker_color=["orange","orange"]
            )
        )
    )

    st.expander("Learn More: Leverage Ratios").write(
        """
        - **Debt/Equity**: How much debt the company uses relative to equity. High → riskier
        - **Debt/Assets**: % of assets funded by debt. Lower → safer
        """
    )

# ---------------------------
# Profitability Ratios
# ---------------------------
with tabs[2]:
    st.subheader("💰 Profitability Ratios")
    gross_margin = (revenue - cogs) / revenue
    operating_margin = (revenue - cogs - operating_expenses) / revenue
    net_margin = net_income / revenue
    roa = net_income / total_assets
    roe = net_income / equity

    st.metric("Gross Profit Margin", f"{gross_margin:.2f}", delta="Higher is better")
    st.metric("Operating Margin", f"{operating_margin:.2f}", delta="Higher is better")
    st.metric("Net Profit Margin", f"{net_margin:.2f}", delta="Higher is better")
    st.metric("Return on Assets (ROA)", f"{roa:.2f}", delta="Higher is better")
    st.metric("Return on Equity (ROE)", f"{roe:.2f}", delta="Higher is better")

    st.plotly_chart(
        go.Figure(
            go.Bar(
                x=["Gross Margin","Operating Margin","Net Margin","ROA","ROE"],
                y=[gross_margin,operating_margin,net_margin,roa,roe],
                marker_color="blue"
            )
        )
    )

    st.expander("Learn More: Profitability Ratios").write(
        """
        - **Gross Margin**: Profitability after COGS  
        - **Operating Margin**: Profitability after operating expenses  
        - **Net Margin**: Profitability after all expenses and taxes  
        - **ROA**: How efficiently assets generate profit  
        - **ROE**: How efficiently equity generates profit
        """
    )

# ---------------------------
# Scenario Simulation
# ---------------------------
st.header("🔄 Scenario Simulation")
st.write("Adjust inputs to see how ratios change dynamically.")
st.slider("Increase / Decrease Current Assets", 0, int(current_assets*2), int(current_assets), key="sim_assets")
st.slider("Increase / Decrease Liabilities", 0, int(total_liabilities*2), int(total_liabilities), key="sim_liabilities")
st.slider("Increase / Decrease Net Income", 0, int(net_income*2), int(net_income), key="sim_netincome")
st.write("Ratios update in real time above!")

