import streamlit as st
import pandas as pd

# 設定頁面寬度與標題
st.set_page_config(page_title="數據儀表板", layout="wide")
st.title("每月營運數據更新儀表板")

# 1. 建立 Excel 上傳按鈕
uploaded_file = st.file_uploader("請上傳最新的 Excel 檔案 (.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        # 讀取上傳的 Excel 檔案
        df = pd.read_excel(uploaded_file)
        
        st.success("檔案上傳成功！最新數據已更新：")
        
        # 建立兩欄版面：左邊放數據表格，右邊放圖表
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("數據預覽")
            st.dataframe(df, use_container_width=True)
            
        with col2:
            st.subheader("數據趨勢圖")
            # 假設 Excel 內有 '月份' 與 '銷售額' 兩個欄位
            if '月份' in df.columns and '銷售額' in df.columns:
                st.line_chart(df.set_index('月份')['銷售額'])
            else:
                st.info("請確保 Excel 包含 '月份' 與 '銷售額' 欄位以自動繪製圖表")
                
    except Exception as e:
        st.error(f"檔案解析失敗：{e}")
else:
    st.info("💡 請點擊上方按鈕上傳本月 Excel 檔案以刷新資料。")