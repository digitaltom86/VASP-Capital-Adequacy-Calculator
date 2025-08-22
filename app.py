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
st.markdown('<h1 class="main-header">AdmiPlatform Capital Adequacy Calculator</h1>', unsafe_allow_html=True)
st.markdown("**CIMA Rule Section 8 Compliance - Virtual Asset Custodian Framework**")
st.markdown("*Comprehensive methodology for calculating, maintaining, and monitoring capital adequacy*")

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")
st.sidebar.markdown("*Enter your business parameters to calculate capital requirements*")

# Company Information
with st.sidebar.expander("🏢 Company Information", expanded=True):
    company_name = st.text_input("Company Name", value="AdmiPlatform Ltd.")
    service_type = st.selectbox("Service Type", ["Custody Provider"])
    calculation_date = st.date_input("Calculation Date", value=datetime.now().date())
    st.markdown("**Note:** *This calculator is configured specifically for Virtual Asset Custody Services*")

# Business Projections
with st.sidebar.expander("📊 Business Projections", expanded=True):
    st.markdown("**Select Projection Year**")
    projection_year = st.selectbox("Projection Year", ["Year 1 (2025)", "Year 2 (2026)", "Year 3 (2027)"])
    
    # Pre-populated data from P&L
    financial_data = {
        "Year 1 (2025)": {
            "custody_revenue": 766431,
            "total_aum": 557480000,
            "fixed_overheads_monthly": 282474,
            "cash_equivalents": 854369
        },
        "Year 2 (2026)": {
            "custody_revenue": 1761258,
            "total_aum": 1474200000,
            "fixed_overheads_monthly": 597529,
            "cash_equivalents": 11286899
        },
        "Year 3 (2027)": {
            "custody_revenue": 4754602,
            "total_aum": 2882200000,
            "fixed_overheads_monthly": 624668,
            "cash_equivalents": 20126629
        }
    }
    
    selected_data = financial_data[projection_year]
    
    st.markdown("**Assets Under Custody (AUC) - Auto-populated from P&L**")
    total_auc_eur = st.number_input("Total AUC (EUR)", value=float(selected_data["total_aum"]), step=1000000.0)
    eur_to_usd_rate = st.number_input("EUR to USD Exchange Rate", min_value=1.0, max_value=1.5, value=1.08, step=0.01)
    total_auc = total_auc_eur * eur_to_usd_rate
    
    st.write(f"**Total AUC (USD): ${total_auc:,.0f}**")
    
    # Asset breakdown
    st.markdown("**Asset Allocation (%)**")
    btc_pct = st.slider("Bitcoin %", 0, 100, 40)
    eth_pct = st.slider("Ethereum %", 0, 100, 35)
    other_pct = 100 - btc_pct - eth_pct
    st.write(f"Other Assets: {other_pct}%")
    
    aum_btc = total_auc * (btc_pct / 100)
    aum_eth = total_auc * (eth_pct / 100)
    aum_other = total_auc * (other_pct / 100)

# Fixed Overheads
with st.sidebar.expander("💸 Fixed Overheads (From P&L Projections)", expanded=True):
    monthly_fixed_overheads_eur = selected_data["fixed_overheads_monthly"]
    monthly_fixed_overheads = monthly_fixed_overheads_eur * eur_to_usd_rate
    
    st.markdown("**Fixed Overheads - AdmiPlatform Specific**")
    st.write(f"Monthly Fixed Overheads (EUR): €{monthly_fixed_overheads_eur:,.0f}")
    st.write(f"Monthly Fixed Overheads (USD): ${monthly_fixed_overheads:,.0f}")
    
    st.markdown("**Components include:**")
    st.write("• Salaries for permanent staff recharged to Cayman entity")
    st.write("• Software licenses and subscription fees") 
    st.write("• Insurance premiums")
    st.write("• Professional fees (legal, audit, compliance)")
    st.write("• Essential IT infrastructure and maintenance costs")
    st.write("• Marketing and administrative expenses")

