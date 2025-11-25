import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

st.set_page_config(page_title="Balance Sheet Learning Lab", layout="wide", page_icon="📊")

# Custom CSS
st.markdown("""
    <style>
    .big-number {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .asset-box { background-color: #d4edda; color: #155724; border: 3px solid #28a745; }
    .liability-box { background-color: #f8d7da; color: #721c24; border: 3px solid #dc3545; }
    .equity-box { background-color: #fff3cd; color: #856404; border: 3px solid #ffc107; }
    .info-box {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 10px 0;
    }
    .tip-box {
        background-color: #fff9e6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 20px;
        border-radius: 10px;
        border: 3px solid #28a745;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for game mode
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'game_score' not in st.session_state:
    st.session_state.game_score = 0
if 'challenges_completed' not in st.session_state:
    st.session_state.challenges_completed = 0

def format_currency(value):
    return f"${value:,.0f}"

def check_balance(assets, liabilities, equity):
    return abs(assets - (liabilities + equity)) < 1

def get_balance_tips(assets, liabilities, equity):
    difference = assets - (liabilities + equity)
    tips = []
    
    if difference > 0:
        tips.append(f"💡 **Assets are ${abs(difference):,.0f} higher** than Liabilities + Equity")
        tips.append("✅ **To balance, you can:**")
        tips.append(f"   • Add ${abs(difference):,.0f} to Liabilities (take a loan)")
        tips.append(f"   • Add ${abs(difference):,.0f} to Equity (invest more capital)")
        tips.append(f"   • Reduce Assets by ${abs(difference):,.0f} (pay down cash, sell equipment)")
        tips.append("   • Or use a combination of the above!")
    elif difference < 0:
        tips.append(f"💡 **Liabilities + Equity are ${abs(difference):,.0f} higher** than Assets")
        tips.append("✅ **To balance, you can:**")
        tips.append(f"   • Add ${abs(difference):,.0f} to Assets (buy equipment, increase inventory)")
        tips.append(f"   • Reduce Liabilities by ${abs(difference):,.0f} (pay off debt)")
        tips.append(f"   • Reduce Equity by ${abs(difference):,.0f} (pay dividends to owners)")
        tips.append("   • Or use a combination of the above!")
    
    return tips

# Title and Introduction
st.title("📊 Interactive Balance Sheet Learning Lab")
st.markdown("### Learn balance sheet fundamentals through interactive games and real-world scenarios!")

# Mode Selection
st.markdown("---")
mode = st.radio("**Choose Your Learning Mode:**", 
                ["📚 Learn Mode - Explore Freely", 
                 "🎮 Challenge Mode - Fix the Balance Sheet!",
                 "🏢 Real-World Scenarios"],
                horizontal=True)

st.markdown("---")

# ---------------------------
# LEARN MODE
# ---------------------------
if "Learn Mode" in mode:
    st.header("📚 Learn Mode: Understanding Balance Sheet Components")
    
    st.markdown("""
    <div class="info-box">
    <b>🎯 The Golden Rule of Balance Sheets:</b><br>
    <b>ASSETS = LIABILITIES + EQUITY</b><br><br>
    Think of it like this: Everything a company owns (assets) is financed either by borrowing money (liabilities) or by owner's investment (equity).
    </div>
    """, unsafe_allow_html=True)
    
    # Create three columns for the balance sheet
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🟢 ASSETS")
        st.markdown("*What the company OWNS*")
        st.markdown("---")
        
        with st.expander("💵 Current Assets (Short-term)", expanded=True):
            st.markdown("**Assets that can be converted to cash within 1 year**")
            cash = st.number_input("Cash & Cash Equivalents", value=200000.0, step=5000.0, 
                                   help="💰 Example: Money in bank accounts, short-term investments")
            st.caption("Real-life: Like having $200k in your business checking account")
            
            accounts_receivable = st.number_input("Accounts Receivable", value=150000.0, step=5000.0,
                                                  help="🧾 Example: Customer invoices not yet paid")
            st.caption("Real-life: You delivered $150k worth of pizzas to restaurants, they'll pay you in 30 days")
            
            inventory = st.number_input("Inventory", value=100000.0, step=5000.0,
                                       help="📦 Example: Products ready to sell")
            st.caption("Real-life: $100k worth of coffee beans sitting in your warehouse")
        
        with st.expander("🏢 Non-Current Assets (Long-term)"):
            st.markdown("**Assets used for more than 1 year**")
            ppe = st.number_input("Property, Plant & Equipment", value=500000.0, step=10000.0,
                                 help="🏭 Example: Buildings, machines, vehicles")
            st.caption("Real-life: Your pizza ovens, delivery trucks, restaurant building")
            
            intangible_assets = st.number_input("Intangible Assets", value=50000.0, step=5000.0,
                                               help="💡 Example: Patents, trademarks, brand value")
            st.caption("Real-life: Your trademarked restaurant name and secret sauce recipe")
    
    with col2:
        st.markdown("### 🔴 LIABILITIES")
        st.markdown("*What the company OWES*")
        st.markdown("---")
        
        with st.expander("⏰ Current Liabilities (Short-term)", expanded=True):
            st.markdown("**Debts due within 1 year**")
            accounts_payable = st.number_input("Accounts Payable", value=80000.0, step=5000.0,
                                              help="🧾 Example: Bills you need to pay suppliers")
            st.caption("Real-life: You owe $80k to your flour and cheese suppliers")
            
            short_term_debt = st.number_input("Short-term Debt", value=70000.0, step=5000.0,
                                             help="💳 Example: Loans due this year, credit card debt")
            st.caption("Real-life: A $70k business loan you need to repay in 6 months")
        
        with st.expander("📅 Non-Current Liabilities (Long-term)"):
            st.markdown("**Debts due after 1 year**")
            long_term_debt = st.number_input("Long-term Debt", value=300000.0, step=10000.0,
                                            help="🏦 Example: Mortgages, bonds, long-term loans")
            st.caption("Real-life: A $300k mortgage on your restaurant building, paying over 15 years")
    
    with col3:
        st.markdown("### 🟡 EQUITY")
        st.markdown("*Owner's stake in company*")
        st.markdown("---")
        
        with st.expander("👥 Shareholders' Equity", expanded=True):
            st.markdown("**Money invested by owners + accumulated profits**")
            share_capital = st.number_input("Share Capital", value=300000.0, step=10000.0,
                                           help="💰 Example: Money owners invested to start the business")
            st.caption("Real-life: You invested $300k of your own savings to open the restaurant")
            
            retained_earnings = st.number_input("Retained Earnings", value=150000.0, step=5000.0,
                                               help="📈 Example: Profits kept in the business (not paid out)")
            st.caption("Real-life: You made $150k profit over the years and reinvested it instead of taking it home")
    
    # Calculate totals
    total_assets = cash + accounts_receivable + inventory + ppe + intangible_assets
    total_liabilities = accounts_payable + short_term_debt + long_term_debt
    total_equity = share_capital + retained_earnings
    
    # Display totals prominently
    st.markdown("---")
    st.markdown("## 📊 Balance Sheet Totals")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="big-number asset-box">Assets<br>{format_currency(total_assets)}</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="big-number liability-box">Liabilities<br>{format_currency(total_liabilities)}</div>', 
                   unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="big-number equity-box">Equity<br>{format_currency(total_equity)}</div>', 
                   unsafe_allow_html=True)
    
    # Balance Check
    st.markdown("---")
    st.markdown("## ⚖️ Balance Check")
    
    liabilities_plus_equity = total_liabilities + total_equity
    is_balanced = check_balance(total_assets, total_liabilities, total_equity)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Total Assets", format_currency(total_assets), delta_color="off")
    
    with col2:
        st.markdown("<h3 style='text-align: center;'>=</h3>", unsafe_allow_html=True)
    
    with col3:
        st.metric("Liabilities + Equity", format_currency(liabilities_plus_equity), 
                 delta=format_currency(liabilities_plus_equity - total_assets), 
                 delta_color="inverse" if not is_balanced else "off")
    
    if is_balanced:
        st.markdown('<div class="success-box">✅ BALANCED! Perfect! Assets = Liabilities + Equity</div>', 
                   unsafe_allow_html=True)
        st.balloons()
    else:
        st.error(f"⚠️ NOT BALANCED! Difference: {format_currency(abs(total_assets - liabilities_plus_equity))}")
        
        # Show helpful tips
        st.markdown('<div class="tip-box">', unsafe_allow_html=True)
        st.markdown("### 🎓 How to Balance Your Balance Sheet:")
        tips = get_balance_tips(total_assets, total_liabilities, total_equity)
        for tip in tips:
            st.markdown(tip)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Visualization
    st.markdown("---")
    st.markdown("## 📈 Visual Breakdown")
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Assets Composition", "Liabilities + Equity Composition"),
        specs=[[{"type": "pie"}, {"type": "pie"}]]
    )
    
    # Assets pie chart
    fig.add_trace(go.Pie(
        labels=["Cash", "Receivables", "Inventory", "PPE", "Intangibles"],
        values=[cash, accounts_receivable, inventory, ppe, intangible_assets],
        marker_colors=['#90EE90', '#98FB98', '#00FA9A', '#3CB371', '#2E8B57'],
        hole=0.3
    ), row=1, col=1)
    
    # Liabilities + Equity pie chart
    fig.add_trace(go.Pie(
        labels=["Accounts Payable", "Short-term Debt", "Long-term Debt", "Share Capital", "Retained Earnings"],
        values=[accounts_payable, short_term_debt, long_term_debt, share_capital, retained_earnings],
        marker_colors=['#FFB6C1', '#FF69B4', '#FF1493', '#FFD700', '#FFA500'],
        hole=0.3
    ), row=1, col=2)
    
    fig.update_layout(height=400, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
    # Bar chart comparison
    fig2 = go.Figure(data=[
        go.Bar(name='Assets', x=['Balance Sheet'], y=[total_assets], marker_color='#28a745'),
        go.Bar(name='Liabilities', x=['Balance Sheet'], y=[total_liabilities], marker_color='#dc3545'),
        go.Bar(name='Equity', x=['Balance Sheet'], y=[total_equity], marker_color='#ffc107')
    ])
    fig2.update_layout(barmode='group', title='Assets vs Liabilities vs Equity', height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# CHALLENGE MODE
# ---------------------------
elif "Challenge Mode" in mode:
    st.header("🎮 Challenge Mode: Fix the Balance Sheet!")
    
    st.markdown("""
    <div class="info-box">
    <b>🎯 Your Mission:</b> Companies have submitted unbalanced balance sheets! 
    Your job is to fix them by adjusting the right accounts. Each successful fix earns you points!
    </div>
    """, unsafe_allow_html=True)
    
    # Challenge selection
    challenge = st.selectbox("Select a Challenge:", [
        "Challenge 1: The Missing Equipment 🏭",
        "Challenge 2: The Forgotten Loan 💰",
        "Challenge 3: The Equity Mystery 👥",
        "Challenge 4: The Cash Crisis 💵",
        "Challenge 5: Random Challenge 🎲"
    ])
    
    if st.button("🎮 Start Challenge!", type="primary"):
        st.session_state.game_mode = challenge
    
    if st.session_state.game_mode:
        st.markdown("---")
        
        # Define challenges
        if "Challenge 1" in st.session_state.game_mode:
            st.markdown("### 🏭 Challenge 1: The Missing Equipment")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> A manufacturing company bought new machinery worth $100,000 but forgot to record it! 
            The balance sheet shows they paid cash for it, but the equipment isn't listed in assets.
            
            <b>Your task:</b> Add the equipment to fix the balance!
            </div>
            """, unsafe_allow_html=True)
            
            # Pre-filled values (unbalanced)
            cash_c = st.number_input("Cash", value=100000.0, step=5000.0, key="c1_cash")
            inventory_c = st.number_input("Inventory", value=200000.0, step=5000.0, key="c1_inv")
            ppe_c = st.number_input("⭐ Equipment (Fix this!)", value=0.0, step=5000.0, key="c1_ppe", 
                                   help="Hint: They bought $100k worth of equipment!")
            
            liabilities_c = st.number_input("Total Liabilities", value=100000.0, step=5000.0, key="c1_liab")
            equity_c = st.number_input("Total Equity", value=200000.0, step=5000.0, key="c1_eq")
            
            total_assets_c = cash_c + inventory_c + ppe_c
            total_liab_eq_c = liabilities_c + equity_c
            
            if check_balance(total_assets_c, liabilities_c, equity_c):
                st.success("🎉 CHALLENGE COMPLETE! You fixed the balance sheet!")
                st.balloons()
                st.markdown("**Explanation:** The company spent $100k cash on equipment. Assets stayed the same (cash went down $100k, equipment went up $100k), so the balance sheet stays balanced!")
            else:
                st.warning(f"Not quite! Difference: {format_currency(abs(total_assets_c - total_liab_eq_c))}")
                st.info("💡 Hint: The equipment costs $100,000. What should you add to the Equipment line?")
        
        elif "Challenge 2" in st.session_state.game_mode:
            st.markdown("### 💰 Challenge 2: The Forgotten Loan")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> A retail store took out a $150,000 bank loan to buy inventory, 
            but the accountant forgot to record the loan on the balance sheet!
            
            <b>Your task:</b> Add the missing loan to balance the books!
            </div>
            """, unsafe_allow_html=True)
            
            cash_c = st.number_input("Cash", value=100000.0, step=5000.0, key="c2_cash")
            inventory_c = st.number_input("Inventory", value=400000.0, step=5000.0, key="c2_inv", 
                                         help="This includes the $150k worth they bought with the loan")
            
            liabilities_c = st.number_input("⭐ Total Liabilities (Fix this!)", value=200000.0, step=5000.0, key="c2_liab",
                                           help="Hint: They took a $150k loan!")
            equity_c = st.number_input("Total Equity", value=300000.0, step=5000.0, key="c2_eq")
            
            total_assets_c = cash_c + inventory_c
            total_liab_eq_c = liabilities_c + equity_c
            
            if check_balance(total_assets_c, liabilities_c, equity_c):
                st.success("🎉 CHALLENGE COMPLETE! You found the missing loan!")
                st.balloons()
                st.markdown("**Explanation:** The loan increased inventory (asset) by $150k AND increased liabilities by $150k. Both sides go up equally, keeping it balanced!")
            else:
                st.warning(f"Not quite! Difference: {format_currency(abs(total_assets_c - total_liab_eq_c))}")
                st.info("💡 Hint: They borrowed $150,000. This should be added to liabilities!")
        
        elif "Challenge 3" in st.session_state.game_mode:
            st.markdown("### 👥 Challenge 3: The Equity Mystery")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> The owner invested an additional $80,000 into the business, 
            which was deposited as cash, but the equity wasn't updated!
            
            <b>Your task:</b> Update the equity to reflect the new investment!
            </div>
            """, unsafe_allow_html=True)
            
            cash_c = st.number_input("Cash", value=280000.0, step=5000.0, key="c3_cash",
                                    help="This includes the $80k investment")
            inventory_c = st.number_input("Inventory", value=120000.0, step=5000.0, key="c3_inv")
            
            liabilities_c = st.number_input("Total Liabilities", value=150000.0, step=5000.0, key="c3_liab")
            equity_c = st.number_input("⭐ Total Equity (Fix this!)", value=170000.0, step=5000.0, key="c3_eq",
                                      help="Hint: The owner added $80k to their investment!")
            
            total_assets_c = cash_c + inventory_c
            total_liab_eq_c = liabilities_c + equity_c
            
            if check_balance(total_assets_c, liabilities_c, equity_c):
                st.success("🎉 CHALLENGE COMPLETE! The equity is now correct!")
                st.balloons()
                st.markdown("**Explanation:** When the owner invests money, cash (asset) goes up by $80k AND equity goes up by $80k. The owner now has a bigger stake in the business!")
            else:
                st.warning(f"Not quite! Difference: {format_currency(abs(total_assets_c - total_liab_eq_c))}")
                st.info("💡 Hint: The original equity was $170k. The owner added $80k. What's the new equity?")
        
        elif "Challenge 4" in st.session_state.game_mode:
            st.markdown("### 💵 Challenge 4: The Cash Crisis")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> A company paid off $60,000 of their debt using cash, 
            but only updated the liabilities side - they forgot to reduce cash!
            
            <b>Your task:</b> Reduce the cash to reflect the payment!
            </div>
            """, unsafe_allow_html=True)
            
            cash_c = st.number_input("⭐ Cash (Fix this!)", value=250000.0, step=5000.0, key="c4_cash",
                                    help="Hint: They paid $60k in cash to reduce debt!")
            inventory_c = st.number_input("Inventory", value=150000.0, step=5000.0, key="c4_inv")
            
            liabilities_c = st.number_input("Total Liabilities", value=140000.0, step=5000.0, key="c4_liab",
                                           help="Already reduced by $60k")
            equity_c = st.number_input("Total Equity", value=200000.0, step=5000.0, key="c4_eq")
            
            total_assets_c = cash_c + inventory_c
            total_liab_eq_c = liabilities_c + equity_c
            
            if check_balance(total_assets_c, liabilities_c, equity_c):
                st.success("🎉 CHALLENGE COMPLETE! Cash is now correctly recorded!")
                st.balloons()
                st.markdown("**Explanation:** Paying off debt reduces cash (asset) by $60k AND reduces liabilities by $60k. Both sides decrease equally!")
            else:
                st.warning(f"Not quite! Difference: {format_currency(abs(total_assets_c - total_liab_eq_c))}")
                st.info("💡 Hint: They paid $60,000 in cash. The original cash was $250k. What should it be now?")

        # Show current balance status
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Assets", format_currency(total_assets_c))
        with col2:
            st.markdown("<h3 style='text-align: center;'>=</h3>", unsafe_allow_html=True)
        with col3:
            st.metric("Liabilities + Equity", format_currency(total_liab_eq_c))

# ---------------------------
# REAL-WORLD SCENARIOS
# ---------------------------
elif "Real-World" in mode:
    st.header("🏢 Real-World Business Scenarios")
    
    st.markdown("""
    <div class="info-box">
    <b>Learn how real business transactions affect the balance sheet!</b><br>
    See how common business activities change assets, liabilities, and equity.
    </div>
    """, unsafe_allow_html=True)
    
    scenario = st.selectbox("Choose a Business Scenario:", [
        "🍕 Opening a Pizza Restaurant",
        "🚗 Starting a Delivery Service",
        "💻 Launching a Tech Startup",
        "🏪 Opening a Retail Store"
    ])
    
    if "Pizza Restaurant" in scenario:
        st.markdown("### 🍕 Opening a Pizza Restaurant: Step-by-Step")
        
        step = st.slider("Follow the journey:", 1, 6, 1)
        
        # Initialize values
        cash = 0
        equipment = 0
        inventory = 0
        debt = 0
        equity = 0
        receivables = 0
        
        if step >= 1:
            st.markdown("#### Step 1: Initial Investment")
            st.info("You invest $200,000 of your own money to start the business")
            cash += 200000
            equity += 200000
            st.success("✅ Cash +$200k (Asset) | Equity +$200k")
        
        if step >= 2:
            st.markdown("#### Step 2: Buy Equipment")
            st.info("You buy pizza ovens and kitchen equipment for $100,000 cash")
            cash -= 100000
            equipment += 100000
            st.success("✅ Cash -$100k, Equipment +$100k (Assets) | No change on other side")
        
        if step >= 3:
            st.markdown("#### Step 3: Take Out a Loan")
            st.info("You take a $150,000 bank loan to have more working capital")
            cash += 150000
            debt += 150000
            st.success("✅ Cash +$150k (Asset) | Debt +$150k (Liability)")
        
        if step >= 4:
            st.markdown("#### Step 4: Buy Inventory")
            st.info("You buy $50,000 worth of ingredients (flour, cheese, sauce, etc.)")
            cash -= 50000
            inventory += 50000
            st.success("✅ Cash -$50k, Inventory +$50k (Assets) | No change on other side")
        
        if step >= 5:
            st.markdown("#### Step 5: Make Sales on Credit")
            st.info("You cater a big event for $30,000, they'll pay you next month")
            receivables += 30000
            equity += 30000  # This is revenue, increases retained earnings
            st.success("✅ Receivables +$30k (Asset) | Equity +$30k (profit increases equity)")
        
        if step >= 6:
            st.markdown("#### Step 6: Pay Off Some Debt")
            st.info("Business is good! You pay off $50,000 of the loan")
            cash -= 50000
            debt -= 50000
            st.success("✅ Cash -$50k (Asset) | Debt -$50k (Liability)")
        
        # Show current balance sheet
        st.markdown("---")
        st.markdown("### 📊 Current Balance Sheet")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ASSETS")
            st.write(f"Cash: {format_currency(cash)}")
            st.write(f"Equipment: {format_currency(equipment)}")
            st.write(f"Inventory: {format_currency(inventory)}")
            st.write(f"Receivables: {format_currency(receivables)}")
            st.markdown(f"**Total Assets: {format_currency(cash + equipment + inventory + receivables)}**")
        
        with col2:
            st.markdown("#### LIABILITIES + EQUITY")
            st.write(f"Debt: {format_currency(debt)}")
            st.write(f"Equity: {format_currency(equity)}")
            st.markdown(f"**Total L+E: {format_currency(debt + equity)}**")
        
        if check_balance(cash + equipment + inventory + receivables, debt, equity):
            st.success("✅ Balance Sheet is BALANCED!")
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(name='Assets', x=['Cash', 'Equipment', 'Inventory', 'Receivables'], 
                   y=[cash, equipment, inventory, receivables], marker_color='lightgreen'),
            go.Bar(name='Liabilities', x=['Debt'], y=[debt], marker_color='lightcoral'),
            go.Bar(name='Equity', x=['Equity'], y=[equity], marker_color='lightyellow')
        ])
        fig.update_layout(title='Balance Sheet Breakdown', barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True)

# Educational Footer
st.markdown("---")
st.markdown("""
### 📚 Key Takeaways:
1. **Assets = Liabilities + Equity** - This ALWAYS must be true!
2. **Every transaction affects at least 2 accounts** - That's why it's called "double-entry" bookkeeping
3. **Transactions can affect one side or both sides** - But the equation always stays balanced
4. **Cash is king** - But assets include much more than just cash
5. **Equity grows with profits** - When you make money, retained earnings (part of equity) increases

**Practice Makes Perfect!** Try different scenarios and see how the balance sheet changes. Understanding this is crucial for analyzing any business!
""")
