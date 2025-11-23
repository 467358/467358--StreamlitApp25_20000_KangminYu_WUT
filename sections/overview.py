import streamlit as st

def show(df):
    st.header("KPI & High-Level Trends")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accidents (Filtered)", f"{len(df):,}")
    avg_casualties = df['casualty_count'].mean() if 'casualty_count' in df else 0
    col2.metric("Avg Casualties per Accident", f"{avg_casualties:.2f}")
    critical_rate = (len(df[df['accident_severity'].isin(['Serious Injury', 'Fatal Injury'])]) / len(df) * 100) if len(df) > 0 and 'accident_severity' in df else 0
    col3.metric("Severe/Fatal Accident Rate", f"{critical_rate:.1f}%")
    st.markdown("---")
