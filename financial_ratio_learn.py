import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Financial Ratio Learning Lab", layout="wide", page_icon="📊")

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-metric {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .green-metric { background-color: #d4edda; color: #155724; }
    .yellow-metric { background-color: #fff3cd; color: #856404; }
    .red-metric { background-color: #f8d7da; color: #721c24; }
    .formula-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
        font-family: monospace;
    }
    .example-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .interpretation-box {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #FFC107;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Financial Ratio Learning Lab")
st.markdown("### Master financial analysis with interactive learning and real-world examples")

# Helper function to format currency
def format_currency(value):
    return f"${value:,.0f}"

# Helper function to get ratio color class
def get_ratio_status(value, ratio_type):
    if ratio_type == "current":
        if value >= 1.5:
            return "green-metric", "✅ Excellent"
        elif value >= 1:
            return "yellow-metric", "⚠️ Acceptable"
        else:
            return "red-metric", "❌ Poor"
    elif ratio_type == "quick":
        if value >= 1:
            return "green-metric", "✅ Good"
        else:
            return "yellow-metric", "⚠️ Caution"
    elif ratio_type == "leverage":
        if value < 1:
            return "green-metric", "✅ Conservative"
        elif value < 2:
            return "yellow-metric", "⚠️ Moderate"
        else:
            return "red-metric", "❌ Aggressive"

# ---------------------------
# Balance Sheet Section
# ---------------------------
st.header("🏦 Balance Sheet")
st.markdown("*The balance sheet shows what a company owns (Assets) and owes (Liabilities), plus owner's investment (Equity)*")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 ASSETS (What the company owns)")
    st.markdown("---")
    
    current_assets = st.number_input(
        "💰 Current Assets",
        value=1000000.0,
        step=10000.0,
        help="Assets that can be converted to cash within one year (cash, accounts receivable, inventory)"
    )
    
    inventory = st.number_input(
        "📦 Inventory (subset of current assets)",
        value=200000.0,
        step=10000.0,
        help="Goods available for sale - less liquid than cash or receivables"
    )
    
    st.markdown("---")
    
    total_assets = st.number_input(
        "🏢 Total Assets",
        value=2000000.0,
        step=10000.0,
        help="All assets: current assets + fixed assets (buildings, equipment, etc.)"
    )

with col2:
    st.markdown("### 📉 LIABILITIES & EQUITY (How assets are financed)")
    st.markdown("---")
    
    current_liabilities = st.number_input(
        "💳 Current Liabilities",
        value=500000.0,
        step=10000.0,
        help="Debts due within one year (accounts payable, short-term loans)"
    )
    
    total_liabilities = st.number_input(
        "🏦 Total Liabilities",
        value=1200000.0,
        step=10000.0,
        help="All debts: short-term + long-term (loans, bonds, mortgages)"
    )
    
    st.markdown("---")
    
    equity = st.number_input(
        "👥 Equity (Owner's Capital)",
        value=800000.0,
        step=10000.0,
        help="Owner's investment + retained earnings"
    )

# Balance Sheet Equation Check
balance_check = abs(total_assets - (total_liabilities + equity))
if balance_check < 1:
    st.success(f"✅ **Balance Sheet Equation:** {format_currency(total_assets)} = {format_currency(total_liabilities)} + {format_currency(equity)} → **BALANCED**")
else:
    st.error(f"⚠️ **Balance Sheet Not Balanced!** Assets = {format_currency(total_assets)}, Liabilities + Equity = {format_currency(total_liabilities + equity)}")

# Display Balance Sheet Table
st.markdown("### 📋 Balance Sheet Summary")
balance_df = pd.DataFrame({
    'ASSETS': [
        'Current Assets',
        '  - Inventory',
        'Total Assets'
    ],
    'Amount': [
        format_currency(current_assets),
        format_currency(inventory),
        format_currency(total_assets)
    ],
    'LIABILITIES & EQUITY': [
        'Current Liabilities',
        'Total Liabilities',
        'Equity'
    ],
    'Amount ': [
        format_currency(current_liabilities),
        format_currency(total_liabilities),
        format_currency(equity)
    ]
})
st.dataframe(balance_df, hide_index=True, use_container_width=True)

st.markdown("---")

# ---------------------------
# P&L Statement Section
# ---------------------------
st.header("💵 Profit & Loss Statement (Income Statement)")
st.markdown("*Shows how much money the company made or lost over a period*")

col1, col2, col3 = st.columns(3)

with col1:
    revenue = st.number_input("📊 Revenue (Sales)", value=1500000.0, step=10000.0, help="Total sales from products/services")
    cogs = st.number_input("📦 COGS (Cost of Goods Sold)", value=800000.0, step=10000.0, help="Direct costs to produce goods")

with col2:
    operating_expenses = st.number_input("💼 Operating Expenses", value=300000.0, step=10000.0, help="Salaries, rent, marketing, etc.")
    interest_expense = st.number_input("💰 Interest Expense", value=50000.0, step=10000.0, help="Interest paid on debt")

with col3:
    tax_expense = st.number_input("🏛️ Tax Expense", value=100000.0, step=10000.0, help="Income taxes paid")
    net_income = st.number_input("✅ Net Income", value=250000.0, step=10000.0, help="Bottom line profit")

# P&L Calculation Display
gross_profit = revenue - cogs
operating_income = gross_profit - operating_expenses

st.markdown("### 📋 P&L Summary")
pnl_df = pd.DataFrame({
    'Item': ['Revenue', 'Less: COGS', 'Gross Profit', 'Less: Operating Expenses', 'Operating Income', 
             'Less: Interest', 'Less: Taxes', 'Net Income'],
    'Amount': [format_currency(revenue), format_currency(cogs), format_currency(gross_profit),
               format_currency(operating_expenses), format_currency(operating_income),
               format_currency(interest_expense), format_currency(tax_expense), format_currency(net_income)]
})
st.dataframe(pnl_df, hide_index=True, use_container_width=True)

st.markdown("---")

# ---------------------------
# Calculate All Ratios
# ---------------------------
current_ratio = current_assets / current_liabilities if current_liabilities > 0 else 0
quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities > 0 else 0
debt_to_equity = total_liabilities / equity if equity > 0 else 0
debt_to_assets = total_liabilities / total_assets if total_assets > 0 else 0
gross_margin = (revenue - cogs) / revenue if revenue > 0 else 0
operating_margin = operating_income / revenue if revenue > 0 else 0
net_margin = net_income / revenue if revenue > 0 else 0
roa = net_income / total_assets if total_assets > 0 else 0
roe = net_income / equity if equity > 0 else 0

# ---------------------------
# Ratio Analysis Tabs
# ---------------------------
st.header("📊 Financial Ratio Analysis")

tab1, tab2, tab3 = st.tabs(["💧 Liquidity Ratios", "⚖️ Leverage Ratios", "💰 Profitability Ratios"])

# ---------------------------
# LIQUIDITY RATIOS TAB
# ---------------------------
with tab1:
    st.markdown("## 💧 Liquidity Ratios")
    st.info("**Purpose:** Measure a company's ability to pay short-term debts and handle unexpected expenses")
    
    # Current Ratio
    st.markdown("### 1️⃣ Current Ratio")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        color_class, status = get_ratio_status(current_ratio, "current")
        st.markdown(f'<div class="big-metric {color_class}">{current_ratio:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f"**Status:** {status}")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("ROE = Net Income ÷ Equity")
        st.markdown(f"**Calculation:** {format_currency(net_income)} ÷ {format_currency(equity)} = **{roe:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**💼 Real-Life Example:**")
    st.markdown("""
    You invest $100,000 of your own money (equity) to start a business. At year-end, the business made $15,000 profit.
    
    **ROE = $15,000 ÷ $100,000 = 15%**
    
    You earned 15% return on your investment. Compare this to:
    - Savings account: ~4% return
    - Stock market average: ~10% return
    - Your business: 15% return ✓
    
    **With Leverage:** If you borrowed $50,000 and only invested $50,000 of your own money (still $100,000 total assets), and made the same $15,000 profit:
    - ROE = $15,000 ÷ $50,000 = **30%** (doubled!)
    
    This shows the power (and risk) of leverage. Same profit, but higher return on YOUR money because you used other people's money (debt) too.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 How to Interpret:**")
    st.markdown(f"""
    - **Your ROE: {roe:.2%}**
    - **> 15%:** Excellent - Strong returns for shareholders
    - **10% - 15%:** Good - Competitive returns
    - **< 10%:** Low - May not be worth the risk vs. safer investments
    
    **Why it matters:** This is THE number shareholders care about most. It tells them: "For every dollar I invested, how much profit did you generate?" Higher ROE attracts investors.
    
    **The Relationship:** ROE is always ≥ ROA when using debt. Debt amplifies returns (and losses).
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Profitability Visualization
    st.markdown("### 📊 Profitability Cascade")
    
    # Waterfall chart showing profit margins
    fig = go.Figure(go.Waterfall(
        name = "Profitability", orientation = "v",
        measure = ["relative", "relative", "relative", "total"],
        x = ["Gross Margin", "Operating Margin", "Net Margin", "Final"],
        y = [gross_margin*100, (operating_margin-gross_margin)*100, (net_margin-operating_margin)*100, net_margin*100],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig.update_layout(title = "Profitability Margins (%)", showlegend = False, height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart for ROA and ROE
    fig2 = go.Figure(data=[
        go.Bar(name='ROA', x=['Return on Assets'], y=[roa*100], marker_color='lightblue'),
        go.Bar(name='ROE', x=['Return on Equity'], y=[roe*100], marker_color='lightgreen')
    ])
    fig2.update_layout(title="Returns Comparison (%)", yaxis_title="Return (%)", showlegend=True, height=400)
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**🎯 Summary of Profitability Ratios:**")
    st.markdown(f"""
    | Ratio | Your Value | What It Tells You |
    |-------|-----------|-------------------|
    | Gross Margin | {gross_margin:.1%} | {gross_margin*100:.1f}% left after making/buying products |
    | Operating Margin | {operating_margin:.1%} | {operating_margin*100:.1f}% left after running the business |
    | Net Margin | {net_margin:.1%} | {net_margin*100:.1f}% final profit per dollar of sales |
    | ROA | {roa:.1%} | ${roa*100:.1f} profit per $100 of assets |
    | ROE | {roe:.1%} | ${roe*100:.1f} profit per $100 invested by owners |
    
    **Key Insight:** Compare these ratios to competitors in your industry. A 5% net margin might be excellent for a grocery store but terrible for a software company!
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# Summary Dashboard
# ---------------------------
st.markdown("---")
st.header("📈 Complete Financial Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💧 Liquidity")
    st.metric("Current Ratio", f"{current_ratio:.2f}", 
              delta="Healthy" if current_ratio >= 1.5 else "Acceptable" if current_ratio >= 1 else "Warning",
              delta_color="normal" if current_ratio >= 1 else "inverse")
    st.metric("Quick Ratio", f"{quick_ratio:.2f}",
              delta="Good" if quick_ratio >= 1 else "Low",
              delta_color="normal" if quick_ratio >= 1 else "inverse")

with col2:
    st.markdown("### ⚖️ Leverage")
    st.metric("Debt/Equity", f"{debt_to_equity:.2f}",
              delta="Conservative" if debt_to_equity < 1 else "Moderate" if debt_to_equity < 2 else "High")
    st.metric("Debt/Assets", f"{debt_to_assets:.1%}",
              delta=f"{(1-debt_to_assets)*100:.0f}% owned")

with col3:
    st.markdown("### 💰 Profitability")
    st.metric("Net Margin", f"{net_margin:.1%}",
              delta=f"${net_margin*revenue:,.0f} profit")
    st.metric("ROE", f"{roe:.1%}",
              delta="Shareholder return")

# Quick Health Check
st.markdown("### 🏥 Financial Health Check")

health_score = 0
health_messages = []

if current_ratio >= 1.5:
    health_score += 25
    health_messages.append("✅ Strong liquidity position")
elif current_ratio >= 1:
    health_score += 15
    health_messages.append("⚠️ Adequate liquidity")
else:
    health_messages.append("❌ Liquidity concerns")

if debt_to_equity < 1:
    health_score += 25
    health_messages.append("✅ Conservative debt levels")
elif debt_to_equity < 2:
    health_score += 15
    health_messages.append("⚠️ Moderate debt levels")
else:
    health_messages.append("❌ High debt risk")

if net_margin > 0.1:
    health_score += 25
    health_messages.append("✅ Healthy profit margins")
elif net_margin > 0:
    health_score += 15
    health_messages.append("⚠️ Thin profit margins")
else:
    health_messages.append("❌ Operating at a loss")

if roe > 0.15:
    health_score += 25
    health_messages.append("✅ Excellent returns for shareholders")
elif roe > 0.10:
    health_score += 15
    health_messages.append("⚠️ Moderate returns for shareholders")
else:
    health_messages.append("❌ Poor shareholder returns")

st.progress(health_score / 100)
st.markdown(f"**Overall Health Score: {health_score}/100**")
for msg in health_messages:
    st.markdown(msg)

st.markdown("---")
st.markdown("### 💡 Pro Tip")
st.info("""
**Remember the Context:** Financial ratios don't exist in a vacuum!
- Compare against **industry benchmarks** (retail vs. tech vs. manufacturing have very different "normal" ratios)
- Track **trends over time** (is your liquidity improving or declining?)
- Consider **business lifecycle** (startups often have negative profitability while growing, mature companies should be profitable)
- Read **the full story** (great ratios with declining sales might hide problems, "poor" ratios might be strategic investments)

**Use this tool to:** Experiment with different scenarios, understand trade-offs (debt vs. equity), and build financial intuition!
""")formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Current Ratio = Current Assets ÷ Current Liabilities")
        st.markdown(f"**Calculation:** {format_currency(current_assets)} ÷ {format_currency(current_liabilities)} = **{current_ratio:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🏪 Real-Life Example:**")
    st.markdown("""
    Imagine you run a coffee shop. You have $10,000 in the bank and $5,000 worth of coffee beans (current assets = $15,000). 
    You owe $10,000 to suppliers due next month (current liabilities).
    
    **Current Ratio = $15,000 ÷ $10,000 = 1.5**
    
    This means for every $1 you owe short-term, you have $1.50 available to pay it. This is healthy!
    
    If your ratio was 0.8, you'd only have $0.80 for every $1 owed - that's a problem because you might not be able to pay your bills.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 How to Interpret:**")
    st.markdown(f"""
    - **Your Ratio: {current_ratio:.2f}**
    - **≥ 1.5:** Excellent - You have plenty of cushion to pay short-term debts
    - **1.0 - 1.5:** Acceptable - You can cover debts but with less margin
    - **< 1.0:** Warning - You may struggle to pay short-term obligations
    
    **Why it matters:** Banks and suppliers look at this to decide if you're creditworthy. Too low = risky, too high might mean you're not using assets efficiently.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Ratio
    st.markdown("### 2️⃣ Quick Ratio (Acid Test)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        color_class, status = get_ratio_status(quick_ratio, "quick")
        st.markdown(f'<div class="big-metric {color_class}">{quick_ratio:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f"**Status:** {status}")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Quick Ratio = (Current Assets - Inventory) ÷ Current Liabilities")
        st.markdown(f"**Calculation:** ({format_currency(current_assets)} - {format_currency(inventory)}) ÷ {format_currency(current_liabilities)} = **{quick_ratio:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🏪 Real-Life Example:**")
    st.markdown("""
    Using the same coffee shop: You have $15,000 in current assets, but $5,000 is tied up in coffee beans (inventory). 
    If you needed to pay all your debts TODAY, you couldn't instantly sell all your beans.
    
    **Quick Ratio = ($15,000 - $5,000) ÷ $10,000 = 1.0**
    
    You have exactly $10,000 in "liquid" assets (cash and receivables) to pay $10,000 in debts. This is the bare minimum.
    
    **Why exclude inventory?** Inventory takes time to sell. In an emergency, you need cash NOW, not coffee beans you still need to sell.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 How to Interpret:**")
    st.markdown(f"""
    - **Your Ratio: {quick_ratio:.2f}**
    - **≥ 1.0:** Good - You can pay immediate obligations without selling inventory
    - **< 1.0:** Caution - You'd need to sell inventory quickly to meet obligations
    
    **Why it matters:** This is a tougher test than current ratio. It shows if you can survive a cash crunch without having to liquidate inventory at fire-sale prices.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualization
    st.markdown("### 📊 Liquidity Ratios Visualization")
    fig = go.Figure(data=[
        go.Bar(name='Current Ratio', x=['Current Ratio'], y=[current_ratio], 
               marker_color='lightgreen' if current_ratio >= 1.5 else 'orange' if current_ratio >= 1 else 'red'),
        go.Bar(name='Quick Ratio', x=['Quick Ratio'], y=[quick_ratio],
               marker_color='lightgreen' if quick_ratio >= 1 else 'orange')
    ])
    fig.add_hline(y=1.5, line_dash="dash", line_color="green", annotation_text="Optimal Current Ratio (1.5)")
    fig.add_hline(y=1.0, line_dash="dash", line_color="orange", annotation_text="Minimum Safe Level (1.0)")
    fig.update_layout(title="Liquidity Ratios Comparison", yaxis_title="Ratio Value", showlegend=False, height=400)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# LEVERAGE RATIOS TAB
# ---------------------------
with tab2:
    st.markdown("## ⚖️ Leverage Ratios")
    st.info("**Purpose:** Measure how much debt a company uses and its ability to meet long-term obligations")
    
    # Debt to Equity
    st.markdown("### 1️⃣ Debt to Equity Ratio")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        color_class, status = get_ratio_status(debt_to_equity, "leverage")
        st.markdown(f'<div class="big-metric {color_class}">{debt_to_equity:.2f}</div>', unsafe_allow_html=True)
        st.markdown(f"**Status:** {status}")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Debt to Equity = Total Liabilities ÷ Equity")
        st.markdown(f"**Calculation:** {format_currency(total_liabilities)} ÷ {format_currency(equity)} = **{debt_to_equity:.2f}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🏠 Real-Life Example:**")
    st.markdown("""
    Think of buying a house worth $500,000:
    
    **Scenario A (Conservative):** You put down $300,000 (equity) and borrow $200,000 (debt)
    - Debt to Equity = $200,000 ÷ $300,000 = **0.67**
    
    **Scenario B (Aggressive):** You put down $100,000 (equity) and borrow $400,000 (debt)
    - Debt to Equity = $400,000 ÷ $100,000 = **4.0**
    
    In Scenario A, you're using less debt relative to your own money - safer but slower growth.
    In Scenario B, you're heavily leveraged - riskier (higher mortgage payments) but you keep more cash for other investments.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 How to Interpret:**")
    st.markdown(f"""
    - **Your Ratio: {debt_to_equity:.2f}**
    - **< 1.0:** Conservative - You use less debt than equity (safer)
    - **1.0 - 2.0:** Moderate - Balanced mix of debt and equity
    - **> 2.0:** Aggressive - Heavy reliance on debt (riskier, but can amplify returns)
    
    **Why it matters:** High debt means high interest payments. If business slows down, you still must pay creditors. But debt can also help you grow faster. It's about finding the right balance for your industry and risk tolerance.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Debt to Assets
    st.markdown("### 2️⃣ Debt to Assets Ratio")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric yellow-metric">{debt_to_assets:.2%}</div>', unsafe_allow_html=True)
        st.markdown(f"**{debt_to_assets:.1%} of assets are financed by debt**")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Debt to Assets = Total Liabilities ÷ Total Assets")
        st.markdown(f"**Calculation:** {format_currency(total_liabilities)} ÷ {format_currency(total_assets)} = **{debt_to_assets:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🚗 Real-Life Example:**")
    st.markdown("""
    You start a delivery business. You buy 10 vans for $200,000 total:
    
    **Option A:** Pay $200,000 cash (100% equity financed)
    - Debt to Assets = $0 ÷ $200,000 = **0%**
    
    **Option B:** Pay $50,000 down, finance $150,000 (75% debt financed)
    - Debt to Assets = $150,000 ÷ $200,000 = **75%**
    
    Option A is safer (no debt risk) but ties up all your cash.
    Option B preserves cash for operations but requires regular loan payments regardless of how business is doing.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="interpretation-box">', unsafe_allow_html=True)
    st.markdown("**📖 How to Interpret:**")
    st.markdown(f"""
    - **Your Ratio: {debt_to_assets:.2%}**
    - **< 30%:** Very safe - Most assets are owned outright
    - **30% - 60%:** Moderate - Balanced financing
    - **> 60%:** High leverage - Most assets are financed by debt
    
    **Why it matters:** Shows what percentage of your assets would need to be sold to pay off all debts. Lower is safer. If you have 70% debt-to-assets and asset values drop, you could be underwater (owe more than you own).
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualization
    st.markdown("### 📊 Capital Structure Visualization")
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'pie'}, {'type':'bar'}]])
    
    fig.add_trace(go.Pie(labels=['Debt', 'Equity'], values=[total_liabilities, equity],
                         marker_colors=['#ff7f0e', '#2ca02c']), row=1, col=1)
    
    fig.add_trace(go.Bar(x=['Debt to Equity', 'Debt to Assets'], 
                         y=[debt_to_equity, debt_to_assets],
                         marker_color=['orange', 'lightcoral']), row=1, col=2)
    
    fig.update_layout(title="Company Capital Structure", showlegend=True, height=400)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# PROFITABILITY RATIOS TAB
# ---------------------------
with tab3:
    st.markdown("## 💰 Profitability Ratios")
    st.info("**Purpose:** Measure how efficiently a company generates profit from sales and investments")
    
    # Gross Profit Margin
    st.markdown("### 1️⃣ Gross Profit Margin")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric green-metric">{gross_margin:.2%}</div>', unsafe_allow_html=True)
        st.markdown("**Profit after direct costs**")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Gross Margin = (Revenue - COGS) ÷ Revenue")
        st.markdown(f"**Calculation:** ({format_currency(revenue)} - {format_currency(cogs)}) ÷ {format_currency(revenue)} = **{gross_margin:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🍕 Real-Life Example:**")
    st.markdown("""
    You run a pizza shop. You sell a pizza for $20 (revenue). The ingredients and labor to make it cost $8 (COGS).
    
    **Gross Margin = ($20 - $8) ÷ $20 = 60%**
    
    This means for every $20 pizza sold, you keep $12 (60%) to cover rent, marketing, utilities, and profit. The other $8 (40%) went to make the pizza.
    
    **Why it matters:** If your gross margin is too low, you won't have enough left over to pay other expenses. A 20% gross margin means you only have $4 from that $20 pizza to pay for EVERYTHING else - probably not sustainable.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Operating Margin
    st.markdown("### 2️⃣ Operating Margin")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric green-metric">{operating_margin:.2%}</div>', unsafe_allow_html=True)
        st.markdown("**Profit from core operations**")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Operating Margin = Operating Income ÷ Revenue")
        st.markdown(f"**Calculation:** {format_currency(operating_income)} ÷ {format_currency(revenue)} = **{operating_margin:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🍕 Real-Life Example (continued):**")
    st.markdown("""
    After making $12 gross profit per pizza, you still have to pay:
    - Rent: $3 per pizza
    - Wages for cashier: $2 per pizza
    - Marketing: $1 per pizza
    - Utilities: $1 per pizza
    **Total Operating Expenses = $7 per pizza**
    
    **Operating Income = $12 - $7 = $5 per pizza**
    **Operating Margin = $5 ÷ $20 = 25%**
    
    Now you're down to $5 (25%) from that $20 pizza, BEFORE paying interest on loans or taxes.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Net Profit Margin
    st.markdown("### 3️⃣ Net Profit Margin")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric green-metric">{net_margin:.2%}</div>', unsafe_allow_html=True)
        st.markdown("**The bottom line**")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("Net Margin = Net Income ÷ Revenue")
        st.markdown(f"**Calculation:** {format_currency(net_income)} ÷ {format_currency(revenue)} = **{net_margin:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🍕 Real-Life Example (final):**")
    st.markdown("""
    From the $5 operating income, you still pay:
    - Interest on business loan: $1.50
    - Income taxes: $1.00
    
    **Net Income = $5 - $1.50 - $1.00 = $2.50 per pizza**
    **Net Margin = $2.50 ÷ $20 = 12.5%**
    
    Out of every $20 pizza, you finally keep $2.50 as actual profit. This is what you can reinvest in the business or take home.
    
    **The Cascade:** Revenue (100%) → Gross Profit (60%) → Operating Income (25%) → Net Income (12.5%)
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ROA
    st.markdown("### 4️⃣ Return on Assets (ROA)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric green-metric">{roa:.2%}</div>', unsafe_allow_html=True)
        st.markdown("**Profit per dollar of assets**")
    
    with col2:
        st.markdown('<div class="formula-box">', unsafe_allow_html=True)
        st.markdown("**Formula:**")
        st.code("ROA = Net Income ÷ Total Assets")
        st.markdown(f"**Calculation:** {format_currency(net_income)} ÷ {format_currency(total_assets)} = **{roa:.2%}**")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="example-box">', unsafe_allow_html=True)
    st.markdown("**🏭 Real-Life Example:**")
    st.markdown("""
    **Company A (Capital Intensive):** Manufacturing plant with $10 million in equipment makes $500,000 profit
    - ROA = $500,000 ÷ $10,000,000 = **5%**
    
    **Company B (Asset Light):** Software company with $1 million in assets makes $200,000 profit
    - ROA = $200,000 ÷ $1,000,000 = **20%**
    
    Company B generates more profit per dollar of assets - more efficient use of resources. This is why tech companies often have higher ROAs than manufacturing.
    
    **Why it matters:** Shows how well management uses assets to generate profit. Higher ROA = more efficient business model.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ROE
    st.markdown("### 5️⃣ Return on Equity (ROE)")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f'<div class="big-metric green-metric">{roe:.2%}</div>', unsafe_allow_html=True)
        st.markdown("**Return to shareholders**")
    
    with col2:
        st.markdown('<div class="
