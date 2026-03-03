import pandas as pd

# Load the dataset
df = pd.read_csv("../data/Telco-Customer-Churn.csv")

# How many rows and columns?
print("SHAPE:")
print(df.shape)

# What columns do we have?
print("\nCOLUMNS:")
print(df.columns.tolist())

# Any missing values?
print("\nMISSING VALUES:")
print(df.isnull().sum())

# How many churned vs stayed?
print("\nCHURN COUNTS:")
print(df["Churn"].value_counts())

# Churn rate
churn_rate = df["Churn"].value_counts(normalize=True)["Yes"] * 100
print(f"\nChurn Rate: {churn_rate:.1f}%")

# Basic stats
print("\nNUMERIC STATS:")
print(df[["tenure", "MonthlyCharges", "TotalCharges"]].describe())
