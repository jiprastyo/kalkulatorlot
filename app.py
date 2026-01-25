import streamlit as st
import math

st.set_page_config(page_title="Syariah Stock Calc", page_icon="📈", layout="centered")

def calculate_sharia_trading(price, lot, fee_buy_pct, fee_sell_pct, target_profit_pct):
    shares = lot * 100
    buy_value = price * shares
    buy_fee = buy_value * (fee_buy_pct / 100)
    total_buy_cost = buy_value + buy_fee
    avg_price = total_buy_cost / shares
    
    target_return_val = total_buy_cost * (1 + target_profit_pct / 100)
    required_sell_value = target_return_val / (1 - (fee_sell_pct / 100))
    target_sell_price = math.ceil(required_sell_value / shares)
    
    bep_sell_value = total_buy_cost / (1 - (fee_sell_pct / 100))
    bep_price = math.ceil(bep_sell_value / shares)
    
    return total_buy_cost, avg_price, bep_price, target_sell_price

st.title("📟 Syariah Stock Calc")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    price = st.number_input("Harga Beli (Price)", min_value=50.0, value=1000.0, step=5.0)
    lot = st.number_input("Jumlah Lot", min_value=1.0, value=10.0, step=1.0)
with col2:
    fee_buy = st.number_input("Fee Beli (%)", value=0.15, step=0.01)
    fee_sell = st.number_input("Fee Jual (%)", value=0.25, step=0.01)

target = st.number_input("Target Profit (%)", value=2.0, step=0.5)

if st.button("HITUNG"):
    total_buy, avg, bep, sell_target = calculate_sharia_trading(price, lot, fee_buy, fee_sell, target)
    st.success("Selesai")
    c1, c2 = st.columns(2)
    c1.metric("Total Modal", f"{total_buy:,.0f}")
    c1.metric("BEP", f"{bep}")
    c2.metric("Harga Avg", f"{avg:,.2f}")
    c2.metric("Target Jual", f"{sell_target}")
