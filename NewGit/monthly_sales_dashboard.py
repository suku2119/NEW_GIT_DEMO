import streamlit as st
import pandas as pd

st.title("📊 Monthly Sales Dashboard")

# Sample data input
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May"],
    "Sales": [100000, 150000, 120000, 180000, 200000]
}

df = pd.DataFrame(data)

# Editable table
df = st.data_editor(df, num_rows="dynamic")

# Metrics
total_sales = df["Sales"].sum()
avg_sales = df["Sales"].mean()

st.metric("Total Sales", f"₹{total_sales}")
st.metric("Average Sales", f"₹{avg_sales:.2f}")

# Chart
st.line_chart(df.set_index("Month"))