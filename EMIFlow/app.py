import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="EMIFlow", layout="centered")

st.title("💰 EMIFlow - Loan EMI Calculator")

st.sidebar.header("Loan Details")

# Inputs
principal = st.sidebar.number_input("Loan Amount (₹)", min_value=1000, max_value=10000000, step=1000, value=500000)
rate = st.sidebar.slider("Annual Interest Rate (%)", 1.0, 20.0, 8.5, step=0.1)
years = st.sidebar.slider("Loan Tenure (Years)", 1, 30, 10)

# Calculations
monthly_rate = rate / (12 * 100)
months = years * 12

emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
total_payment = emi * months
total_interest = total_payment - principal

# Display Results
st.subheader("📊 Loan Summary")
st.write(f"**Monthly EMI:** ₹{emi:,.2f}")
st.write(f"**Total Interest Payable:** ₹{total_interest:,.2f}")
st.write(f"**Total Payment (Principal + Interest):** ₹{total_payment:,.2f}")

# Plot EMI Breakdown
labels = ['Principal Amount', 'Total Interest']
sizes = [principal, total_interest]
colors = ['#4CAF50', '#F44336']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
ax.axis('equal')
st.pyplot(fig)

# Payment Schedule Table
st.subheader("📅 Payment Schedule (Yearly Overview)")

schedule = []
balance = principal

for year in range(1, years + 1):
    interest_paid = 0
    principal_paid = 0
    for _ in range(12):
        interest = balance * monthly_rate
        principal_component = emi - interest
        balance -= principal_component
        interest_paid += interest
        principal_paid += principal_component
    schedule.append([year, round(principal_paid), round(interest_paid), round(balance)])

df_schedule = pd.DataFrame(schedule, columns=["Year", "Principal Paid", "Interest Paid", "Balance Remaining"])
st.dataframe(df_schedule)
