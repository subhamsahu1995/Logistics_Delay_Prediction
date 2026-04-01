from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

st.title("🚚 Logistics Delay Prediction")

st.info("💡 Tip: High discount + Same Day shipping + weekend orders increase delay risk")

st.markdown("### 📦 Enter Order Details")

# -------- USER INPUTS --------

# Numeric inputs (with ranges)
sales_per_customer = st.slider("Sales per Customer", 0, 2000, 300)

latitude = st.number_input("Latitude", value=40.0)
longitude = st.number_input("Longitude", value=-73.0)

order_item_discount = st.slider("Discount Amount", 0, 500, 10)
order_item_discount_rate = st.slider("Discount Rate", 0.0, 1.0, 0.1)

order_item_profit_ratio = st.slider("Profit Ratio", 0.0, 1.0, 0.2)

order_item_quantity = st.slider("Quantity", 1, 10, 2)

order_profit_per_order = st.slider("Profit per Order", -100, 500, 50)

# Date input instead of manual flags
order_date = st.date_input("Order Date")

# Categorical inputs
payment_type = st.selectbox("Payment Type", ["DEBIT", "TRANSFER", "PAYMENT", "CASH"])

shipping_mode = st.selectbox(
    "Shipping Mode",
    ["Standard Class", "Second Class", "First Class", "Same Day"]
)

order_region = st.selectbox(
    "Order Region",
    [
        "Western Europe", "Central America", "South America",
        "Northern Europe", "Oceania", "Southeast Asia",
        "Caribbean", "East of USA", "West of USA", "Others"
    ]
)

customer_segment = st.selectbox(
    "Customer Segment",
    ["Consumer", "Corporate", "Home Office"]
)

# -------- AUTO FEATURE ENGINEERING --------

# Weekend
day_of_week = order_date.weekday()
is_weekend = 1 if day_of_week >= 5 else 0

# Holiday season
month = order_date.month
is_holiday_season = 1 if month in [11, 12] else 0

# Discount impact
discount_impact = order_item_discount * order_item_quantity

# Weekend express
weekend_express = 1 if (is_weekend == 1 and shipping_mode == "Same Day") else 0

# High value order
high_value_order = 1 if sales_per_customer > 500 else 0

# Bulk order
bulk_order = 1 if order_item_quantity > 3 else 0

# -------- CREATE INPUT DATA --------

input_data = pd.DataFrame({
    'sales_per_customer': [sales_per_customer],
    'latitude': [latitude],
    'longitude': [longitude],
    'order_item_discount': [order_item_discount],
    'order_item_discount_rate': [order_item_discount_rate],
    'order_item_profit_ratio': [order_item_profit_ratio],
    'order_item_quantity': [order_item_quantity],
    'order_profit_per_order': [order_profit_per_order],
    'is_weekend': [is_weekend],
    'is_holiday_season': [is_holiday_season],
    'discount_impact': [discount_impact],
    'weekend_express': [weekend_express],
    'high_value_order': [high_value_order],
    'bulk_order': [bulk_order],
    'payment_type': [payment_type],
    'shipping_mode': [shipping_mode],
    'order_region': [order_region],
    'customer_segment': [customer_segment]
})

# -------- PREDICTION --------

if st.button("Predict Delay"):

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    st.subheader("📊 Result")

    if prediction == 1:
        st.error(f"⚠️ Delay Expected (Confidence: {probability:.2f})")

        st.write("### 🔍 Possible Reasons:")
        if order_item_discount > 50:
            st.write("- High discount applied")
        if order_item_quantity > 3:
            st.write("- Large order size")
        if shipping_mode == "Same Day":
            st.write("- Express shipping pressure")
        if is_weekend == 1:
            st.write("- Weekend order")

    else:
        st.success(f"✅ No Delay Expected (Confidence: {1 - probability:.2f})")