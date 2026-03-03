import pandas as pd
from sqlalchemy import create_engine, URL, text
from dotenv import load_dotenv
import os

load_dotenv()

# Load CSV
df = pd.read_csv("../data/Telco-Customer-Churn.csv")

# Fix TotalCharges
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df.dropna(subset=["TotalCharges"], inplace=True)
print(f"Rows after cleaning: {len(df)}")

# Connect to Neon PostgreSQL
connection_url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=5432,
    database=os.getenv("DB_NAME"),
    query={"sslmode": "require"}
)
engine = create_engine(connection_url)

# Drop tables in correct order
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS subscriptions CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS plans CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS customers CASCADE"))
    conn.commit()
print("Old tables dropped!")

# ── Load customers table ──
customers = df[["customerID", "gender", "SeniorCitizen",
                "Partner", "Dependents", "tenure"]].copy()
customers.columns = ["customer_id", "gender",
                     "senior_citizen", "partner", "dependents", "tenure"]
customers.to_sql("customers", engine, if_exists="replace", index=False)
print("customers table loaded!")

# ── Load plans table ──
plans = df[["Contract", "PaymentMethod",
            "MonthlyCharges", "TotalCharges"]].copy()
plans.columns = ["contract", "payment_method",
                 "monthly_charges", "total_charges"]
plans = plans.drop_duplicates().reset_index(drop=True)
plans.insert(0, "plan_id", range(1, len(plans)+1))
plans.to_sql("plans", engine, if_exists="replace", index=False)
print("plans table loaded!")

# ── Load subscriptions table ──
df_merged = df.merge(plans, left_on=["Contract", "PaymentMethod", "MonthlyCharges", "TotalCharges"],
                     right_on=["contract", "payment_method", "monthly_charges", "total_charges"])

subs = df_merged[["customerID", "plan_id", "PhoneService", "InternetService",
                  "StreamingTV", "StreamingMovies", "Churn"]].copy()
subs.columns = ["customer_id", "plan_id", "phone_service", "internet_service",
                "streaming_tv", "streaming_movies", "churn"]
subs.reset_index(drop=True, inplace=True)
subs.insert(0, "subscription_id", range(1, len(subs)+1))
subs.to_sql("subscriptions", engine, if_exists="replace", index=False)
print("subscriptions table loaded!")

print("\nAll done! All 3 tables loaded into Neon PostgreSQL!")