# Risk Parameters
with st.sidebar.expander("⚠️ Risk Parameters - AdmiPlatform Framework", expanded=True):
    st.markdown("**Risk-Based Capital (RBC) Components**")
    st.write("RBC = OpCC + MCC + CrCC + LiCC")
    
    st.markdown("**a. Operational Capital Charge (OpCC)**")
    op_risk_weight = st.slider("OpRisk Weight - AUC (%)", 
                              min_value=0.1, max_value=3.0, value=2.0, step=0.1,
                              help="Applied to AUC for cybersecurity, key management, fraud risks")
    op_risk_factor = st.slider("OpRisk Factor - Fixed Overheads", 
                              min_value=1.0, max_value=2.5, value=1.5, step=0.1,
                              help="Multiplier for cost overruns, remediation expenses")
    
    st.markdown("**b. Market Capital Charge (MCC)**")
    volatility_factor = st.slider("Volatility Factor (%)", 
                                 min_value=10.0, max_value=60.0, value=40.0, step=5.0,
                                 help="Based on 12+ months historical data, VaR methodology")
    
    st.markdown("**c. Credit Capital Charge (CrCC)**")
    counterparty_risk_weight = st.slider("Counterparty Risk Weight (%)", 
                                        min_value=0.5, max_value=3.0, value=1.0, step=0.1,
                                        help="Banking partners, service providers exposure")
    
    st.markdown("**d. Liquidity Capital Charge (LiCC)**")
    liquidity_factor = st.slider("Liquidity Factor (%)", 
                                min_value=10.0, max_value=40.0, value=25.0, step=5.0,
                                help="30-day stress scenario buffer")

# Capital Holdings
with st.sidebar.expander("🏦 Capital Holdings (From Balance Sheet)", expanded=True):
    st.markdown("**Current Capital Position**")
    
    # Auto-populate from balance sheet data
    if projection_year == "Year 1 (2025)":
        total_equity = 6810634 * eur_to_usd_rate
    elif projection_year == "Year 2 (2026)":
        total_equity = 20515638 * eur_to_usd_rate
    else:  # Year 3 (2027)
        total_equity = 29509237 * eur_to_usd_rate
    
    st.write(f"**Total Equity (from Balance Sheet): ${total_equity:,.0f}**")
    
    tier1_capital = st.number_input("Tier 1 Capital (USD)", value=float(max(0, total_equity)), step=50000.0)
    tier2_capital = st.number_input("Tier 2 Capital (USD)", min_value=0.0, value=0.0, step=50000.0)
    
    va_capital_holdings = st.number_input("Company's Own Crypto Holdings (USD)", 
                                         min_value=0.0, value=50000.0, step=10000.0)
    
    counterparty_exposure = st.number_input("Banking/Counterparty Exposure (USD)", 
                                          min_value=0.0, 
                                          value=float(selected_data["cash_equivalents"] * eur_to_usd_rate), 
                                          step=10000.0)
    
    projected_monthly_withdrawals = total_aum * 0.05
    projected_cash_outflow = st.number_input("30-Day Projected Cash Outflow (USD)", 
                                            min_value=0.0, 
                                            value=float(projected_monthly_withdrawals), 
                                            step=10000.0)

# Main calculation area
col1, col2 = st.columns([2, 1])

