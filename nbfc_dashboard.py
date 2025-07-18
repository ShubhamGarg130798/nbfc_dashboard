import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page config
st.set_page_config(
    page_title="NBFC Business Calculator",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #2E8B57, #4169E1);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.metric-card {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #2E8B57;
    margin: 5px 0;
}
.alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
.alert-warning {
    background-color: #fff3cd;
    border-color: #ffeaa7;
    color: #856404;
    padding: 10px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div class="main-header">
    <h1>💰 Interactive NBFC Business Calculator</h1>
    <p>Adjust parameters below and see real-time impact on your business projections!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs - Make it more prominent
st.sidebar.markdown("# 🎛️ Business Parameters")
st.sidebar.markdown("**Change any value to see instant updates!**")

# Input Parameters Section
st.sidebar.markdown("## 💰 Capital Deployment")
month1_capital = st.sidebar.number_input("Month 1 Capital (₹ Crores)", 
                                         min_value=1.0, max_value=15.0, value=5.0, step=0.5, 
                                         help="Initial capital deployment")

month2_capital = st.sidebar.number_input("Month 2 Capital (₹ Crores)", 
                                         min_value=0.0, max_value=10.0, value=4.0, step=0.5)

month3_capital = st.sidebar.number_input("Month 3 Capital (₹ Crores)", 
                                         min_value=0.0, max_value=10.0, value=4.0, step=0.5)

month4_capital = st.sidebar.number_input("Month 4 Capital (₹ Crores)", 
                                         min_value=0.0, max_value=10.0, value=4.0, step=0.5)

month5_capital = st.sidebar.number_input("Month 5 Capital (₹ Crores)", 
                                         min_value=0.0, max_value=10.0, value=3.0, step=0.5)

total_capital = month1_capital + month2_capital + month3_capital + month4_capital + month5_capital

st.sidebar.markdown("## 📈 Revenue Parameters")
processing_fees = st.sidebar.slider("Processing Fees (%)", 
                                   min_value=5.0, max_value=20.0, value=11.8, step=0.1,
                                   help="One-time processing fee charged to customers")

monthly_interest = st.sidebar.slider("Monthly Interest Rate (%)", 
                                    min_value=15.0, max_value=50.0, value=30.0, step=0.5,
                                    help="Monthly interest charged on loans")

st.sidebar.markdown("## 💸 Cost Parameters")
cost_of_funds = st.sidebar.slider("Cost of Funds (% monthly)", 
                                 min_value=0.5, max_value=5.0, value=1.5, step=0.1,
                                 help="Monthly cost of borrowing capital")

marketing_expenses = st.sidebar.slider("Marketing Expenses (%)", 
                                      min_value=0.5, max_value=5.0, value=2.0, step=0.1,
                                      help="Marketing cost as % of disbursement")

opex_rates = {
    'Month 1': 10.0,
    'Month 2': st.sidebar.slider("OpEx Month 2 (%)", 5.0, 15.0, 10.0, 0.5),
    'Month 3': st.sidebar.slider("OpEx Month 3 (%)", 2.0, 10.0, 5.0, 0.5),
    'Month 4': st.sidebar.slider("OpEx Month 4+ (%)", 2.0, 8.0, 4.0, 0.5)
}

st.sidebar.markdown("## 🎯 Loan Parameters")
avg_loan_ticket = st.sidebar.number_input("Average Loan Ticket Size (₹)", 
                                          min_value=10000, max_value=50000, value=22000, step=1000,
                                          help="Average loan amount per customer")

rotation_cycle = st.sidebar.slider("Average Rotation Cycle (days)", 
                                  min_value=15, max_value=45, value=30, step=1,
                                  help="Time for one complete loan cycle")

st.sidebar.markdown("## 📅 Collection Parameters")
t0_collection = st.sidebar.slider("Same Day Collection (%)", 
                                 min_value=60, max_value=95, value=80, step=1)

t30_collection = st.sidebar.slider("T+30 Collection (%)", 
                                  min_value=0, max_value=15, value=5, step=1)

t60_collection = st.sidebar.slider("T+60 Collection (%)", 
                                  min_value=0, max_value=15, value=5, step=1)

t90_collection = st.sidebar.slider("T+90 Collection (%)", 
                                  min_value=0, max_value=10, value=3, step=1)

total_collection = t0_collection + t30_collection + t60_collection + t90_collection
default_rate = 100 - total_collection

# Calculate derived metrics
cycles_per_year = 365 / rotation_cycle
annual_roi = (1 + monthly_interest/100) ** 12 - 1

# Display key summary metrics
st.markdown("## 📊 Key Business Metrics")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("💰 Total Capital", f"₹{total_capital:.1f} Cr", 
             delta=f"{total_capital - 20:.1f} from target")

with col2:
    st.metric("📈 Annual ROI", f"{annual_roi*100:.1f}%", 
             delta=f"Monthly: {monthly_interest}%")

with col3:
    st.metric("🔄 Cycles/Year", f"{cycles_per_year:.1f}", 
             delta=f"{rotation_cycle} days each")

with col4:
    st.metric("✅ Collection Rate", f"{total_collection}%", 
             delta=f"Default: {default_rate:.1f}%")

with col5:
    st.metric("🎯 Loan Ticket", f"₹{avg_loan_ticket:,}", 
             delta="Per customer")

# Main calculation function
def calculate_monthly_projections():
    months = 12
    capital_deployed = [month1_capital*10000000, month2_capital*10000000, month3_capital*10000000, 
                       month4_capital*10000000, month5_capital*10000000, 0, 0, 0, 0, 0, 0, 0]
    
    results = []
    cumulative_capital = 0
    previous_aum = 0
    
    for month in range(months):
        # Capital available calculation
        if month == 0:
            capital_available = capital_deployed[month]
        else:
            capital_available = previous_aum + capital_deployed[month] + (results[month-1]['profit'] if results[month-1]['profit'] > 0 else 0)
        
        # Amount actually disbursed (markup applied)
        markup_factor = 1 + processing_fees/100
        amount_disbursed = capital_available * markup_factor
        
        # Number of customers
        num_customers = int(amount_disbursed / avg_loan_ticket)
        
        # Operational expenses
        if month == 0:
            opex_rate = 10.0  # Fixed for month 1
        elif month == 1:
            opex_rate = opex_rates['Month 2']
        elif month == 2:
            opex_rate = opex_rates['Month 3']
        else:
            opex_rate = opex_rates['Month 4']
        
        # Calculate costs
        opex = amount_disbursed * (opex_rate / 100) if month > 0 or amount_disbursed > 50000000 else 1500000
        api_cost = amount_disbursed * 0.02  # Simplified API cost
        marketing_cost = amount_disbursed * (marketing_expenses / 100)
        
        # Cost of funds (applied to specific months as per your model)
        fund_cost = 0
        if month in [2, 5, 8, 11]:  # Based on your Excel pattern
            fund_cost = capital_deployed[month] * (cost_of_funds / 100) if capital_deployed[month] > 0 else 0
        
        # Bad debt calculation
        bad_debt = amount_disbursed * (default_rate / 100)
        
        # GST calculation (18% on fees)
        gst = amount_disbursed * (processing_fees / 100) * 0.18
        
        # Revenue calculations
        interest_revenue = amount_disbursed * (monthly_interest / 100)
        processing_fee_revenue = amount_disbursed * (processing_fees / 100)
        bad_debt_recovery = bad_debt * 0.25 if month > 0 else 0  # 25% recovery
        
        # Total revenue and costs
        total_revenue = interest_revenue + processing_fee_revenue + bad_debt_recovery
        total_costs = opex + api_cost + marketing_cost + fund_cost + bad_debt + gst
        
        # Profit calculation
        profit = total_revenue - total_costs
        
        # AUM calculation
        aum = amount_disbursed + (previous_aum * 0.8) + profit  # Simplified AUM growth
        previous_aum = aum
        
        results.append({
            'month': month + 1,
            'capital_deployed': capital_deployed[month] / 10000000,
            'capital_available': capital_available / 10000000,
            'amount_disbursed': amount_disbursed / 10000000,
            'num_customers': num_customers,
            'interest_revenue': interest_revenue / 10000000,
            'processing_revenue': processing_fee_revenue / 10000000,
            'total_revenue': total_revenue / 10000000,
            'opex': opex / 10000000,
            'marketing_cost': marketing_cost / 10000000,
            'bad_debt': bad_debt / 10000000,
            'total_costs': total_costs / 10000000,
            'profit': profit / 10000000,
            'aum': aum / 10000000,
            'roi_percentage': (profit / amount_disbursed * 100) if amount_disbursed > 0 else 0
        })
    
    return pd.DataFrame(results)

# Calculate projections
df = calculate_monthly_projections()

# Charts section
st.markdown("---")
st.markdown("## 📈 Interactive Business Projections")

# Revenue vs Costs chart
fig_revenue_costs = go.Figure()

fig_revenue_costs.add_trace(go.Bar(
    x=df['month'],
    y=df['total_revenue'],
    name='Total Revenue',
    marker_color='#2E8B57',
    hovertemplate='Month %{x}<br>Revenue: ₹%{y:.2f} Cr<extra></extra>'
))

fig_revenue_costs.add_trace(go.Bar(
    x=df['month'],
    y=df['total_costs'],
    name='Total Costs',
    marker_color='#FF6B6B',
    hovertemplate='Month %{x}<br>Costs: ₹%{y:.2f} Cr<extra></extra>'
))

fig_revenue_costs.add_trace(go.Scatter(
    x=df['month'],
    y=df['profit'],
    mode='lines+markers',
    name='Net Profit',
    line=dict(color='#FFD700', width=4),
    marker=dict(size=8),
    hovertemplate='Month %{x}<br>Profit: ₹%{y:.2f} Cr<extra></extra>'
))

fig_revenue_costs.update_layout(
    title="Monthly Revenue, Costs & Profit Analysis",
    xaxis_title="Month",
    yaxis_title="Amount (₹ Crores)",
    hovermode='x unified',
    height=500
)

st.plotly_chart(fig_revenue_costs, use_container_width=True)

# AUM and Customer Growth
col1, col2 = st.columns(2)

with col1:
    fig_aum = px.area(
        df,
        x='month',
        y='aum',
        title="Assets Under Management (AUM) Growth",
        color_discrete_sequence=['#4169E1']
    )
    fig_aum.update_layout(
        xaxis_title="Month",
        yaxis_title="AUM (₹ Crores)",
        height=400
    )
    st.plotly_chart(fig_aum, use_container_width=True)

with col2:
    fig_customers = px.bar(
        df,
        x='month',
        y='num_customers',
        title="Monthly Customer Acquisition",
        color='num_customers',
        color_continuous_scale='viridis'
    )
    fig_customers.update_layout(
        xaxis_title="Month",
        yaxis_title="Number of Customers",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_customers, use_container_width=True)

# ROI Analysis
st.markdown("---")
st.markdown("## 🎯 Profitability Analysis")

fig_roi = px.line(
    df,
    x='month',
    y='roi_percentage',
    title="Monthly Return on Investment (ROI)",
    markers=True,
    line_shape='spline'
)
fig_roi.update_traces(line=dict(color='#FF6347', width=4), marker=dict(size=10))
fig_roi.update_layout(
    xaxis_title="Month",
    yaxis_title="ROI (%)",
    height=400
)
st.plotly_chart(fig_roi, use_container_width=True)

# Detailed breakdown table
st.markdown("---")
st.markdown("## 📋 Detailed Monthly Breakdown")

# Format the dataframe for display
display_df = df.copy()
display_df = display_df.round(2)
display_df.columns = ['Month', 'Capital Deployed (₹Cr)', 'Capital Available (₹Cr)', 
                     'Amount Disbursed (₹Cr)', 'Customers', 'Interest Revenue (₹Cr)',
                     'Processing Revenue (₹Cr)', 'Total Revenue (₹Cr)', 'OpEx (₹Cr)',
                     'Marketing Cost (₹Cr)', 'Bad Debt (₹Cr)', 'Total Costs (₹Cr)',
                     'Net Profit (₹Cr)', 'AUM (₹Cr)', 'ROI (%)']

st.dataframe(display_df, use_container_width=True, hide_index=True)

# Key insights and recommendations
st.markdown("---")
st.markdown("## 💡 Business Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📊 Performance Summary")
    
    total_revenue = df['total_revenue'].sum()
    total_costs = df['total_costs'].sum()
    total_profit = df['profit'].sum()
    final_aum = df['aum'].iloc[-1]
    avg_roi = df['roi_percentage'].mean()
    total_customers = df['num_customers'].sum()
    
    st.markdown(f"""
    **Financial Performance (12 months):**
    - 💰 **Total Revenue:** ₹{total_revenue:.2f} Crores
    - 💸 **Total Costs:** ₹{total_costs:.2f} Crores  
    - 📈 **Net Profit:** ₹{total_profit:.2f} Crores
    - 🏦 **Final AUM:** ₹{final_aum:.2f} Crores
    - 📊 **Average ROI:** {avg_roi:.1f}% per month
    - 👥 **Total Customers:** {total_customers:,}
    """)

with col2:
    st.markdown("### 🎯 Smart Recommendations")
    
    # Dynamic recommendations based on user inputs
    recommendations = []
    
    if avg_roi > 15:
        recommendations.append("🟢 **Excellent ROI**: Your model shows strong returns!")
    elif avg_roi > 8:
        recommendations.append("🟡 **Good Performance**: ROI is above industry average")
    else:
        recommendations.append("🔴 **Optimize Returns**: Consider increasing interest rates")
    
    if default_rate < 10:
        recommendations.append("🟢 **Low Risk**: Your collection efficiency is excellent")
    elif default_rate < 15:
        recommendations.append("🟡 **Moderate Risk**: Collection rates are acceptable")
    else:
        recommendations.append("🔴 **High Risk**: Focus on improving collection processes")
    
    if rotation_cycle < 25:
        recommendations.append("🟢 **Fast Cycles**: Excellent capital velocity")
    else:
        recommendations.append("🟡 **Standard Cycles**: Consider optimizing loan processing")
    
    if marketing_expenses > 3:
        recommendations.append("🟡 **Marketing Optimization**: Review marketing efficiency")
    
    for rec in recommendations:
        st.markdown(rec)

# Scenario comparison
st.markdown("---")
st.markdown("## 🔀 Quick Scenario Comparison")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🟢 Current Scenario")
    st.write(f"**Final Profit:** ₹{total_profit:.2f} Cr")
    st.write(f"**ROI:** {avg_roi:.1f}%/month")
    st.write(f"**Risk Level:** {default_rate:.1f}% default")

with col2:
    st.markdown("### 🔵 Conservative (-20%)")
    conservative_profit = total_profit * 0.8
    conservative_roi = avg_roi * 0.8
    st.write(f"**Final Profit:** ₹{conservative_profit:.2f} Cr")
    st.write(f"**ROI:** {conservative_roi:.1f}%/month")
    st.write(f"**Risk Level:** {default_rate * 0.7:.1f}% default")

with col3:
    st.markdown("### 🟡 Aggressive (+30%)")
    aggressive_profit = total_profit * 1.3
    aggressive_roi = avg_roi * 1.3
    st.write(f"**Final Profit:** ₹{aggressive_profit:.2f} Cr")
    st.write(f"**ROI:** {aggressive_roi:.1f}%/month")
    st.write(f"**Risk Level:** {default_rate * 1.3:.1f}% default")

# Export functionality
st.markdown("---")
st.markdown("## 📤 Export Your Analysis")

col1, col2 = st.columns(2)

with col1:
    csv_data = df.to_csv(index=False)
    st.download_button(
        label="📊 Download Detailed Data (CSV)",
        data=csv_data,
        file_name=f"nbfc_projection_{total_capital:.1f}cr.csv",
        mime="text/csv",
        help="Download complete monthly breakdown"
    )

with col2:
    summary_text = f"""
NBFC Business Projection Summary
Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

BUSINESS PARAMETERS:
- Total Capital: ₹{total_capital:.1f} Crores
- Monthly Interest: {monthly_interest}%
- Processing Fees: {processing_fees}%
- Average Ticket: ₹{avg_loan_ticket:,}
- Rotation Cycle: {rotation_cycle} days
- Collection Rate: {total_collection}%

FINANCIAL RESULTS (12 months):
- Total Revenue: ₹{total_revenue:.2f} Crores
- Total Costs: ₹{total_costs:.2f} Crores
- Net Profit: ₹{total_profit:.2f} Crores
- Final AUM: ₹{final_aum:.2f} Crores
- Average Monthly ROI: {avg_roi:.1f}%
- Total Customers: {total_customers:,}

GROWTH METRICS:
- Capital Multiplication: {final_aum/total_capital:.1f}x
- Revenue Growth: Strong upward trend
- Risk Profile: {default_rate:.1f}% default rate
"""
    
    st.download_button(
        label="📄 Download Summary Report",
        data=summary_text,
        file_name=f"nbfc_summary_{total_capital:.1f}cr.txt",
        mime="text/plain",
        help="Download executive summary"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <h4>🚀 Interactive NBFC Calculator</h4>
    <p>Adjust any parameter in the sidebar to see real-time updates across all charts and metrics!</p>
    <p><strong>Pro Tip:</strong> Save different scenarios by changing parameters and downloading the results.</p>
</div>
""", unsafe_allow_html=True)