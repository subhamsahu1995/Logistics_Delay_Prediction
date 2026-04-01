import streamlit as st
import pandas as pd
import numpy as np
import joblib
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Delay Predictor", page_icon="📦")

st.title("📦 Delivery Delay Predictor")

# Load model
@st.cache_resource
def load_model():
    try:
        model = joblib.load("model_new.pkl")
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

model = load_model()

if model is None:
    st.stop()

# Function to reset form values
def set_ontime_values():
    st.session_state['sales'] = 75.0
    st.session_state['quantity'] = 1
    st.session_state['discount'] = 5.0
    st.session_state['discount_rate'] = 0.07
    st.session_state['profit_ratio'] = 0.25
    st.session_state['latitude'] = 40.7128
    st.session_state['longitude'] = -74.0060
    st.session_state['is_weekend'] = 0
    st.session_state['is_holiday'] = 0
    st.session_state['payment_type'] = "DEBIT"
    st.session_state['customer_segment'] = "Consumer"
    st.session_state['shipping_mode'] = "Standard Class"
    st.session_state['order_region'] = "East of USA"
    st.session_state['predict_clicked'] = True

def set_delayed_values():
    st.session_state['sales'] = 850.0
    st.session_state['quantity'] = 5
    st.session_state['discount'] = 0.0
    st.session_state['discount_rate'] = 0.0
    st.session_state['profit_ratio'] = 0.45
    st.session_state['latitude'] = -23.5505
    st.session_state['longitude'] = -46.6333
    st.session_state['is_weekend'] = 1
    st.session_state['is_holiday'] = 1
    st.session_state['payment_type'] = "TRANSFER"
    st.session_state['customer_segment'] = "Corporate"
    st.session_state['shipping_mode'] = "Same Day"
    st.session_state['order_region'] = "South America"
    st.session_state['predict_clicked'] = True

# Sample buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("⚠️ DELAYED Example", use_container_width=True):
        set_ontime_values()
        st.rerun()
with col2:
    if st.button("✅ ON TIME Example", use_container_width=True):
        set_delayed_values()
        st.rerun()

# Initialize session state defaults
if 'sales' not in st.session_state:
    st.session_state['sales'] = 100.0
if 'quantity' not in st.session_state:
    st.session_state['quantity'] = 1
if 'discount' not in st.session_state:
    st.session_state['discount'] = 0.0
if 'discount_rate' not in st.session_state:
    st.session_state['discount_rate'] = 0.0
if 'profit_ratio' not in st.session_state:
    st.session_state['profit_ratio'] = 0.25
if 'latitude' not in st.session_state:
    st.session_state['latitude'] = 40.7128
if 'longitude' not in st.session_state:
    st.session_state['longitude'] = -74.0060
if 'is_weekend' not in st.session_state:
    st.session_state['is_weekend'] = 0
if 'is_holiday' not in st.session_state:
    st.session_state['is_holiday'] = 0
if 'payment_type' not in st.session_state:
    st.session_state['payment_type'] = "DEBIT"
if 'customer_segment' not in st.session_state:
    st.session_state['customer_segment'] = "Consumer"
if 'shipping_mode' not in st.session_state:
    st.session_state['shipping_mode'] = "Standard Class"
if 'order_region' not in st.session_state:
    st.session_state['order_region'] = "East of USA"
if 'predict_clicked' not in st.session_state:
    st.session_state['predict_clicked'] = False

