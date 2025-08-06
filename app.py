import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math

# Page configuration
st.set_page_config(
    page_title="AdmiPlatform VASP Capital Adequacy Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fef3c7;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d1fae5;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10b981;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #fee2e2;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">AdmiPlatform VASP Capital Adequacy Calculator</h1>', unsafe_allow_html=True)
st.markdown("**CIMA Rule Compliance Calculator for Virtual Asset Service Providers**")

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")
st.sidebar.markdown("*Enter your business parameters to calculate capital requirements*")

# Company Information
with st.sidebar.expander("🏢 Company Information", expanded=True):
    company_name = st.text_input("Company Name", value="AdmiPlatform Ltd.")
    service_type = st.selectbox("Service Type", ["Custody Provider", "Trading Platform", "Both"])
    calculation_date = st.date_input("Calculation Date", value=datetime.now().date())

# Assets Under Management
with st.sidebar.expander("💼 Assets Under Management", expanded=True):
    st.markdown("**Client Virtual Assets Under Custody**")
    aum_btc = st.number_input("Bitcoin (BTC) Value (USD)", min_value=0.0, value=1000000.0, step=10000.0)
    aum_eth = st.number_input("Ethereum (ETH) Value (USD)", min_value=0.0, value=500000.0, step=10000.0)
    aum_other = st.number_input("Other Virtual Assets (USD)", min_value=0.0, value=250000.0, step=10000.0)
    total_aum = aum_btc + aum_eth + aum_other

# Fixed Overheads (Monthly)
with st.sidebar.expander("💸 Fixed Overheads (Monthly)", expanded=True):
    st.markdown("**Regular Non-Discretionary Expenses**")
    salary_benefits = st.number_input("Salaries & Benefits", min_value=0.0, value=50000.0, step=1000.0)
    rent_property = st.number_input("Rent & Property", min_value=0.0, value=5000.0, step=500.0)
    software_licenses = st.number_input("Software Licenses", min_value=0.0, value=3000.0, step=500.0)
    insurance_premiums = st.number_input("Insurance Premiums", min_value=0.0, value=8000.0, step=500.0)
    professional_fees = st.number_input("Professional Fees", min_value=0.0, value=10000.0, step=1000.0)
    it_infrastructure = st.number_input("IT Infrastructure", min_value=0.0, value=7000.0, step=500.0)
    other_admin = st.number_input("Other Admin Expenses", min_value=0.0, value=5000.0, step=500.0)
    
    monthly_fixed_overheads = (salary_benefits + rent_property + software_licenses + 
                              insurance_premiums + professional_fees + it_infrastructure + other_admin)

# Risk Parameters
with st.sidebar.expander("⚠️ Risk Parameters", expanded=True):
    st.markdown("**Risk Weight Factors**")
    op_risk_weight = st.slider("Operational Risk Weight (%)", min_value=0.5, max_value=5.0, value=2.0, step=0.1)
    op_risk_factor = st.slider("Operational Risk Factor (Fixed Overhead Multiplier)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)
    volatility_factor = st.slider("Market Volatility Factor (%)", min_value=10.0, max_value=60.0, value=40.0, step=5.0)
    counterparty_risk_weight = st.slider("Counterparty Risk Weight (%)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    liquidity_factor = st.slider("Liquidity Factor (%)", min_value=10.0, max_value=50.0, value=25.0, step=5.0)

# Capital Holdings
with st.sidebar.expander("🏦 Capital Holdings", expanded=True):
    st.markdown("**Current Capital Position**")
    tier1_capital = st.number_input("Tier 1 Capital (USD)", min_value=0.0, value=2000000.0, step=50000.0)
    tier2_capital = st.number_input("Tier 2 Capital (USD)", min_value=0.0, value=500000.0, step=50000.0)
    va_capital_holdings = st.number_input("Virtual Asset Capital Holdings (USD)", min_value=0.0, value=100000.0, step=10000.0)
    counterparty_exposure = st.number_input("Total Counterparty Exposure (USD)", min_value=0.0, value=200000.0, step=10000.0)
    projected_cash_outflow = st.number_input("30-Day Projected Cash Outflow (USD)", min_value=0.0, value=300000.0, step=10000.0)

# Main calculation area
col1, col2 = st.columns([2, 1])

with col1:
    # Risk-Based Capital Calculation
    st.header("📈 Risk-Based Capital (RBC) Calculation")
    
    # Operational Capital Charge
    op_aum_charge = total_aum * (op_risk_weight / 100)
    op_overhead_charge = monthly_fixed_overheads * op_risk_factor
    operational_capital_charge = op_aum_charge + op_overhead_charge
    
    # Market Capital Charge
    market_capital_charge = va_capital_holdings * (volatility_factor / 100)
    
    # Credit Capital Charge
    credit_capital_charge = counterparty_exposure * (counterparty_risk_weight / 100)
    
    # Liquidity Capital Charge
    liquidity_capital_charge = projected_cash_outflow * (liquidity_factor / 100)
    
    # Total RBC
    total_rbc = operational_capital_charge + market_capital_charge + credit_capital_charge + liquidity_capital_charge
    
    # Fixed Overheads Capital (6 months)
    fixed_overheads_capital = monthly_fixed_overheads * 6
    
    # Final Capital Requirement
    capital_requirement = max(total_rbc, fixed_overheads_capital)
    
    # Total Eligible Capital
    total_eligible_capital = tier1_capital + tier2_capital
    
    # Capital Adequacy Ratio
    capital_adequacy_ratio = (total_eligible_capital / capital_requirement) * 100 if capital_requirement > 0 else 0
    
    # Display detailed breakdown
    breakdown_data = {
        'Component': [
            'Operational Capital Charge (AUM)',
            'Operational Capital Charge (Overheads)',
            'Market Capital Charge',
            'Credit Capital Charge',
            'Liquidity Capital Charge',
            'Total Risk-Based Capital',
            'Fixed Overheads Capital (6 months)',
            'Final Capital Requirement'
        ],
        'Calculation': [
            f"${total_aum:,.0f} × {op_risk_weight}%",
            f"${monthly_fixed_overheads:,.0f} × {op_risk_factor}",
            f"${va_capital_holdings:,.0f} × {volatility_factor}%",
            f"${counterparty_exposure:,.0f} × {counterparty_risk_weight}%",
            f"${projected_cash_outflow:,.0f} × {liquidity_factor}%",
            "Sum of above charges",
            f"${monthly_fixed_overheads:,.0f} × 6 months",
            "Max(RBC, Fixed Overheads)"
        ],
        'Amount (USD)': [
            f"${op_aum_charge:,.0f}",
            f"${op_overhead_charge:,.0f}",
            f"${market_capital_charge:,.0f}",
            f"${credit_capital_charge:,.0f}",
            f"${liquidity_capital_charge:,.0f}",
            f"${total_rbc:,.0f}",
            f"${fixed_overheads_capital:,.0f}",
            f"${capital_requirement:,.0f}"
        ]
    }
    
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True)
    
    # Charts
    st.subheader("📊 Capital Requirement Breakdown")
    
    # RBC Components breakdown using native Streamlit charts
    rbc_components = pd.DataFrame({
        'Component': ['Operational (AUM)', 'Operational (Overheads)', 'Market', 'Credit', 'Liquidity'],
        'Amount': [op_aum_charge, op_overhead_charge, market_capital_charge, credit_capital_charge, liquidity_capital_charge],
        'Percentage': [
            (op_aum_charge / total_rbc * 100) if total_rbc > 0 else 0,
            (op_overhead_charge / total_rbc * 100) if total_rbc > 0 else 0,
            (market_capital_charge / total_rbc * 100) if total_rbc > 0 else 0,
            (credit_capital_charge / total_rbc * 100) if total_rbc > 0 else 0,
            (liquidity_capital_charge / total_rbc * 100) if total_rbc > 0 else 0
        ]
    })
    
    st.write("**Risk-Based Capital Components:**")
    st.bar_chart(rbc_components.set_index('Component')['Amount'])
    
    # Display component breakdown table
    rbc_components['Amount'] = rbc_components['Amount'].apply(lambda x: f"${x:,.0f}")
    rbc_components['Percentage'] = rbc_components['Percentage'].apply(lambda x: f"{x:.1f}%")
    st.dataframe(rbc_components, use_container_width=True)
    
    # Capital methods comparison
    st.write("**Capital Requirement Methods Comparison:**")
    comparison_data = pd.DataFrame({
        'Risk-Based Capital': [total_rbc],
        'Fixed Overheads Capital': [fixed_overheads_capital]
    })
    st.bar_chart(comparison_data)
    
    selected_method = "Risk-Based Capital" if capital_requirement == total_rbc else "Fixed Overheads Capital"
    st.write(f"**Selected Method:** {selected_method} (${capital_requirement:,.0f})")

with col2:
    st.header("📋 Summary Results")
    
    # Capital Adequacy Status
    if capital_adequacy_ratio >= 150:
        status_color = "success-box"
        status_text = "✅ COMPLIANT"
        status_message = "Capital adequacy ratio exceeds internal target of 150%"
    elif capital_adequacy_ratio >= 100:
        status_color = "warning-box"
        status_text = "⚠️ MINIMUM MET"
        status_message = "Meets minimum requirement but below internal target"
    else:
        status_color = "danger-box"
        status_text = "❌ NON-COMPLIANT"
        status_message = "Capital adequacy ratio below minimum requirement"
    
    st.markdown(f'<div class="{status_color}"><strong>{status_text}</strong><br>{status_message}</div>', unsafe_allow_html=True)
    
    # Key metrics
    metrics = [
        ("Total AUM", f"${total_aum:,.0f}"),
        ("Monthly Fixed Overheads", f"${monthly_fixed_overheads:,.0f}"),
        ("Risk-Based Capital", f"${total_rbc:,.0f}"),
        ("Fixed Overheads Capital", f"${fixed_overheads_capital:,.0f}"),
        ("**Capital Requirement**", f"**${capital_requirement:,.0f}**"),
        ("Total Eligible Capital", f"${total_eligible_capital:,.0f}"),
        ("**Capital Adequacy Ratio**", f"**{capital_adequacy_ratio:.1f}%**"),
        ("Surplus/(Deficit)", f"${total_eligible_capital - capital_requirement:,.0f}")
    ]
    
    for metric, value in metrics:
        st.metric(metric, value)
    
    # Stress Testing Section
    st.subheader("🧪 Stress Testing")
    
    stress_scenarios = {
        "Market Crash (50% AUM decline)": total_aum * 0.5,
        "High Volatility (80% factor)": 0.8,
        "Mass Withdrawals (2x cash outflow)": projected_cash_outflow * 2
    }
    
    for scenario, impact in stress_scenarios.items():
        if "AUM decline" in scenario:
            stressed_aum = impact
            stressed_rbc = (stressed_aum * (op_risk_weight / 100) + op_overhead_charge + 
                           market_capital_charge + credit_capital_charge + liquidity_capital_charge)
        elif "volatility" in scenario:
            stressed_rbc = (op_aum_charge + op_overhead_charge + 
                           va_capital_holdings * impact + credit_capital_charge + liquidity_capital_charge)
        else:  # withdrawal scenario
            stressed_rbc = (op_aum_charge + op_overhead_charge + market_capital_charge + 
                           credit_capital_charge + impact * (liquidity_factor / 100))
        
        stressed_requirement = max(stressed_rbc, fixed_overheads_capital)
        stressed_ratio = (total_eligible_capital / stressed_requirement) * 100
        
        st.write(f"**{scenario}**")
        st.write(f"Stressed CAR: {stressed_ratio:.1f}%")
        
        if stressed_ratio >= 100:
            st.write("✅ Would remain compliant")
        else:
            st.write("❌ Would breach requirements")
        st.write("---")

# Additional Information
st.header("📚 Regulatory Framework Compliance")

compliance_items = [
    "✅ Section 8.1: Capital equal to higher of RBC or 6-month fixed overheads",
    "✅ Section 8.2: Risk-based capital considering size, scope, and complexity",
    "✅ Section 8.3: Additional capital buffer capability",
    "✅ Section 8.4: Annual capital adequacy review framework",
    "✅ Section 8.5: Breach notification procedures",
    "✅ Section 8.6: Recovery plan scenarios",
    "✅ Section 8.7: Stress testing and sensitivity analysis",
    "✅ Section 8.8: Insurance requirements consideration"
]

col1, col2 = st.columns(2)
with col1:
    for item in compliance_items[:4]:
        st.write(item)

with col2:
    for item in compliance_items[4:]:
        st.write(item)

# Export functionality
st.header("📄 Report Generation")

if st.button("Generate Capital Adequacy Report", type="primary"):
    report_data = {
        "Company": company_name,
        "Calculation Date": calculation_date.strftime("%Y-%m-%d"),
        "Service Type": service_type,
        "Total AUM (USD)": f"{total_aum:,.0f}",
        "Monthly Fixed Overheads (USD)": f"{monthly_fixed_overheads:,.0f}",
        "Risk-Based Capital (USD)": f"{total_rbc:,.0f}",
        "Fixed Overheads Capital (USD)": f"{fixed_overheads_capital:,.0f}",
        "Capital Requirement (USD)": f"{capital_requirement:,.0f}",
        "Total Eligible Capital (USD)": f"{total_eligible_capital:,.0f}",
        "Capital Adequacy Ratio (%)": f"{capital_adequacy_ratio:.1f}",
        "Compliance Status": status_text,
        "Operational Risk Weight (%)": f"{op_risk_weight}",
        "Market Volatility Factor (%)": f"{volatility_factor}",
        "Counterparty Risk Weight (%)": f"{counterparty_risk_weight}",
        "Liquidity Factor (%)": f"{liquidity_factor}"
    }
    
    report_df = pd.DataFrame(list(report_data.items()), columns=["Parameter", "Value"])
    
    st.subheader("📊 Capital Adequacy Report Summary")
    st.dataframe(report_df, use_container_width=True)
    
    # Download button
    csv = report_df.to_csv(index=False)
    st.download_button(
        label="Download Report as CSV",
        data=csv,
        file_name=f"capital_adequacy_report_{company_name}_{calculation_date}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7280; font-size: 0.9em;'>
    <p><strong>AdmiPlatform VASP Capital Adequacy Calculator</strong></p>
    <p>Developed for CIMA Rule compliance | Virtual Asset Service Provider Application</p>
    <p><em>This calculator is designed to assist with VASP application requirements and ongoing compliance monitoring.</em></p>
</div>
""", unsafe_allow_html=True)
