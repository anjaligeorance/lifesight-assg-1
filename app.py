import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# Load Data
# --------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("final_cleaned_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

channel_df = pd.read_csv("channel_data.csv")
channel_df["date"] = pd.to_datetime(channel_df["date"])


# --------------------------
# KPI Section
# --------------------------
st.title("📊 Marketing Intelligence Dashboard")

total_spend = df["spend"].sum()
total_revenue = df["total_revenue"].sum()
total_profit = df["gross_profit"].sum()
total_orders = df["orders"].sum()
total_customers = df["new_customers"].sum()
roas = df["attributed_revenue"].sum() / total_spend

# KPI Cards
kpi1, kpi2, kpi3 = st.columns(3)
kpi4, kpi5, kpi6 = st.columns(3)

kpi1.metric("💰 Total Spend", f"${total_spend:,.2f}")
kpi2.metric("📈 Total Revenue", f"${total_revenue:,.2f}")
kpi3.metric("🏦 Total Profit", f"${total_profit:,.2f}")

kpi4.metric("🛒 Total Orders", f"{total_orders:,}")
kpi5.metric("👥 New Customers", f"{total_customers:,}")
kpi6.metric("📊 ROAS", f"{roas:.2f}x")

st.markdown("---")

# --------------------------
# Charts
# --------------------------

# Line chart: Revenue vs Spend
fig1 = px.line(df, x="date", y=["total_revenue", "spend"],
               labels={"value": "Amount", "date": "Date"},
               title="Revenue vs Spend Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Line chart: Orders trend
fig2 = px.line(df, x="date", y="orders",
               title="Orders Trend Over Time")
st.plotly_chart(fig2, use_container_width=True)

# Scatter: Spend vs Orders
fig3 = px.scatter(df, x="spend", y="orders",
                  size="clicks", color="total_revenue",
                  hover_data=["new_customers"],
                  title="Spend vs Orders (Bubble size = Clicks, Color = Revenue)")
st.plotly_chart(fig3, use_container_width=True)





# Extra Metrics for Insights

overall_roas = df["attributed_revenue"].sum() / df["spend"].sum()
avg_profit_margin = df["Profit_Margin"].mean()
avg_aov = df["AOV"].mean()

# Detect correlation between spend and orders
corr_spend_orders = df["spend"].corr(df["orders"])



# Insights / Storytelling

st.markdown("## 📖 Insights & Storytelling")

st.markdown(f"""
- **Return on Ad Spend (ROAS):** On average, every $1 spent returns **{overall_roas:.2f}x** in attributed revenue.
- **Average Order Value (AOV):** Customers spend about **${avg_aov:,.2f}** per order.
- **Profit Margin:** Across 120 days, profit margin averages **{avg_profit_margin:.1%}**, showing healthy unit economics.
- **Spend vs Orders:** Marketing spend and orders are correlated at **{corr_spend_orders:.2f}**, meaning higher spend generally leads to more orders, but not perfectly.
- Some days show **high spend with weak profit growth**, suggesting inefficiencies in budget allocation.
""")

