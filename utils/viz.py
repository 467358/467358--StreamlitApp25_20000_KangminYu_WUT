import streamlit as st

def draw_chart(chart, title):
	"""
	统一风格的Altair图表展示函数。
	:param chart: Altair图表对象
	:param title: 图表标题
	"""
	chart = chart.properties(title=title).interactive()
	st.altair_chart(chart, use_container_width=True)
