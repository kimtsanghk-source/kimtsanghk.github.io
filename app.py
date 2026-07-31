import streamlit as st
import pandas as pd

st.set_page_config(page_title="每月數據儀表板", layout="wide")
st.title("每月營運數據更新儀表板")

uploaded_file = st.file_uploader("請上傳最新的 Excel 檔案 (.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    # 讀取 Excel
    df = pd.read_excel(uploaded_file)
    st.success("檔案上傳成功！最新數據已更新：")

    # 1. 整理年月標籤 (例如將 2025 與 Nov 組合成 "2025 Nov")
    if '年份' in df.columns and '月份' in df.columns:
        df['年月'] = df['年份'].astype(str) + " " + df['月份'].astype(str)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("數據預覽")
        st.dataframe(df, use_container_width=True)

    with col2:
        st.subheader("總訂單數量趨勢圖")
        # 2. 自動繪製真實欄位 (以 '年月' 為 X 軸，'總訂單數量' 為 Y 軸)
        if '年月' in df.columns and '總訂單數量' in df.columns:
            # 剔除 None / 空值，只畫有數據的月份 (如 Jul ~ Nov)
            df_chart = df.dropna(subset=['總訂單數量'])
            st.line_chart(df_chart.set_index('年月')['總訂單數量'])
        else:
            st.warning("找不到『總訂單數量』欄位，請檢查 Excel 表頭。")

    # 3. 自動提取「最新一個月份（Nov）」的 KPI 數據，給下方的 Dashboard 使用
    # 填補 None 並抓取最後一行非空的數據
    valid_df = df.dropna(subset=['總訂單數量'])
    if not valid_df.empty:
        latest_row = valid_df.iloc[-1]  # 取得最新的一行 (2025 Nov)
        
        latest_month = latest_row['年月']
        latest_orders = latest_row['總訂單數量']
        latest_hours = latest_row['總配送時間(小時)'] if '總配送時間(小時)' in df.columns else "N/A"
        latest_eff = latest_row['每小時配送效率(訂單)'] if '每小時配送效率(訂單)' in df.columns else "N/A"

        st.markdown("---")
        st.subheader(f"🚀 動態指標展示 (最新數據月份：{latest_month})")
        
        # 用 Streamlit 原生漂亮卡片替換下方寫死的 Dashboard
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("MONTHLY TOTAL ORDERS", f"{latest_orders:,}")
        kpi2.metric("DELIVERY EFFICIENCY", f"{latest_eff} ORDERS/HR")
        kpi3.metric("TOTAL OPERATION HOURS", f"{latest_hours:,} HRS")
