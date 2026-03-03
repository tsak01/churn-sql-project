-- ─────────────────────────────────────────
-- QUERY 1: Total Revenue
-- ─────────────────────────────────────────
SELECT ROUND(SUM(total_charges)::NUMERIC, 2) AS total_revenue
FROM plans;

-- ─────────────────────────────────────────
-- QUERY 2: Revenue by Contract Type
-- ─────────────────────────────────────────
SELECT
    contract,
    COUNT(*) AS customer_count,
    ROUND(SUM(total_charges)::NUMERIC, 2) AS total_revenue,
    ROUND(AVG(monthly_charges)::NUMERIC, 2) AS avg_monthly
FROM plans
GROUP BY contract
ORDER BY total_revenue DESC;

-- ─────────────────────────────────────────
-- QUERY 3: Overall Churn Rate
-- ─────────────────────────────────────────
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(100.0 * SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions;

-- ─────────────────────────────────────────
-- QUERY 4: Churn Rate by Contract Type
-- ─────────────────────────────────────────
SELECT
    p.contract,
    COUNT(*) AS total,
    SUM(CASE WHEN s.churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(100.0 * SUM(CASE WHEN s.churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM subscriptions s
JOIN plans p ON s.plan_id = p.plan_id
GROUP BY p.contract
ORDER BY churn_rate_pct DESC;

-- ─────────────────────────────────────────
-- QUERY 5: Revenue Lost Due to Churn
-- ─────────────────────────────────────────
SELECT
    ROUND(SUM(CASE WHEN s.churn = 'Yes' THEN p.monthly_charges ELSE 0 END)::NUMERIC, 2) AS monthly_revenue_lost,
    ROUND(SUM(CASE WHEN s.churn = 'Yes' THEN p.total_charges ELSE 0 END)::NUMERIC, 2) AS total_revenue_lost
FROM subscriptions s
JOIN plans p ON s.plan_id = p.plan_id;

-- ─────────────────────────────────────────
-- QUERY 6: Customer Lifetime Value (LTV)
-- ─────────────────────────────────────────
SELECT
    p.contract,
    ROUND(AVG(p.total_charges)::NUMERIC, 2) AS avg_ltv,
    ROUND(AVG(c.tenure)::NUMERIC, 1) AS avg_tenure_months,
    ROUND(AVG(p.monthly_charges)::NUMERIC, 2) AS avg_monthly
FROM subscriptions s
JOIN plans p ON s.plan_id = p.plan_id
JOIN customers c ON s.customer_id = c.customer_id
WHERE s.churn = 'No'
GROUP BY p.contract
ORDER BY avg_ltv DESC;

-- ─────────────────────────────────────────
-- QUERY 7: Risk Scoring
-- ─────────────────────────────────────────
SELECT
    risk_segment,
    COUNT(*) AS customer_count
FROM (
    SELECT
        CASE
            WHEN p.contract = 'Month-to-month' AND c.tenure < 12 AND p.monthly_charges > 65 THEN 'High Risk'
            WHEN p.contract = 'Month-to-month' AND c.tenure < 24 THEN 'Medium Risk'
            WHEN p.contract = 'One year' THEN 'Low Risk'
            ELSE 'Very Low Risk'
        END AS risk_segment
    FROM subscriptions s
    JOIN plans p ON s.plan_id = p.plan_id
    JOIN customers c ON s.customer_id = c.customer_id
) risk_table
GROUP BY risk_segment
ORDER BY customer_count DESC;