# Form
with st.form("prediction_form"):
    st.subheader("Order Details")
    
    left, right = st.columns(2)
    
    with left:
        # Dropdowns
        payment_type = st.selectbox(
            "Payment Type", 
            ["DEBIT", "PAYMENT", "TRANSFER", "CASH"],
            index=["DEBIT", "PAYMENT", "TRANSFER", "CASH"].index(st.session_state['payment_type'])
        )
        
        customer_segment = st.selectbox(
            "Customer Segment", 
            ["Consumer", "Corporate", "Home Office"],
            index=["Consumer", "Corporate", "Home Office"].index(st.session_state['customer_segment'])
        )
        
        shipping_mode = st.selectbox(
            "Shipping Mode", 
            ["Standard Class", "Second Class", "First Class", "Same Day"],
            index=["Standard Class", "Second Class", "First Class", "Same Day"].index(st.session_state['shipping_mode'])
        )
        
        order_region = st.selectbox(
            "Order Region", 
            ["East of USA", "West of USA", "Western Europe", "Central America", "South America", "Southeast Asia"],
            index=["East of USA", "West of USA", "Western Europe", "Central America", "South America", "Southeast Asia"].index(st.session_state['order_region'])
        )
        
        # Sliders
        sales = st.slider(
            "Sales ($)", 
            min_value=0.0, 
            max_value=1000.0, 
            value=st.session_state['sales'],
            step=10.0
        )
        
        quantity = st.slider(
            "Quantity", 
            min_value=1, 
            max_value=20, 
            value=st.session_state['quantity'],
            step=1
        )
    
    with right:
        # Sliders
        discount = st.slider(
            "Discount ($)", 
            min_value=0.0, 
            max_value=200.0, 
            value=st.session_state['discount'],
            step=5.0
        )
        
        discount_rate = st.slider(
            "Discount Rate", 
            min_value=0.0, 
            max_value=0.5, 
            value=st.session_state['discount_rate'],
            step=0.01,
            format="%.2f"
        )
        
        profit_ratio = st.slider(
            "Profit Ratio", 
            min_value=0.0, 
            max_value=0.8, 
            value=st.session_state['profit_ratio'],
            step=0.01,
            format="%.2f"
        )
        
        latitude = st.number_input(
            "Latitude", 
            value=st.session_state['latitude'],
            format="%.4f"
        )
        
        longitude = st.number_input(
            "Longitude", 
            value=st.session_state['longitude'],
            format="%.4f"
        )
        
        is_weekend = st.selectbox(
            "Weekend?", 
            [0, 1], 
            format_func=lambda x: "Yes" if x == 1 else "No",
            index=st.session_state['is_weekend']
        )
        
        is_holiday = st.selectbox(
            "Holiday Season?", 
            [0, 1], 
            format_func=lambda x: "Yes" if x == 1 else "No",
            index=st.session_state['is_holiday']
        )
    
    # Calculate derived fields
    discount_impact = discount * quantity
    profit_per_order = sales * profit_ratio
    high_value = 1 if sales > 100 else 0
    bulk_order = 1 if quantity > 3 else 0
    weekend_express = 1 if (is_weekend == 1 and shipping_mode == "Same Day") else 0
    
    submitted = st.form_submit_button("🔮 Predict", type="primary", use_container_width=True)

# Make prediction when form submitted OR sample button clicked
if submitted or st.session_state.get('predict_clicked', False):
    # Reset predict_clicked
    if st.session_state.get('predict_clicked', False):
        st.session_state['predict_clicked'] = False
    
    # Create input data
    input_data = pd.DataFrame([{
        'sales_per_customer': sales,
        'latitude': latitude,
        'longitude': longitude,
        'order_item_discount': discount,
        'order_item_discount_rate': discount_rate,
        'order_item_profit_ratio': profit_ratio,
        'order_item_quantity': quantity,
        'order_profit_per_order': profit_per_order,
        'is_weekend': is_weekend,
        'is_holiday_season': is_holiday,
        'discount_impact': discount_impact,
        'weekend_express': weekend_express,
        'high_value_order': high_value,
        'bulk_order': bulk_order,
        'payment_type': payment_type,
        'shipping_mode': shipping_mode,
        'order_region': order_region,
        'customer_segment': customer_segment
    }])
    
    try:
        pred = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1] * 100  # Convert to percentage
        
        st.markdown("---")
        st.subheader("📊 Prediction Result")
        
        # Display result
        if pred == 0:
            st.success(f"### ✅ ON TIME")
            st.balloons()
        else:
            st.error(f"### ⚠️ DELAYED")
            st.snow()
        
        st.metric("Delay Probability", f"{prob:.1f}%")
        
        # Risk level based on your specified ranges
        if prob <= 20:
            st.success("🟢 **Low Risk of Delay** - Normal processing")
        elif prob <= 38:
            st.info("🔵 **Medium Risk** - Monitor shipment")
        elif prob <= 50:
            st.warning("🟡 **High Risk** - Take action")
        elif prob <= 80:
            st.error("🔴 **Very High Risk** - Immediate action required")
        else:
            st.error("💀 **Critical Risk** - Urgent intervention needed")
            
    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Powered by XGBoost")