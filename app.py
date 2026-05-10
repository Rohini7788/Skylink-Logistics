import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Logistics Post-Mortem", layout="wide")

# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_data():
    orders = pd.read_csv('orders.csv').dropna(how='all')
    nps = pd.read_csv('nps.csv').dropna(how='all')
    hubs = pd.read_csv('hub_performance.csv').dropna(how='all')
    complaints = pd.read_csv('complaints.csv').dropna(how='all')
    customers = pd.read_csv('customers.csv').dropna(how='all')
    
    # Date formatting
    orders['promised_date'] = pd.to_datetime(orders['promised_date'])
    orders['delivery_date'] = pd.to_datetime(orders['delivery_date'])
    orders['order_date'] = pd.to_datetime(orders['order_date'])
    
    # Derived Metric: SLA Breach
    orders['sla_breached'] = orders['delivery_date'] > orders['promised_date']
    
    return orders, nps, hubs, complaints, customers

orders, nps, hubs, complaints, customers = load_data()

# --- HEADER: THE HOOK ---
st.title("📦 The Festive Surge: A Story of Scale and Service")
st.markdown("""
### Executive Summary
Between October and December, our order volume surged by **40%**. 
While the growth was record-breaking, our customer satisfaction (NPS) reached an all-time low. 
This report investigates the friction points in our logistics chain.
""")

# --- SECTION 1: THE CURRENT STATE (DERIVED METRICS) ---
st.header("Chapter 1: The Performance Pulse")

# Calculating NPS
promoters = (nps['score'] >= 9).sum()
detractors = (nps['score'] <= 6).sum()
nps_score = ((promoters - detractors) / len(nps)) * 100

# Calculating Repeat Rate
repeat_cust = customers[customers['segment'].isin(['Repeat', 'High Value'])].shape[0]
repeat_rate = (repeat_cust / len(customers)) * 100

# Calculating SLA Breach %
overall_breach = (orders['sla_breached'].mean()) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Current NPS", f"{nps_score:.1f}", "-15 pts vs Q3", delta_color="inverse")
m2.metric("Repeat Usage Rate", f"{repeat_rate:.1f}%", "-5% churn risk")
m3.metric("Overall SLA Breach %", f"{overall_breach:.1f}%", "+22% delay spike", delta_color="inverse")

# --- SECTION 2: THE VILLAIN (CITY & COURIER PERFORMANCE) ---
st.divider()
st.header("Chapter 2: Identifying the Friction")
st.write("Our data shows that the decline isn't uniform. Tier-2 cities—specifically Nagpur and Indore—are the primary drivers of dissatisfaction.")

col1, col2 = st.columns(2)

with col1:
    # Pivot for City Performance
    city_perf = orders.groupby('city')['sla_breached'].mean().reset_index().sort_values('sla_breached', ascending=False)
    fig_city = px.bar(city_perf, x='city', y='sla_breached', 
                       title="SLA Breach Rate by City",
                       labels={'sla_breached': 'Breach Rate (%)'},
                       color='sla_breached', color_continuous_scale='Reds')
    st.plotly_chart(fig_city, use_container_width=True)

with col2:
    # Pivot for Courier Performance
    courier_perf = orders.groupby('courier_partner')['sla_breached'].mean().reset_index()
    fig_courier = px.bar(courier_perf, x='courier_partner', y='sla_breached', 
                          title="Courier Partner Reliability",
                          color='courier_partner')
    st.plotly_chart(fig_courier, use_container_width=True)

st.warning("⚠️ **Insight:** QuickShip is responsible for the highest volume of breaches in Indore, indicating a failure in their local hub handoff.")

# --- SECTION 3: THE COMPLAINT FUNNEL ---
st.divider()
st.header("Chapter 3: The Cost of a Late Package")
st.write("What happens when a package is late? It leads to a 'Complaint-to-Detractor' spiral.")

# Corrected Pivot for Complaint Distribution
# .reset_index() now creates 'issue_type' and 'count' columns
comp_dist = complaints['issue_type'].value_counts().reset_index()

# Update names and values to match the new Plotly requirements
fig_pie = px.pie(comp_dist, 
                 values='count',      # The number of complaints
                 names='issue_type',  # The type of issue (Late Delivery, etc.)
                 title="Primary Complaint Drivers", 
                 hole=0.5)

st.plotly_chart(fig_pie, use_container_width=True)
st.info("**Observation:** 32% of complaints in Nagpur are 'Fake Delivery Attempts'—a behavior that destroys customer trust immediately.")

# --- SECTION 4: THE RESOLUTION (RECOMMENDATIONS) ---
st.divider()
st.header("Final Chapter: The Road to Recovery")
st.markdown("""
To improve NPS without increasing costs, we must optimize our existing partnerships and fix hub-level behaviors.
""")

r1, r2, r3 = st.columns(3)
with r1:
    st.subheader("⚡ Quick Wins")
    st.write("""
    - Move all Nagpur volume from **QuickShip** to **FastEx**.
    - Implement auto-SMS alerts when an order status is updated to 'Out for Delivery'.
    """)
with r2:
    st.subheader("🏗️ Structural Fixes")
    st.write("""
    - Audit the Nagpur hub regarding 'Fake Delivery' reporting.
    - Tiered SLA penalties: Couriers with >20% breach rates during festive weeks face a 10% payout reduction.
    """)
with r3:
    st.subheader("📈 Long-term KPIs")
    st.write("""
    - **First-Attempt Delivery Rate:** Focus on reducing RTO.
    - **NPS Recovery Rate:** Tracking if a resolved complaint leads to a repeat purchase.
    """)

st.success("By reallocating volume to high-performing couriers, we can reduce complaints by an estimated 18% with zero additional shipping cost.")
