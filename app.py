import streamlit as st
import extra_streamlit_components as stx
import math
import time

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Syariah Stock Calc", page_icon="💾", layout="centered")

# --- Inisialisasi Cookie Manager ---
# Ini adalah "jembatan" untuk menyimpan data di browser user
cookie_manager = stx.CookieManager()

# --- Fungsi Helper untuk Load/Save ---
def get_cookie_value(key, default_val):
    val = cookie_manager.get(key)
    if val is None:
        return default_val
    return float(val)

# --- Logika Perhitungan ---
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

# --- UI Header ---
st.title("💾 Syariah Stock Calc")
st.caption("Pengaturan Anda akan tersimpan otomatis (Auto-Save)")
st.markdown("---")

# --- Mengambil Data dari Cookies (atau Default) ---
# Kita perlu 'st.spinner' sebentar karena membaca cookies butuh waktu sepersekian detik
val_price = get_cookie_value("c_price", 1000.0)
val_lot = get_cookie_value("c_lot", 10.0)
val_fee_buy = get_cookie_value("c_fee_buy", 0.15)
val_fee_sell = get_cookie_value("c_fee_sell", 0.25)
val_target = get_cookie_value("c_target", 2.0)

# --- Input Form ---
col1, col2 = st.columns(2)

with col1:
    price = st.number_input("Harga Beli (Price)", min_value=50.0, value=val_price, step=5.0)
    lot = st.number_input("Jumlah Lot", min_value=1.0, value=val_lot, step=1.0)

with col2:
    fee_buy = st.number_input("Fee Beli (%)", value=val_fee_buy, step=0.01, format="%.2f")
    fee_sell = st.number_input("Fee Jual (%)", value=val_fee_sell, step=0.01, format="%.2f")

target = st.number_input("Target Profit (%)", value=val_target, step=0.5)

# --- Tombol Hitung & Simpan ---
if st.button("HITUNG & SIMPAN PREFERENSI", use_container_width=True):
    # 1. Simpan nilai terbaru ke Cookies (browser user)
    cookie_manager.set("c_price", price)
    cookie_manager.set("c_lot", lot)
    cookie_manager.set("c_fee_buy", fee_buy)
    cookie_manager.set("c_fee_sell", fee_sell)
    cookie_manager.set("c_target", target)
    
    # 2. Lakukan Perhitungan
    total_buy, avg, bep, sell_target = calculate_sharia_trading(price, lot, fee_buy, fee_sell, target)
    
    st.success("Data dihitung & Preferensi disimpan!")
    
    # 3. Tampilkan Hasil
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric(label="Total Modal (Rp)", value=f"{total_buy:,.0f}")
        st.metric(label="Break Even Point (BEP)", value=f"{bep}")
        
    with res_col2:
        st.metric(label="Harga Rata-rata (Avg)", value=f"{avg:,.2f}")
        st.metric(label=f"Target Jual ({target}%)", value=f"{sell_target}", delta=f"{sell_target-int(price)}")
