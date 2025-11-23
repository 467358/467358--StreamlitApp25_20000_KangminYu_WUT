
# 数据清洗与特征工程函数
import pandas as pd
import numpy as np

def clean_and_engineer_features(df: pd.DataFrame) -> pd.DataFrame:
	"""
	对原始数据进行清洗和特征工程：
	- 统一列名
	- 替换缺失值
	- 时间处理
	- 类型转换
	- 新特征生成
	"""
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True).str.lower()
	df = df.replace(['Unknown', 'unknown', 'na', '-1', 'Other'], np.nan)
	if 'time' in df.columns:
		df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
		df['hour'] = df['time'].apply(lambda x: x.hour if pd.notna(x) else np.nan)
	if 'day_of_week' in df.columns:
		df['day_of_week'] = pd.Categorical(
			df['day_of_week'], 
			categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
			ordered=True
		)
	if 'accident_severity' in df.columns:
		df['accident_severity'] = pd.Categorical(
			df['accident_severity'], 
			categories=['Slight Injury', 'Serious Injury', 'Fatal Injury'], 
			ordered=True
		)
	if 'number_of_casualties' in df.columns:
		df['casualty_count'] = pd.to_numeric(df['number_of_casualties'], errors='coerce')
	AGE_BANDS = ['Under 18', '18-30', '31-50', 'Over 51']
	if 'age_band_of_driver' in df.columns:
		df['age_band_of_driver'] = pd.Categorical(df['age_band_of_driver'], categories=AGE_BANDS, ordered=True)
	EDU_LEVELS = ['Illiterate', 'Elementary school', 'Junior high school', 'High school graduate', 'Above high school', 'College & above']
	if 'educational_level' in df.columns:
		df['educational_level'] = pd.Categorical(df['educational_level'], categories=EDU_LEVELS, ordered=True)
	return df
