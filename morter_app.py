import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Mortar Plant Dashboard", layout="wide")

# --- Sidebar Inputs ---
st.sidebar.title("🔧 Production Inputs")
tons_produced = st.sidebar.number_input("Today's Output (Tons)", min_value=0.0, value=250.0)
price_per_bag = st.sidebar.number_input("Sale Price per Bag (MAD)", value=24.0)
cost_per_bag = st.sidebar.number_input("Production Cost per Bag (MAD)", value=6.0)

st.sidebar.markdown("---")
st.sidebar.title("🧱 Raw Material Costs (per ton)")
sand_cost = st.sidebar.number_input("Sand Cost", value=80.0)
cement_cost = st.sidebar.number_input("Cement Cost", value=1000.0)
additive_cost = st.sidebar.number_input("Additive Cost", value=3000.0)

# --- Calculations ---
bags_filled = tons_produced * 1000 / 25
profit_per_bag = price_per_bag - cost_per_bag
total_profit = bags_filled * profit_per_bag

# --- Main Dashboard ---
st.title("🏗️ Mortar Production Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("💼 Bags Filled", f"{int(bags_filled):,}")
col2.metric("💸 Profit per Bag", f"{profit_per_bag:.2f} MAD")
col3.metric("📈 Total Daily Profit", f"{total_profit:,.0f} MAD")

# --- Material Usage ---
st.subheader("📦 Raw Material Usage Estimates")

sand_used = tons_produced * 0.8
cement_used = tons_produced * 0.18
additive_used = tons_produced * 0.02

material_df = pd.DataFrame({
    "Material": ["Sand", "Cement", "Additives"],
    "Estimated Tons": [sand_used, cement_used, additive_used],
    "Cost/ton (MAD)": [sand_cost, cement_cost, additive_cost],
    "Total Cost (MAD)": [
        round(sand_used * sand_cost, 0),
        round(cement_used * cement_cost, 0),
        round(additive_used * additive_cost, 0),
    ]
})
st.dataframe(material_df)

# --- QC Logging ---
st.subheader("🧪 Batch Quality Check")
with st.form("qc_form"):
    batch_id = st.text_input("Batch ID")
    water_ratio = st.slider("Water Ratio", 0.10, 0.25, 0.18)
    finish_score = st.slider("Finish Rating", 1, 10, 8)
    notes = st.text_area("Field Notes")
    submitted = st.form_submit_button("📌 Log QC Data")

if submitted:
    st.success(f"Batch {batch_id} QC logged.")
    st.write(f"- Water Ratio: {water_ratio}")
    st.write(f"- Finish Score: {finish_score}/10")
    st.write(f"- Notes: {notes}")

# --- Footer ---
st.caption(f"Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")