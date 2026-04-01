# 🚚 Logistics Delay Prediction App

## 📌 Project Overview
This project predicts whether a shipment/order will be **delayed or not delayed** using a Machine Learning model.

Link: https://logisticsdelayprediction-mqzuldejym3lcqfaowtrea.streamlit.app/

It uses:
- Feature engineering (business-driven)
- XGBoost model
- Streamlit for web deployment

---

## 🎯 Objective
To help logistics teams:
- Identify high-risk orders
- Take preventive actions
- Improve delivery performance

---

## 🧠 Model Details
- Model: XGBoost Classifier
- Pipeline:
  - StandardScaler (numerical features)
  - OneHotEncoder (categorical features)
- Target:
  - `0` → No Delay
  - `1` → Delay

---

## 📊 Features Used

### 🔢 Numerical Features
- sales_per_customer
- latitude
- longitude
- order_item_discount
- order_item_discount_rate
- order_item_profit_ratio
- order_item_quantity
- order_profit_per_order
- is_weekend
- is_holiday_season
- discount_impact
- weekend_express
- high_value_order
- bulk_order

### 🔤 Categorical Features
- payment_type
- shipping_mode
- order_region
- customer_segment

---

## ⚙️ Feature Engineering
- Weekend detection from order date
- Holiday season identification
- Discount impact calculation
- Bulk order detection
- High-value order flag
- Weekend express combination

---

## 🖥️ Web App (Streamlit)
The app allows users to:
- Enter order details using sliders and dropdowns
- Automatically compute derived features
- Predict delay risk
- Get confidence score and explanation

---

## ▶️ Run Locally

### 1. Create virtual environment
```bash
python -m venv venv
