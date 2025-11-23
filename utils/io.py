import pandas as pd
import numpy as np
import streamlit as st

def load_data(path: str) -> pd.DataFrame:
	"""Loads the raw dataset, cleans column names, and sets data types."""
	df = pd.read_csv(path)
	df.columns = df.columns.str.replace('[^A-Za-z0-9_]+', '', regex=True).str.lower()
	df = df.replace(['Unknown', 'unknown', 'na', '-1', 'Other'], np.nan)
	df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.time
	df['day_of_week'] = pd.Categorical(
		df['day_of_week'], 
		categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
		ordered=True
	)
	df['accident_severity'] = pd.Categorical(
		df['accident_severity'], 
		categories=['Slight Injury', 'Serious Injury', 'Fatal Injury'], 
		ordered=True
	)
	df['hour'] = df['time'].apply(lambda x: x.hour if pd.notna(x) else np.nan)
	df['casualty_count'] = pd.to_numeric(df['number_of_casualties'], errors='coerce')
	AGE_BANDS = ['Under 18', '18-30', '31-50', 'Over 51']
	df['age_band_of_driver'] = pd.Categorical(df['age_band_of_driver'], categories=AGE_BANDS, ordered=True)
	EDU_LEVELS = ['Illiterate', 'Elementary school', 'Junior high school', 'High school graduate', 'Above high school', 'College & above']
	df['educational_level'] = pd.Categorical(df['educational_level'], categories=EDU_LEVELS, ordered=True)
	return df
