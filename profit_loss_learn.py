import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

st.set_page_config(page_title="P&L Learning Lab", layout="wide", page_icon="💰")

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
    .profit-box { background-color: #d4edda; color: #155724; border: 3px solid #28a745; }
    .loss-box { background-color: #f8d7da; color: #721c24; border: 3px solid #dc3545; }
    .revenue-box { background-color: #cfe2ff; color: #084298; border: 3px solid #0d6efd; }
    .expense-box { background-color: #fff3cd; color: #856404; border: 3px solid #ffc107; }
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
    .warning-box {
        background-color: #fff3cd;
        padding: 20px;
        border-radius: 10px;
        border: 3px solid #ffc107;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'game_mode' not in st.session_state:
    st.session_state.game_mode = None
if 'game_score' not in st.session_state:
    st.session_state.game_score = 0

def format_currency(value):
    return f"${value:,.0f}"

def calculate_margins(revenue, cogs, opex, interest, tax):
    gross_profit = revenue - cogs
    operating_profit = gross_profit - opex
    ebt = operating_profit - interest
    net_income = ebt - tax
    
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
    operating_margin = (operating_profit / revenue * 100) if revenue > 0 else 0
    net_margin = (net_income / revenue * 100) if revenue > 0 else 0
    
    return gross_profit, operating_profit, ebt, net_income, gross_margin, operating_margin, net_margin

# Title and Introduction
st.title("💰 Interactive P&L Statement Learning Lab")
st.markdown("### Master Profit & Loss statements through games, challenges, and real-world scenarios!")

# Mode Selection
st.markdown("---")
mode = st.radio("**Choose Your Learning Mode:**", 
                ["📚 Learn Mode - Build Your P&L", 
                 "🎮 Challenge Mode - Run a Business!",
                 "🏢 Real-World Scenarios"],
                horizontal=True)

st.markdown("---")

# ---------------------------
# LEARN MODE
# ---------------------------
if "Learn Mode" in mode:
    st.header("📚 Learn Mode: Understanding P&L Components")
    
    st.markdown("""
    <div class="info-box">
    <b>🎯 What is a P&L Statement?</b><br>
    The Profit & Loss (Income Statement) shows if your business made or lost money during a period.<br><br>
    <b>Simple Formula: REVENUE - ALL EXPENSES = NET INCOME (Profit or Loss)</b><br><br>
    Think of it like your personal monthly budget: Money coming in (salary) minus money going out (rent, food, bills) = what you have left over!
    </div>
    """, unsafe_allow_html=True)
    
    # Revenue Section
    st.markdown("## 💵 REVENUE (Money Coming In)")
    st.markdown("*All the money your business earns from selling products or services*")
    
    with st.expander("💰 Revenue Streams", expanded=True):
        product_sales = st.number_input("Product Sales", value=500000.0, step=10000.0,
                                        help="💡 Money from selling products")
        st.caption("🍕 Real-life: You sold 25,000 pizzas at $20 each = $500,000")
        
        service_revenue = st.number_input("Service Revenue", value=200000.0, step=10000.0,
                                         help="💡 Money from providing services")
        st.caption("🚚 Real-life: Delivery fees, catering services = $200,000")
        
        other_income = st.number_input("Other Income", value=50000.0, step=5000.0,
                                      help="💡 Interest, investment income, etc.")
        st.caption("💰 Real-life: Interest from business savings account = $50,000")
    
    total_revenue = product_sales + service_revenue + other_income
    st.markdown(f'<div class="big-number revenue-box">Total Revenue<br>{format_currency(total_revenue)}</div>', 
               unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Cost of Goods Sold
    st.markdown("## 📦 COST OF GOODS SOLD (COGS)")
    st.markdown("*Direct costs to make or buy the products you sell*")
    
    with st.expander("🏭 Direct Costs", expanded=True):
        raw_materials = st.number_input("Raw Materials", value=150000.0, step=5000.0,
                                       help="💡 Ingredients, parts, materials")
        st.caption("🍕 Real-life: Flour, cheese, tomatoes, pepperoni = $150,000")
        
        direct_labor = st.number_input("Direct Labor", value=100000.0, step=5000.0,
                                      help="💡 Wages for workers who make the product")
        st.caption("👨‍🍳 Real-life: Pizza chef salaries = $100,000")
        
        packaging = st.number_input("Packaging & Shipping", value=50000.0, step=5000.0,
                                   help="💡 Boxes, delivery costs")
        st.caption("📦 Real-life: Pizza boxes, delivery gas = $50,000")
    
    total_cogs = raw_materials + direct_labor + packaging
    st.markdown(f'<div class="big-number expense-box">Total COGS<br>{format_currency(total_cogs)}</div>', 
               unsafe_allow_html=True)
    
    # Calculate Gross Profit
    gross_profit = total_revenue - total_cogs
    gross_margin = (gross_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    st.markdown("### 📊 Gross Profit")
    st.markdown(f"**Formula:** Revenue - COGS = Gross Profit")
    st.markdown(f"**{format_currency(total_revenue)} - {format_currency(total_cogs)} = {format_currency(gross_profit)}**")
    
    if gross_profit > 0:
        st.markdown(f'<div class="big-number profit-box">Gross Profit: {format_currency(gross_profit)}<br>Margin: {gross_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.success(f"✅ Great! You have {format_currency(gross_profit)} left to cover operating expenses and make profit!")
    else:
        st.markdown(f'<div class="big-number loss-box">Gross Loss: {format_currency(gross_profit)}<br>Margin: {gross_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.error("⚠️ Warning! Your direct costs are higher than your revenue. You're losing money on each sale!")
    
    st.markdown("---")
    
    # Operating Expenses
    st.markdown("## 💼 OPERATING EXPENSES (OpEx)")
    st.markdown("*Costs to run the business that aren't directly tied to making products*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("👥 Selling & Marketing", expanded=True):
            marketing = st.number_input("Marketing & Advertising", value=50000.0, step=5000.0,
                                       help="💡 Ads, promotions, social media")
            st.caption("📱 Real-life: Facebook ads, flyers, billboards = $50,000")
            
            sales_salaries = st.number_input("Sales Salaries", value=80000.0, step=5000.0,
                                            help="💡 Sales team wages")
            st.caption("💼 Real-life: Commission for sales staff = $80,000")
    
    with col2:
        with st.expander("🏢 General & Administrative", expanded=True):
            rent = st.number_input("Rent & Utilities", value=60000.0, step=5000.0,
                                  help="💡 Store/office rent, electricity, water")
            st.caption("🏪 Real-life: Restaurant rent + utilities = $60,000")
            
            admin_salaries = st.number_input("Admin Salaries", value=70000.0, step=5000.0,
                                            help="💡 Management, accounting, HR")
            st.caption("👔 Real-life: Manager and accountant salaries = $70,000")
            
            other_opex = st.number_input("Other Operating Expenses", value=40000.0, step=5000.0,
                                        help="💡 Insurance, software, supplies")
            st.caption("📄 Real-life: Insurance, POS system, cleaning supplies = $40,000")
    
    total_opex = marketing + sales_salaries + rent + admin_salaries + other_opex
    st.markdown(f'<div class="big-number expense-box">Total Operating Expenses<br>{format_currency(total_opex)}</div>', 
               unsafe_allow_html=True)
    
    # Calculate Operating Profit
    operating_profit = gross_profit - total_opex
    operating_margin = (operating_profit / total_revenue * 100) if total_revenue > 0 else 0
    
    st.markdown("### 📊 Operating Profit (EBIT)")
    st.markdown(f"**Formula:** Gross Profit - Operating Expenses = Operating Profit")
    st.markdown(f"**{format_currency(gross_profit)} - {format_currency(total_opex)} = {format_currency(operating_profit)}**")
    
    if operating_profit > 0:
        st.markdown(f'<div class="big-number profit-box">Operating Profit: {format_currency(operating_profit)}<br>Margin: {operating_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.success(f"✅ Excellent! Your core business operations are profitable!")
    else:
        st.markdown(f'<div class="big-number loss-box">Operating Loss: {format_currency(operating_profit)}<br>Margin: {operating_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.error("⚠️ Your operating expenses are too high! You're losing money before interest and taxes.")
    
    st.markdown("---")
    
    # Interest and Taxes
    st.markdown("## 🏦 INTEREST & TAXES")
    
    col1, col2 = st.columns(2)
    
    with col1:
        interest_expense = st.number_input("Interest Expense", value=30000.0, step=5000.0,
                                          help="💡 Interest on loans and debt")
        st.caption("💳 Real-life: Interest on your $500k business loan = $30,000")
    
    with col2:
        tax_expense = st.number_input("Tax Expense", value=50000.0, step=5000.0,
                                     help="💡 Income taxes")
        st.caption("🏛️ Real-life: Corporate income tax = $50,000")
    
    # Calculate EBT
    ebt = operating_profit - interest_expense
    st.markdown("### 📊 Earnings Before Tax (EBT)")
    st.markdown(f"**{format_currency(operating_profit)} - {format_currency(interest_expense)} = {format_currency(ebt)}**")
    
    # Calculate Net Income
    net_income = ebt - tax_expense
    net_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0
    
    st.markdown("---")
    st.markdown("## 🎯 NET INCOME (The Bottom Line)")
    st.markdown(f"**Formula:** EBT - Taxes = Net Income")
    st.markdown(f"**{format_currency(ebt)} - {format_currency(tax_expense)} = {format_currency(net_income)}**")
    
    if net_income > 0:
        st.markdown(f'<div class="big-number profit-box">🎉 NET PROFIT: {format_currency(net_income)}<br>Net Margin: {net_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.balloons()
        st.success(f"🎉 Congratulations! Your business made a profit of {format_currency(net_income)}! This is what you can reinvest or pay to owners!")
    else:
        st.markdown(f'<div class="big-number loss-box">😞 NET LOSS: {format_currency(net_income)}<br>Net Margin: {net_margin:.1f}%</div>', 
                   unsafe_allow_html=True)
        st.error(f"😞 Your business lost {format_currency(abs(net_income))}. You need to increase revenue or decrease expenses!")
    
    # Complete P&L Statement
    st.markdown("---")
    st.markdown("## 📋 Complete P&L Statement")
    
    pnl_data = {
        "Item": [
            "Revenue",
            "Less: Cost of Goods Sold",
            "= Gross Profit",
            "",
            "Less: Operating Expenses",
            "= Operating Profit (EBIT)",
            "",
            "Less: Interest Expense",
            "= Earnings Before Tax",
            "",
            "Less: Income Tax",
            "= NET INCOME"
        ],
        "Amount": [
            format_currency(total_revenue),
            format_currency(total_cogs),
            format_currency(gross_profit),
            "",
            format_currency(total_opex),
            format_currency(operating_profit),
            "",
            format_currency(interest_expense),
            format_currency(ebt),
            "",
            format_currency(tax_expense),
            format_currency(net_income)
        ],
        "% of Revenue": [
            "100.0%",
            f"{(total_cogs/total_revenue*100):.1f}%",
            f"{gross_margin:.1f}%",
            "",
            f"{(total_opex/total_revenue*100):.1f}%",
            f"{operating_margin:.1f}%",
            "",
            f"{(interest_expense/total_revenue*100):.1f}%",
            f"{(ebt/total_revenue*100):.1f}%",
            "",
            f"{(tax_expense/total_revenue*100):.1f}%",
            f"{net_margin:.1f}%"
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(pnl_data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    # Visualizations
    st.markdown("---")
    st.markdown("## 📊 Visual Analysis")
    
    # Waterfall Chart
    fig = go.Figure(go.Waterfall(
        name = "P&L", orientation = "v",
        measure = ["relative", "relative", "total", "relative", "total", "relative", "relative", "total"],
        x = ["Revenue", "COGS", "Gross Profit", "OpEx", "Operating Profit", "Interest", "Tax", "Net Income"],
        y = [total_revenue, -total_cogs, 0, -total_opex, 0, -interest_expense, -tax_expense, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#dc3545"}},
        increasing = {"marker":{"color":"#28a745"}},
        totals = {"marker":{"color":"#0d6efd"}}
    ))
    fig.update_layout(title="P&L Waterfall: From Revenue to Net Income", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Margin Comparison
    fig2 = go.Figure(data=[
        go.Bar(name='Margins', x=['Gross Margin', 'Operating Margin', 'Net Margin'],
               y=[gross_margin, operating_margin, net_margin],
               marker_color=['#90EE90', '#FFD700', '#87CEEB'],
               text=[f"{gross_margin:.1f}%", f"{operating_margin:.1f}%", f"{net_margin:.1f}%"],
               textposition='auto')
    ])
    fig2.update_layout(title="Profitability Margins", yaxis_title="Percentage (%)", height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# CHALLENGE MODE
# ---------------------------
elif "Challenge Mode" in mode:
    st.header("🎮 Challenge Mode: Run Your Own Business!")
    
    st.markdown("""
    <div class="info-box">
    <b>🎯 Your Mission:</b> You're the CEO! Make smart business decisions to maximize profit.
    Each challenge presents a different business situation. Can you turn a profit?
    </div>
    """, unsafe_allow_html=True)
    
    challenge = st.selectbox("Select a Business Challenge:", [
        "🍕 Challenge 1: Save the Struggling Pizzeria",
        "☕ Challenge 2: Coffee Shop Price War",
        "👕 Challenge 3: T-Shirt Business Expansion",
        "💻 Challenge 4: Software Startup Decisions",
        "🎲 Challenge 5: Random Business Scenario"
    ])
    
    if st.button("🎮 Start Challenge!", type="primary"):
        st.session_state.game_mode = challenge
    
    if st.session_state.game_mode:
        st.markdown("---")
        
        # Challenge 1: Struggling Pizzeria
        if "Challenge 1" in st.session_state.game_mode:
            st.markdown("### 🍕 Challenge 1: Save the Struggling Pizzeria")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> "Tony's Pizzeria" is losing money! Last month they had:
            - Revenue: $80,000 (sold 4,000 pizzas at $20 each)
            - COGS: $50,000 (ingredients + pizza chef wages)
            - Operating Expenses: $45,000 (rent, marketing, admin)
            - Interest: $3,000
            - Tax: $0 (no profit, no tax!)
            
            <b>Result: LOSS of $18,000!</b>
            
            <b>Your Job:</b> Make ONE change to turn a profit! What will you do?
            </div>
            """, unsafe_allow_html=True)
            
            decision = st.radio("Choose your strategy:", [
                "💰 Raise pizza price to $25 (25% increase)",
                "📉 Reduce COGS to $40,000 (negotiate better ingredient prices)",
                "✂️ Cut operating expenses to $35,000 (reduce marketing, downsize staff)",
                "📈 Increase sales to 5,000 pizzas (better marketing, same $20 price)"
            ])
            
            if st.button("Execute Strategy!"):
                # Calculate based on decision
                if "Raise pizza price" in decision:
                    revenue = 4000 * 25
                    cogs = 50000
                    opex = 45000
                    explanation = "By raising prices from $20 to $25, you increased revenue by $20,000 (4,000 pizzas × $5)!"
                    risk = "⚠️ Risk: Some customers might leave due to higher prices"
                
                elif "Reduce COGS" in decision:
                    revenue = 80000
                    cogs = 40000
                    opex = 45000
                    explanation = "By negotiating with suppliers, you reduced ingredient costs by $10,000!"
                    risk = "⚠️ Risk: Make sure quality doesn't suffer with cheaper ingredients"
                
                elif "Cut operating" in decision:
                    revenue = 80000
                    cogs = 50000
                    opex = 35000
                    explanation = "By cutting expenses, you saved $10,000 (maybe reduced marketing budget or let go of some staff)"
                    risk = "⚠️ Risk: Less marketing might reduce future sales, fewer staff might hurt service quality"
                
                else:  # Increase sales
                    revenue = 5000 * 20
                    cogs = 50000 + 12500  # More pizzas = more ingredients
                    opex = 45000
                    explanation = "By selling 1,000 more pizzas, you increased revenue by $20,000! COGS increased by $12,500 for extra ingredients."
                    risk = "⚠️ Risk: Can your kitchen handle 25% more volume?"
                
                interest = 3000
                
                gross_profit = revenue - cogs
                operating_profit = gross_profit - opex
                ebt = operating_profit - interest
                net_income = ebt  # No tax if loss, simplified for game
                
                if net_income > 0:
                    tax = net_income * 0.2
                    net_income = ebt - tax
                else:
                    tax = 0
                
                st.markdown("---")
                st.markdown("### 📊 Results After Your Decision")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Revenue", format_currency(revenue))
                col2.metric("COGS", format_currency(cogs))
                col3.metric("OpEx", format_currency(opex))
                col4.metric("Interest", format_currency(interest))
                
                st.markdown("---")
                
                if net_income > 0:
                    st.markdown(f'<div class="success-box">🎉 SUCCESS! Net Profit: {format_currency(net_income)}</div>', 
                               unsafe_allow_html=True)
                    st.balloons()
                    st.success(f"✅ {explanation}")
                    st.warning(risk)
                    st.info("💡 In real business, you'd want to monitor this change closely and be ready to adjust!")
                else:
                    st.markdown(f'<div class="warning-box">😞 Still Losing: {format_currency(net_income)}</div>', 
                               unsafe_allow_html=True)
                    st.error("Try a different strategy or make bigger changes!")
                
                # Show P&L
                pnl_comparison = {
                    "Item": ["Revenue", "COGS", "Gross Profit", "Operating Expenses", "Operating Profit", "Interest", "Tax", "NET INCOME"],
                    "Before": ["$80,000", "$50,000", "$30,000", "$45,000", "-$15,000", "$3,000", "$0", "-$18,000"],
                    "After": [
                        format_currency(revenue),
                        format_currency(cogs),
                        format_currency(gross_profit),
                        format_currency(opex),
                        format_currency(operating_profit),
                        format_currency(interest),
                        format_currency(tax),
                        format_currency(net_income)
                    ]
                }
                
                import pandas as pd
                df_comp = pd.DataFrame(pnl_comparison)
                st.markdown("### 📋 Before vs After Comparison")
                st.dataframe(df_comp, hide_index=True, use_container_width=True)
        
        # Challenge 2: Coffee Shop Price War
        elif "Challenge 2" in st.session_state.game_mode:
            st.markdown("### ☕ Challenge 2: Coffee Shop Price War")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> Your coffee shop "Bean Dreams" is doing well, but Starbucks just opened next door!
            
            <b>Current Situation (Monthly):</b>
            - You sell 10,000 coffees at $5 each = $50,000 revenue
            - COGS: $15,000 (beans, milk, cups)
            - Operating Expenses: $20,000 (rent, staff, utilities)
            - Interest: $1,000
            - Current Net Profit: ~$11,000
            
            <b>The Problem:</b> Starbucks is stealing customers! Sales dropped to 7,000 coffees this month.
            
            <b>Your Job:</b> How will you compete?
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### Current Month Projection (if you do nothing):")
            
            sales_volume = st.slider("☕ Expected Coffee Sales This Month", 5000, 10000, 7000, step=500,
                                    help="Starbucks competition has reduced your sales")
            
            price = st.slider("💵 Coffee Price", 3.0, 7.0, 5.0, step=0.25,
                             help="Should you lower prices to compete? Or raise them for premium positioning?")
            
            marketing_spend = st.slider("📱 Extra Marketing Budget", 0, 10000, 0, step=1000,
                                       help="Invest in marketing to fight back? This adds to operating expenses")
            
            # Calculate results
            revenue = sales_volume * price
            cogs = sales_volume * 1.5  # $1.50 per coffee in direct costs
            opex = 20000 + marketing_spend
            interest = 1000
            
            gross_profit = revenue - cogs
            operating_profit = gross_profit - opex
            ebt = operating_profit - interest
            
            if ebt > 0:
                tax = ebt * 0.2
                net_income = ebt - tax
            else:
                tax = 0
                net_income = ebt
            
            net_margin = (net_income / revenue * 100) if revenue > 0 else 0
            
            st.markdown("---")
            st.markdown("### 📊 Projected Results")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Revenue", format_currency(revenue), delta=format_currency(revenue - 50000))
            col2.metric("Total Expenses", format_currency(cogs + opex + interest + tax))
            col3.metric("Net Income", format_currency(net_income), delta=format_currency(net_income - 11000))
            
            if net_income > 11000:
                st.markdown(f'<div class="success-box">🎉 WINNING! Profit: {format_currency(net_income)} (+{((net_income/11000-1)*100):.0f}%)</div>', 
                           unsafe_allow_html=True)
                st.balloons()
                st.success("✅ Great strategy! You're beating the competition!")
                
                if price < 5:
                    st.info("💡 You competed on price. Make sure you can sustain these margins long-term!")
                if marketing_spend > 5000:
                    st.info("💡 Heavy marketing investment! Track your customer acquisition cost!")
                if sales_volume > 8000:
                    st.info("💡 Volume is up! Make sure you have enough staff and supplies to handle demand!")
                    
            elif net_income > 0:
                st.markdown(f'<div class="warning-box">😐 Surviving... Profit: {format_currency(net_income)}</div>', 
                           unsafe_allow_html=True)
                st.warning("⚠️ You're still profitable but earning less than before. Can you do better?")
                
            else:
                st.markdown(f'<div class="warning-box">😞 LOSING MONEY: {format_currency(net_income)}</div>', 
                           unsafe_allow_html=True)
                st.error("❌ This strategy isn't working! Try adjusting your approach.")
            
            # Business insights
            st.markdown("---")
            st.markdown("### 💡 Business Insights")
            
            original_profit = 11000
            current_profit = net_income
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Your Strategy:**")
                if price < 5:
                    st.write(f"🔽 Lower price (${price}): Competing on cost")
                elif price > 5:
                    st.write(f"🔼 Higher price (${price}): Premium positioning")
                else:
                    st.write(f"➡️ Same price (${price}): Holding steady")
                
                if marketing_spend > 0:
                    st.write(f"📱 Marketing: +${marketing_spend:,}")
                
                if sales_volume < 7000:
                    st.write(f"📉 Low volume: {sales_volume} coffees")
                elif sales_volume > 9000:
                    st.write(f"📈 High volume: {sales_volume} coffees")
            
            with col2:
                st.markdown("**🎯 Key Metrics:**")
                st.write(f"Gross Margin: {(gross_profit/revenue*100):.1f}%")
                st.write(f"Operating Margin: {(operating_profit/revenue*100):.1f}%")
                st.write(f"Net Margin: {net_margin:.1f}%")
                st.write(f"Profit per Coffee: ${net_income/sales_volume:.2f}")
        
        # Challenge 3: T-Shirt Business
        elif "Challenge 3" in st.session_state.game_mode:
            st.markdown("### 👕 Challenge 3: T-Shirt Business Expansion Decision")
            st.markdown("""
            <div class="tip-box">
            <b>Scenario:</b> Your online t-shirt business is profitable! Current situation (per month):
            - Selling 1,000 t-shirts at $25 each = $25,000
            - COGS: $10 per shirt = $10,000
            - Operating Expenses: $8,000
            - Net Profit: ~$5,000/month
            
            <b>Opportunity:</b> A big retailer wants to buy 2,000 shirts per month, but they'll only pay $18 per shirt (wholesale price).
            Your COGS will stay at $10, but you'll need to hire 2 more people (+$4,000/month in OpEx).
            
            <b>Decision:</b> Should you take the wholesale deal or keep focusing on direct sales?
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Option A: Keep Current Business")
                st.write("- Revenue: $25,000")
                st.write("- COGS: $10,000")
                st.write("- OpEx: $8,000")
                st.write("- **Profit: $5,400** (after tax)")
                
            with col2:
                st.markdown("#### 📊 Option B: Take Wholesale Deal")
                st.write("- Direct Sales: 1,000 × $25 = $25,000")
                st.write("- Wholesale: 2,000 × $18 = $36,000")
                st.write("- Total Revenue: $61,000")
                st.write("- COGS: 3,000 × $10 = $30,000")
                st.write("- OpEx: $12,000 (hired 2 people)")
                st.write("- **Profit: $15,200** (after tax)")
            
            decision = st.radio("What's your decision?", [
                "Option A: Stay small, keep $5,400/month profit",
                "Option B: Take wholesale deal, make $15,200/month profit"
            ])
            
            if st.button("Make Decision!"):
                if "Option B" in decision:
                    st.markdown('<div class="success-box">🎉 GREAT CHOICE! You nearly TRIPLED your profit!</div>', 
                               unsafe_allow_html=True)
                    st.balloons()
                    st.success("""
                    ✅ **Why this works:**
                    - Even though wholesale price ($18) is lower than retail ($25), the VOLUME makes up for it
                    - You're making $8 per wholesale shirt ($18 - $10 COGS) × 2,000 = $16,000 gross profit from wholesale
                    - The $4,000 extra in OpEx is worth it for $16,000 extra gross profit
                    - Economies of scale at work!
                    """)
                    st.warning("""
                    ⚠️ **Risks to consider:**
                    - What if the retailer cancels the contract?
                    - Can you handle 3x the production volume?
                    - Will you have time for direct customers?
                    """)
                else:
                    st.markdown('<div class="warning-box">🤔 Playing it safe...</div>', 
                               unsafe_allow_html=True)
                    st.info("""
                    💡 **You chose stability over growth.**
                    - Lower risk (no dependency on one big customer)
                    - Easier to manage
                    - But you're leaving $10,000/month on the table!
                    - Sometimes growth requires taking calculated risks
                    """)
                
                # Show detailed P&L comparison
                st.markdown("---")
                st.markdown("### 📋 Detailed P&L Comparison")
                
                comparison_data = {
                    "Line Item": ["Revenue", "COGS", "Gross Profit", "Operating Expenses", "Operating Profit", "Tax (20%)", "NET INCOME"],
                    "Option A (Current)": ["$25,000", "$10,000", "$15,000", "$8,000", "$7,000", "$1,400", "$5,600"],
                    "Option B (Wholesale)": ["$61,000", "$30,000", "$31,000", "$12,000", "$19,000", "$3,800", "$15,200"]
                }
                
                import pandas as pd
                df_comp = pd.DataFrame(comparison_data)
                st.dataframe(df_comp, hide_index=True, use_container_width=True)

# ---------------------------
# REAL-WORLD SCENARIOS
# ---------------------------
elif "Real-World" in mode:
    st.header("🏢 Real-World Business Scenarios")
    
    st.markdown("""
    <div class="info-box">
    <b>Follow real businesses through their journey and see how the P&L tells their story!</b><br>
    Watch how revenue, expenses, and profit change as businesses grow, struggle, and adapt.
    </div>
    """, unsafe_allow_html=True)
    
    scenario = st.selectbox("Choose a Business Journey:", [
        "🍕 Pizza Restaurant: First Year Journey",
        "📱 Mobile App: Startup to Profitability",
        "🏋️ Gym: Seasonal Business Cycles",
        "🛍️ E-commerce Store: Scaling Up"
    ])
    
    if "Pizza Restaurant" in scenario:
        st.markdown("### 🍕 Tony's Pizzeria: The First Year")
        
        month = st.slider("Follow the journey through Year 1:", 1, 12, 1)
        
        # Define monthly story
        monthly_data = {
            1: {"revenue": 15000, "cogs": 9000, "opex": 18000, "story": "🎉 **Grand Opening!** Lots of expenses (renovations, marketing), low sales. First month jitters!"},
            2: {"revenue": 22000, "cogs": 13000, "opex": 15000, "story": "📈 **Word is spreading!** Sales improving as people discover us. Still spending heavily on marketing."},
            3: {"revenue": 30000, "cogs": 17000, "opex": 14000, "story": "🌟 **Getting known!** Local newspaper featured us. Sales climbing, reduced marketing spend."},
            4: {"revenue": 35000, "cogs": 19000, "opex": 13000, "story": "💪 **Finding rhythm!** Operations smoothing out. First profitable month!"},
            5: {"revenue": 40000, "cogs": 22000, "opex": 13000, "story": "☀️ **Summer boost!** Patio seating open. Catering for local events."},
            6: {"revenue": 45000, "cogs": 24000, "opex": 14000, "story": "🎊 **Hitting stride!** Hired second pizza chef. Tourist season helps."},
            7: {"revenue": 42000, "cogs": 23000, "opex": 13500, "story": "🌴 **Vacation slowdown** Many regulars on vacation, but still solid."},
            8: {"revenue": 38000, "cogs": 21000, "opex": 13000, "story": "🏫 **Back to school** Families back, but slower than summer peak."},
            9: {"revenue": 48000, "cogs": 26000, "opex": 14000, "story": "🏈 **Football season!** Game day specials are huge. Best month yet!"},
            10: {"revenue": 44000, "cogs": 24000, "opex": 13500, "story": "🍂 **Autumn steady** Consistent regulars. Holiday catering orders coming in."},
            11: {"revenue": 52000, "cogs": 28000, "opex": 15000, "story": "🦃 **Holiday parties!** Thanksgiving catering boom. Extra staff needed."},
            12: {"revenue": 55000, "cogs": 30000, "opex": 16000, "story": "🎄 **Holiday season!** Office parties, family gatherings. Best revenue ever!"}
        }
        
        data = monthly_data[month]
        revenue = data["revenue"]
        cogs = data["cogs"]
        opex = data["opex"]
        interest = 2000  # Constant loan payment
        
        gross_profit = revenue - cogs
        operating_profit = gross_profit - opex
        ebt = operating_profit - interest
        tax = max(0, ebt * 0.2)
        net_income = ebt - tax
        
        # Show story
        st.markdown(f"## Month {month}")
        st.markdown(f'<div class="info-box">{data["story"]}</div>', unsafe_allow_html=True)
        
        # Show P&L
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Revenue", format_currency(revenue))
        col2.metric("COGS", format_currency(cogs))
        col3.metric("OpEx", format_currency(opex))
        col4.metric("Interest", format_currency(interest))
        
        st.markdown("---")
        
        if net_income > 0:
            st.markdown(f'<div class="big-number profit-box">Month {month} Profit: {format_currency(net_income)}</div>', 
                       unsafe_allow_html=True)
            st.success(f"✅ Profitable month! Net margin: {(net_income/revenue*100):.1f}%")
        else:
            st.markdown(f'<div class="big-number loss-box">Month {month} Loss: {format_currency(net_income)}</div>', 
                       unsafe_allow_html=True)
            st.warning(f"⚠️ Losing money this month. Common in early months!")
        
        # Cumulative tracking
        cumulative_revenue = sum([monthly_data[m]["revenue"] for m in range(1, month+1)])
        cumulative_cogs = sum([monthly_data[m]["cogs"] for m in range(1, month+1)])
        cumulative_opex = sum([monthly_data[m]["opex"] for m in range(1, month+1)])
        cumulative_interest = interest * month
        cumulative_ebt = cumulative_revenue - cumulative_cogs - cumulative_opex - cumulative_interest
        cumulative_tax = max(0, cumulative_ebt * 0.2)
        cumulative_profit = cumulative_ebt - cumulative_tax
        
        st.markdown("---")
        st.markdown(f"### 📊 Year-to-Date (Months 1-{month})")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Revenue", format_currency(cumulative_revenue))
            st.metric("Total Expenses", format_currency(cumulative_cogs + cumulative_opex + cumulative_interest + cumulative_tax))
        with col2:
            st.metric("Net Profit/Loss YTD", format_currency(cumulative_profit))
            if cumulative_profit > 0:
                st.success(f"✅ Profitable YTD!")
            else:
                st.warning(f"⚠️ Still in the red YTD - normal for new businesses!")
        
        # Chart showing trend
        months_so_far = list(range(1, month + 1))
        revenues = [monthly_data[m]["revenue"] for m in months_so_far]
        profits = []
        for m in months_so_far:
            m_rev = monthly_data[m]["revenue"]
            m_cogs = monthly_data[m]["cogs"]
            m_opex = monthly_data[m]["opex"]
            m_ebt = m_rev - m_cogs - m_opex - interest
            m_tax = max(0, m_ebt * 0.2)
            m_profit = m_ebt - m_tax
            profits.append(m_profit)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months_so_far, y=revenues, name='Revenue', line=dict(color='blue', width=3)))
        fig.add_trace(go.Scatter(x=months_so_far, y=profits, name='Net Profit', line=dict(color='green', width=3)))
        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Break-even")
        fig.update_layout(title=f"Revenue & Profit Trend (Months 1-{month})", 
                         xaxis_title="Month", yaxis_title="Amount ($)", height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Key learnings based on month
        st.markdown("---")
        st.markdown("### 💡 Key Business Lessons")
        
        if month <= 3:
            st.info("""
            **Early Stage Challenges:**
            - High initial expenses (renovations, equipment, marketing)
            - Low revenue while building customer base
            - Losing money is NORMAL in first few months
            - Focus on getting your name out there!
            """)
        elif month <= 6:
            st.info("""
            **Growth Phase:**
            - Revenue growing as word spreads
            - Operating expenses stabilizing
            - Starting to see light at end of tunnel
            - Customer retention becoming key
            """)
        else:
            st.info("""
            **Mature Operations:**
            - Established customer base
            - Predictable expenses
            - Seasonal patterns emerging
            - Focus on consistency and efficiency
            - Plan for slow seasons!
            """)
    
    elif "Mobile App" in scenario:
        st.markdown("### 📱 SocialBuzz App: Startup to Profitability")
        
        quarter = st.slider("Track quarterly performance:", 1, 8, 1, 
                           help="Watch how a mobile app grows from startup to profitable business")
        
        # Define quarterly journey
        quarters_data = {
            1: {"users": 5000, "revenue": 2000, "opex": 150000, "story": "🚀 **Launch Quarter!** Huge development costs, minimal revenue. Focus is on building the product."},
            2: {"users": 25000, "revenue": 10000, "opex": 180000, "story": "📱 **User Growth!** Going viral on TikTok. Heavy marketing spend. Still burning cash."},
            3: {"users": 75000, "revenue": 45000, "opex": 200000, "story": "🌟 **Traction!** Featured on app stores. Added in-app purchases. Revenue accelerating!"},
            4: {"users": 150000, "revenue": 120000, "opex": 220000, "story": "💪 **Scale Mode!** Hired more developers. Server costs increasing with users."},
            5: {"users": 300000, "revenue": 240000, "opex": 250000, "story": "📈 **Revenue > OpEx!** First profitable quarter! Investors happy!"},
            6: {"users": 500000, "revenue": 400000, "opex": 280000, "story": "🎉 **Growth Sustaining!** Premium subscriptions working. Unit economics looking good."},
            7: {"users": 750000, "revenue": 600000, "opex": 320000, "story": "💎 **Premium Focus!** Converting free users to paid. Margins improving."},
            8: {"users": 1000000, "revenue": 850000, "opex": 350000, "story": "🏆 **Million Users!** Major milestone. Considering Series B funding."}
        }
        
        data = quarters_data[quarter]
        users = data["users"]
        revenue = data["revenue"]
        opex = data["opex"]
        cogs = revenue * 0.15  # Server/hosting costs scale with revenue
        
        gross_profit = revenue - cogs
        operating_profit = gross_profit - opex
        net_income = operating_profit  # Simplified, no interest or tax for startup
        
        st.markdown(f"## Q{quarter} - Year {(quarter-1)//4 + 1}")
        st.markdown(f'<div class="info-box">{data["story"]}</div>', unsafe_allow_html=True)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Users", f"{users:,}", delta=f"+{users - quarters_data[max(1, quarter-1)]['users']:,}" if quarter > 1 else None)
        col2.metric("Revenue", format_currency(revenue))
        col3.metric("OpEx", format_currency(opex))
        col4.metric("Burn Rate" if net_income < 0 else "Profit", format_currency(abs(net_income)))
        
        # Revenue per user
        revenue_per_user = revenue / users if users > 0 else 0
        st.metric("💰 Revenue per User (ARPU)", f"${revenue_per_user:.2f}")
        
        if net_income > 0:
            st.markdown(f'<div class="success-box">🎉 PROFITABLE! Net Income: {format_currency(net_income)}</div>', 
                       unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f'<div class="warning-box">💸 Burning Cash: {format_currency(abs(net_income))}/quarter</div>', 
                       unsafe_allow_html=True)
            if quarter <= 4:
                st.info("💡 Normal for early-stage startups! Focus is on growth, not profit yet.")
            else:
                st.warning("⚠️ Need to reach profitability soon or raise more funding!")
        
        # Show trend
        quarters_so_far = list(range(1, quarter + 1))
        user_trend = [quarters_data[q]["users"] for q in quarters_so_far]
        revenue_trend = [quarters_data[q]["revenue"] for q in quarters_so_far]
        profit_trend = []
        for q in quarters_so_far:
            q_rev = quarters_data[q]["revenue"]
            q_cogs = q_rev * 0.15
            q_opex = quarters_data[q]["opex"]
            profit_trend.append(q_rev - q_cogs - q_opex)
        
        fig = make_subplots(rows=1, cols=2, subplot_titles=("User Growth", "Revenue vs Profit"))
        
        fig.add_trace(go.Scatter(x=quarters_so_far, y=user_trend, name='Users', 
                                line=dict(color='purple', width=3)), row=1, col=1)
        
        fig.add_trace(go.Scatter(x=quarters_so_far, y=revenue_trend, name='Revenue',
                                line=dict(color='blue', width=3)), row=1, col=2)
        fig.add_trace(go.Scatter(x=quarters_so_far, y=profit_trend, name='Profit/Loss',
                                line=dict(color='green', width=3)), row=1, col=2)
        fig.add_hline(y=0, line_dash="dash", line_color="red", row=1, col=2)
        
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("### 💡 Startup Financial Lessons")
        st.info("""
        **The Startup P&L Journey:**
        
        1. **Early Stage (Q1-Q2):** Massive losses are normal. You're building the product and user base.
        
        2. **Growth Stage (Q3-Q4):** Revenue starts coming in, but you're still investing heavily in growth.
        
        3. **Scale Stage (Q5-Q6):** Revenue catches up to expenses. First profitable quarters!
        
        4. **Maturity (Q7-Q8):** Sustainable profitability. Focus shifts from "growth at all costs" to "profitable growth."
        
        **Key Metrics for Apps:**
        - **ARPU (Average Revenue Per User):** How much each user generates
        - **CAC (Customer Acquisition Cost):** How much you spend to get each user
        - **LTV (Lifetime Value):** Total revenue from a user over their lifetime
        - **Burn Rate:** How fast you're spending cash (critical for runway)
        """)

# Educational Footer
st.markdown("---")
st.markdown("### 📚 Key P&L Takeaways:")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Understanding the P&L:**
    1. **Revenue** is at the top - that's why we call it the "top line"
    2. **Net Income** is at the bottom - the "bottom line"
    3. **Every expense** reduces profit
    4. **Margins matter** - it's not just about revenue, but profit percentage
    5. **Timing matters** - businesses have good months and bad months
    """)

with col2:
    st.markdown("""
    **P&L vs Balance Sheet:**
    - **P&L:** Shows performance over a PERIOD (month, quarter, year)
    - **Balance Sheet:** Shows position at a POINT IN TIME
    - **Connection:** Net Income from P&L flows into Retained Earnings on Balance Sheet
    - **Both matter:** P&L shows profitability, Balance Sheet shows financial health
    """)

st.success("""
💡 **Pro Tip:** In real business, you analyze BOTH the P&L and Balance Sheet together. 
A company can be profitable (positive P&L) but still go bankrupt if they can't pay their bills (poor Balance Sheet liquidity)!
Practice with both tools to become a financial analysis pro!
""")