with col1:
    # Business Context
    st.header("📊 AdmiPlatform Business Overview")
    
    projected_revenue = selected_data["custody_revenue"] * eur_to_usd_rate
    revenue_margin = (projected_revenue / total_aum) * 100 if total_aum > 0 else 0
    
    col_context1, col_context2 = st.columns(2)
    with col_context1:
        st.metric("Projected Custody Revenue", f"${projected_revenue:,.0f}")
        st.metric("Revenue Margin (bps)", f"{revenue_margin*100:.0f} bps")
    
    with col_context2:
        st.metric("Assets Under Custody", f"${total_aum:,.0f}")
        st.metric("Monthly Operating Expenses", f"${monthly_fixed_overheads:,.0f}")
    
    # Risk-Based Capital Calculation
    st.header("📈 Risk-Based Capital (RBC) Calculation")
    
    # Calculate components
    op_aum_charge = total_aum * (op_risk_weight / 100)
    op_overhead_charge = monthly_fixed_overheads * op_risk_factor
    operational_capital_charge = op_aum_charge + op_overhead_charge
    
    market_capital_charge = va_capital_holdings * (volatility_factor / 100)
    credit_capital_charge = counterparty_exposure * (counterparty_risk_weight / 100)
    liquidity_capital_charge = projected_cash_outflow * (liquidity_factor / 100)
    
    total_rbc = operational_capital_charge + market_capital_charge + credit_capital_charge + liquidity_capital_charge
    fixed_overheads_capital = monthly_fixed_overheads * 6
    capital_requirement = max(total_rbc, fixed_overheads_capital)
    
    total_eligible_capital = tier1_capital + tier2_capital
    capital_adequacy_ratio = (total_eligible_capital / capital_requirement) * 100 if capital_requirement > 0 else 0
    
    # Display breakdown
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
    
    rbc_components = pd.DataFrame({
        'Component': ['Operational (AUM)', 'Operational (Overheads)', 'Market', 'Credit', 'Liquidity'],
        'Amount': [op_aum_charge, op_overhead_charge, market_capital_charge, credit_capital_charge, liquidity_capital_charge]
    })
    
    st.write("**Risk-Based Capital Components:**")
    st.bar_chart(rbc_components.set_index('Component')['Amount'])
    
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
    
    st.markdown(f'<div class="{status_color}"><strong>{status_text}</strong><br>{status_message}</div>', 
                unsafe_allow_html=True)
    
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
    
    # Stress Testing
    st.subheader("🧪 Stress Testing")
    
    stress_scenarios = {
        "Market Crash (30% AUM decline)": {"aum_decline": 0.3, "type": "aum"},
        "Crypto Bear Market (60% volatility)": {"volatility": 0.6, "type": "volatility"}, 
        "Mass Custody Withdrawals (3x outflow)": {"cash_multiplier": 3, "type": "liquidity"},
        "Operational Incident (2x overhead costs)": {"overhead_multiplier": 2, "type": "operational"}
    }
    
    for scenario, params in stress_scenarios.items():
        if params["type"] == "aum":
            stressed_aum = total_aum * (1 - params["aum_decline"])
            stressed_rbc = (stressed_aum * (op_risk_weight / 100) + op_overhead_charge + 
                           market_capital_charge + credit_capital_charge + liquidity_capital_charge)
        elif params["type"] == "volatility":
            stressed_rbc = (op_aum_charge + op_overhead_charge + 
                           va_capital_holdings * params["volatility"] + credit_capital_charge + liquidity_capital_charge)
        elif params["type"] == "liquidity":
            stressed_rbc = (op_aum_charge + op_overhead_charge + market_capital_charge + 
                           credit_capital_charge + projected_cash_outflow * params["cash_multiplier"] * (liquidity_factor / 100))
        else:  # operational
            stressed_overhead_charge = monthly_fixed_overheads * op_risk_factor * params["overhead_multiplier"]
            stressed_rbc = (op_aum_charge + stressed_overhead_charge + market_capital_charge + 
                           credit_capital_charge + liquidity_capital_charge)
        
        stressed_requirement = max(stressed_rbc, fixed_overheads_capital)
        stressed_ratio = (total_eligible_capital / stressed_requirement) * 100
        
        st.write(f"**{scenario}**")
        st.write(f"Stressed CAR: {stressed_ratio:.1f}%")
        
        if stressed_ratio >= 100:
            st.write("✅ Would remain compliant")
        else:
            additional_capital_needed = stressed_requirement - total_eligible_capital
            st.write(f"❌ Would breach requirements")
            st.write(f"Additional capital needed: ${additional_capital_needed:,.0f}")
        st.write("---")

# Regulatory Framework Compliance
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

# Report Generation
st.header("📄 Report Generation")

if st.button("Generate Capital Adequacy Report", type="primary"):
    report_data = {
        "Company": company_name,
        "Calculation Date": calculation_date.strftime("%Y-%m-%d"),
        "Projection Year": projection_year,
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
