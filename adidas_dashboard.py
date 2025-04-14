# # adidas_dashboard.py

# import streamlit as st
# # Set page config
# st.set_page_config(
#     page_title="Adidas Sales Dashboard",
#     page_icon="👟",
#     layout="wide"
# )
# import pandas as pd
# import plotly.express as px
# import time
# from streamlit_lottie import st_lottie
# import json

# # Load your data
# @st.cache_data
# def load_data():
#     df = pd.read_excel("Adidas.xlsx", sheet_name="Sales")
#     df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
#     return df

# df = load_data()

# # Load Lottie animation
# def load_lottie(filepath):
#     with open(filepath, "r") as f:
#         return json.load(f)



# # Header with animation
# st.title("Adidas Sales Performance Dashboard")
# st.markdown("### Powered by Streamlit & Plotly | Interactive Visuals")

# # Sidebar filters
# st.sidebar.header("Filter the Data")

# regions = st.sidebar.multiselect(
#     "Select Region(s)", options=df["Region"].unique(), default=df["Region"].unique()
# )
# states = st.sidebar.multiselect(
#     "Select State(s)", options=df["State"].unique(), default=df["State"].unique()
# )
# products = st.sidebar.multiselect(
#     "Select Product(s)", options=df["Product"].unique(), default=df["Product"].unique()
# )

# start_date, end_date = st.sidebar.date_input(
#     "Select Date Range",
#     [df["InvoiceDate"].min(), df["InvoiceDate"].max()]
# )

# df_filtered = df[
#     (df["Region"].isin(regions)) &
#     (df["State"].isin(states)) &
#     (df["Product"].isin(products)) &
#     (df["InvoiceDate"] >= pd.to_datetime(start_date)) &
#     (df["InvoiceDate"] <= pd.to_datetime(end_date))
# ]

# # KPIs
# total_sales = int(df_filtered["TotalSales"].sum())
# total_units = int(df_filtered["UnitsSold"].sum())
# avg_profit_margin = round(df_filtered["OperatingMargin"].mean() * 100, 2)

# kpi1, kpi2, kpi3 = st.columns(3)
# with kpi1:
#     st.metric(label="Total Sales", value=f"${total_sales:,.0f}")
# with kpi2:
#     st.metric(label="Units Sold", value=f"{total_units:,}")
# with kpi3:
#     st.metric(label="Avg. Profit Margin", value=f"{avg_profit_margin}%")

# st.markdown("---")

# # Sales Over Time
# sales_by_date = df_filtered.groupby("InvoiceDate")["TotalSales"].sum().reset_index()
# fig1 = px.line(sales_by_date, x="InvoiceDate", y="TotalSales", title="Total Sales Over Time")
# fig1.update_layout(margin=dict(l=20, r=20, t=50, b=20))
# st.plotly_chart(fig1, use_container_width=True)

# # Sales by Region
# sales_by_region = df_filtered.groupby("Region")["TotalSales"].sum().reset_index()
# fig2 = px.bar(sales_by_region, x="Region", y="TotalSales", color="Region", title="Sales by Region")
# fig2.update_layout(margin=dict(l=20, r=20, t=50, b=20))
# st.plotly_chart(fig2, use_container_width=True)

# # Product Share
# product_share = df_filtered.groupby("Product")["TotalSales"].sum().reset_index()
# fig3 = px.pie(product_share, values="TotalSales", names="Product", title="Product Sales Share")
# fig3.update_traces(textinfo='percent+label')
# st.plotly_chart(fig3, use_container_width=True)

# # Operating Profit vs. Total Sales
# fig4 = px.scatter(
#     df_filtered,
#     x="TotalSales", y="OperatingProfit",
#     color="Product",
#     size="UnitsSold",
#     hover_data=["Retailer", "City"],
#     title="Operating Profit vs Total Sales"
# )
# fig4.update_layout(margin=dict(l=20, r=20, t=50, b=20))
# st.plotly_chart(fig4, use_container_width=True)

# # Raw Data
# with st.expander("🔍 View Raw Data"):
#     st.dataframe(df_filtered, use_container_width=True)

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: gray;'>"
#     "Built with ❤️ using Streamlit | Adidas Dataset"
#     "</div>", unsafe_allow_html=True
# )



# adidas_dashboard.py

import streamlit as st

# Set page config (MUST be first)
st.set_page_config(
    page_title="Adidas Sales Dashboard",
    page_icon="👟",
    layout="wide"
)

import pandas as pd
import plotly.express as px

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel("Adidas.xlsx", sheet_name="Sales")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# Dashboard title and subtitle
st.title("Adidas Sales Performance Dashboard")
st.markdown("### Powered by Streamlit & Plotly | Interactive Visuals")
st.markdown("---")

# Sidebar filters
st.sidebar.header("Filter the Data")

regions = st.sidebar.multiselect(
    "Select Region(s)", options=df["Region"].unique(), default=list(df["Region"].unique())
)
states = st.sidebar.multiselect(
    "Select State(s)", options=df["State"].unique(), default=list(df["State"].unique())
)
products = st.sidebar.multiselect(
    "Select Product(s)", options=df["Product"].unique(), default=list(df["Product"].unique())
)

# Fix: Ensure date input returns two values
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df["InvoiceDate"].min(), df["InvoiceDate"].max()),
    key="date_range"
)

# Unpack safely
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = df["InvoiceDate"].min()
    end_date = df["InvoiceDate"].max()

# Apply filters
df_filtered = df[
    (df["Region"].isin(regions)) &
    (df["State"].isin(states)) &
    (df["Product"].isin(products)) &
    (df["InvoiceDate"] >= pd.to_datetime(start_date)) &
    (df["InvoiceDate"] <= pd.to_datetime(end_date))
]

# KPIs
total_sales = int(df_filtered["TotalSales"].sum())
total_units = int(df_filtered["UnitsSold"].sum())
avg_profit_margin = round(df_filtered["OperatingMargin"].mean() * 100, 2)

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total Sales", value=f"${total_sales:,.0f}")
with kpi2:
    st.metric(label="Units Sold", value=f"{total_units:,}")
with kpi3:
    st.metric(label="Avg. Profit Margin", value=f"{avg_profit_margin}%")

st.markdown("---")

# Line Chart: Sales Over Time
sales_by_date = df_filtered.groupby("InvoiceDate")["TotalSales"].sum().reset_index()
fig1 = px.line(sales_by_date, x="InvoiceDate", y="TotalSales", title="Total Sales Over Time")
fig1.update_layout(margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig1, use_container_width=True)

# Bar Chart: Sales by Region
sales_by_region = df_filtered.groupby("Region")["TotalSales"].sum().reset_index()
fig2 = px.bar(sales_by_region, x="Region", y="TotalSales", color="Region", title="Sales by Region")
fig2.update_layout(margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig2, use_container_width=True)

# Pie Chart: Product Share
product_share = df_filtered.groupby("Product")["TotalSales"].sum().reset_index()
fig3 = px.pie(product_share, values="TotalSales", names="Product", title="Product Sales Share")
fig3.update_traces(textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)

# Scatter Plot: Profit vs. Sales
fig4 = px.scatter(
    df_filtered,
    x="TotalSales", y="OperatingProfit",
    color="Product",
    size="UnitsSold",
    hover_data=["Retailer", "City"],
    title="Operating Profit vs Total Sales"
)
fig4.update_layout(margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig4, use_container_width=True)

# Raw Data Table
with st.expander("🔍 View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Built with ❤️ using Streamlit | Adidas Dataset"
    "</div>", unsafe_allow_html=True
)
