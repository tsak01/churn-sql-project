# 📊 Telco Customer Churn — SQL & Analytics Project

## Business Problem
A telecom company is losing 26.58% of its customers every year.
This project analyzes 7,000+ customers to find why they're leaving
and how much revenue is at risk.

## 🛠️ Tools Used
- PostgreSQL — database design & SQL analytics
- Python (pandas, SQLAlchemy) — data cleaning & loading
- Streamlit — live interactive dashboard
- Git & GitHub — version control

## 🔑 Key SQL Techniques
- Aggregations with GROUP BY
- Multi-table JOINs across 3 tables
- CASE WHEN for churn rate calculation & risk scoring
- Subqueries for derived metrics

## 📈 Key Insights
- Overall churn rate is **26.58%**
- Month-to-month customers churn at **42.71%** vs **2.85%** for two-year contracts
- Company loses **$139,131 every month** due to churn
- **931 high-risk customers** identified for immediate retention action
- Two-year contract customers have **2.4x higher lifetime value**

## 📁 Project Structure
```
churn-sql-project/
├── data/        → raw dataset
├── sql/         → database schema & analytics queries
├── python/      → data exploration & loading scripts
├── app/         → Streamlit dashboard
├── README.md
└── requirements.txt
```

## 🚀 Live Dashboard
(https://tsak01-churn-sql-project.streamlit.app/)

## 💻 Run Locally
```bash
# Clone the repo
git clone https://github.com/yourusername/churn-sql-project

# Install dependencies
pip install -r requirements.txt

# Run dashboard
cd app
streamlit run streamlit_app.py
```
