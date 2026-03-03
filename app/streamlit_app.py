import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, URL
from dotenv import load_dotenv
import os
load_dotenv()

# ── Page Config ──
st.set_page_config(
    page_title="Telco Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Connection ──


@st.cache_resource
def get_engine():
    connection_url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=5432,
        database=os.getenv("DB_NAME"),
        query={"sslmode": "require"}
    )
    return create_engine(connection_url)


engine = get_engine()

# ── Title ──
st.title("📊 Telco Customer Churn Dashboard")
st.markdown(
    "Analysis of 7,000+ telecom customers to identify churn patterns and revenue risk.")
st.divider()

# ── KPI Cards ──
st.subheader("Key Metrics")

kpi = pd.read_sql("""
    SELECT
        COUNT(*) AS total_customers,
        ROUND(SUM(p.total_charges)::NUMERIC, 2) AS total_revenue,
        SUM(CASE WHEN s.churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
        ROUND(100.0 * SUM(CASE WHEN s.churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate,
        ROUND(SUM(CASE WHEN s.churn = 'Yes' THEN p.monthly_charges ELSE 0 END)::NUMERIC, 2) AS monthly_lost
    FROM subscriptions s
    JOIN plans p ON s.plan_id = p.plan_id
""", engine).iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Customers", f"{int(kpi['total_customers']):,}")
col2.metric("Total Revenue", f"${kpi['total_revenue']:,.0f}")
col3.metric("Churned Customers", f"{int(kpi['churned']):,}")
col4.metric("Churn Rate", f"{kpi['churn_rate']}%")
col5.metric("Monthly Revenue Lost", f"${kpi['monthly_lost']:,.0f}")

st.divider()

# ── Charts Row 1 ──
col6, col7 = st.columns(2)

with col6:
    st.subheader("💰 Revenue by Contract Type")
    rev = pd.read_sql("""
        SELECT contract,
               ROUND(SUM(total_charges)::NUMERIC, 2) AS total_revenue
        FROM plans
        GROUP BY contract
        ORDER BY total_revenue DESC
    """, engine)
    st.bar_chart(rev.set_index("contract"))

with col7:
    st.subheader("📉 Churn Rate by Contract Type")
    churn = pd.read_sql("""
        SELECT p.contract,
               ROUND(100.0 * SUM(CASE WHEN s.churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.plan_id
        GROUP BY p.contract
        ORDER BY churn_rate DESC
    """, engine)
    st.bar_chart(churn.set_index("contract"))

st.divider()

# ── Charts Row 2 ──
col8, col9 = st.columns(2)

with col8:
    st.subheader("⚠️ Customer Risk Segments")
    risk = pd.read_sql("""
        SELECT
            CASE
                WHEN p.contract = 'Month-to-month' AND c.tenure < 12 AND p.monthly_charges > 65 THEN 'High Risk'
                WHEN p.contract = 'Month-to-month' AND c.tenure < 24 THEN 'Medium Risk'
                WHEN p.contract = 'One year' THEN 'Low Risk'
                ELSE 'Very Low Risk'
            END AS risk_segment,
            COUNT(*) AS customers
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.plan_id
        JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY risk_segment
        ORDER BY customers DESC
    """, engine)
    st.bar_chart(risk.set_index("risk_segment"))

with col9:
    st.subheader("📊 Customer Lifetime Value by Contract")
    ltv = pd.read_sql("""
        SELECT p.contract,
               ROUND(AVG(p.total_charges)::NUMERIC, 2) AS avg_ltv
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.plan_id
        JOIN customers c ON s.customer_id = c.customer_id
        WHERE s.churn = 'No'
        GROUP BY p.contract
        ORDER BY avg_ltv DESC
    """, engine)
    st.bar_chart(ltv.set_index("contract"))

st.divider()

# ── Raw Data Table ──
st.subheader("🔍 Explore Raw Data")
sample = pd.read_sql("""
    SELECT c.customer_id, c.tenure, p.contract, p.monthly_charges,
           p.total_charges, s.churn
    FROM subscriptions s
    JOIN plans p ON s.plan_id = p.plan_id
    JOIN customers c ON s.customer_id = c.customer_id
    LIMIT 100
""", engine)
st.dataframe(sample, use_container_width=True)
