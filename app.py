import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

DATA_PATH = 'RTA Dataset.csv'
ACCIDENT_SEVERITY_ORDER = ['Slight Injury', 'Serious Injury', 'Fatal Injury']
CRITICAL_SEVERITY = ['Serious Injury', 'Fatal Injury']

st.set_page_config(
    page_title="RTA Dashboard: Granular Multi-Dimensional Accident Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(show_spinner="Loading and preparing data...")
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
        categories=ACCIDENT_SEVERITY_ORDER, 
        ordered=True
    )

    df['hour'] = df['time'].apply(lambda x: x.hour if pd.notna(x) else np.nan)

    df['casualty_count'] = pd.to_numeric(df['number_of_casualties'], errors='coerce')

    AGE_BANDS = ['Under 18', '18-30', '31-50', 'Over 51']
    df['age_band_of_driver'] = pd.Categorical(df['age_band_of_driver'], categories=AGE_BANDS, ordered=True)
    
    EDU_LEVELS = ['Illiterate', 'Elementary school', 'Junior high school', 'High school graduate', 'Above high school', 'College & above']
    df['educational_level'] = pd.Categorical(df['educational_level'], categories=EDU_LEVELS, ordered=True)
    
    return df

def draw_chart(chart, title):
    """Utility function to display charts with consistent styling."""
    chart = chart.properties(title=title).interactive()
    st.altair_chart(chart, use_container_width=True)

df_data = load_data(DATA_PATH)

with st.sidebar:

    st.image("微信图片_20251123203603_26_25.jpg", width=100) 
    st.image("微信图片_20251123203604_27_25.jpg", width=100) 
    st.markdown("---")
    
    st.title("Data Filters")
    
    st.header("1. Accident Severity")
    selected_severity = st.multiselect(
        "Severity Levels to Focus On:",
        options=ACCIDENT_SEVERITY_ORDER,
        default=ACCIDENT_SEVERITY_ORDER,
        help="Select severity levels to include in charts and KPIs."
    )
    
    st.header("2. Geographical Filter")
    areas = df_data['area_accident_occured'].dropna().unique().tolist()
    selected_areas = st.multiselect(
        "Filter by Accident Area:",
        options=areas,
        default=areas
    )
    
    st.markdown("---")
    st.markdown(
        """
        #EFREIDataStoriesWUT2025  
        **Kangmin Yu** | kangmin.yu@efrei.net
        """
    )

df_filtered = df_data[
    (df_data['accident_severity'].isin(selected_severity)) &
    (df_data['area_accident_occured'].isin(selected_areas))
].copy()

st.title("RTA Dashboard: Road Traffic Accident Multi-Dimensional Analysis")
st.caption("Project Overview: Visualization and analysis of Ethiopian Road Traffic Accident (RTA) data across five customized analytical themes.")
st.markdown("---")

st.header("1. 🚨 Project Narrative: From Problem to Analysis Framework")
st.markdown("---")

st.subheader("The Problem: The Silent Crisis on Ethiopian Roads")
st.error(
    """
    Road Traffic Accidents (RTAs) pose a critical public health and economic challenge globally, and particularly in developing nations. Ethiopia faces an alarming rate of severe accidents and fatalities. Traditional accident reports often focus only on aggregate counts, failing to provide the granular, multi-dimensional insights necessary for effective policy intervention. **The core problem is the lack of actionable intelligence**—policymakers need to understand *who*, *when*, *where*, and *why* the most dangerous accidents occur.
    """
)

st.subheader("The Data Solution: Why This Dataset?")
st.info(
    """
    This **Ethiopian Road Traffic Accident Dataset** was specifically selected because of its rich, interconnected variables that go beyond simple time/location data. It contains crucial **driver characteristics** (Age, Education, Experience), **environmental factors** (Weather, Road Surface), **behavioral causes** (`Cause_of_accident`), and detailed **severity** outcomes. This allows for a shift from simple counting to **causal and predictive analysis**.

    This project utilizes five analytical dimensions to convert raw data into targeted insights (Analysis Phase):
    
    * **Geographic Risk:** Where are the high-risk zones?
    * **Temporal Patterns:** When are the high-risk hours/days?
    * **Causal Factors:** Which driver actions and conditions lead to accidents?
    * **Collision Mechanics:** Which collision types are most lethal?
    * **Driver Demographics:** Which driver profiles are most vulnerable or dangerous?
    """
)
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Total Accidents (Filtered)", f"{len(df_filtered):,}")
col2.metric("Avg Casualties per Accident", f"{df_filtered['casualty_count'].mean():.2f}")
critical_rate = (len(df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)]) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
col3.metric("Severe/Fatal Accident Rate", f"{critical_rate:.1f}%")

st.markdown("---")

st.header("2. 🗺️ Geographic Accident Comparison ")
st.info("Objective: Identify high-risk geographical areas and analyze their primary collision characteristics.")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Geographic Distribution of Accidents by Severity")
    area_agg_severity = df_filtered.groupby(['area_accident_occured', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(area_agg_severity).mark_circle(opacity=0.8).encode(
        x=alt.X('accident_severity', title='Accident Severity', sort=ACCIDENT_SEVERITY_ORDER),
        y=alt.Y('area_accident_occured', title='Accident Area Occurred', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        size=alt.Size('count', title='Accident Count', scale=alt.Scale(range=[50, 600])),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
        tooltip=['area_accident_occured', 'accident_severity', 'count']
    ).properties(title="Area Accident Severity Distribution")
    draw_chart(chart, "Area Accident Severity Distribution")

with col2:
    st.subheader("Major Collision Type Distribution by Area")
    area_collision_agg = df_filtered.groupby(['area_accident_occured', 'type_of_collision'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(area_collision_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='Collision Type Proportion'),
        y=alt.Y('area_accident_occured', title='Accident Area Occurred', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('type_of_collision', title='Collision Type', scale=alt.Scale(scheme='category10')),
        tooltip=['area_accident_occured', 'type_of_collision', alt.Tooltip('count', format=',')]
    ).properties(title="Area Collision Type Proportion")
    draw_chart(chart, "Major Collision Type Distribution by Area")

st.markdown("---")


st.header("3. ⏱️ Temporal Accident Analysis")
st.info("Objective: Determine high-risk time windows within a day and observe the temporal changes in collision types.")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Hourly Accident Count and Severity Trend")
    time_severity_agg = df_filtered.groupby(['hour', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(time_severity_agg).mark_line(point=True).encode(
        x=alt.X('hour', title='Hour of Day'),
        y=alt.Y('count', title='Accident Count'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
        tooltip=['hour', 'accident_severity', 'count']
    ).properties(title="Accident Trends Grouped by Hour and Severity")
    draw_chart(chart, "Hourly Accident Count and Severity Trend")

with col2:
    st.subheader("Collision Type Distribution Across Different Hours")
    time_collision_agg = df_filtered.groupby(['hour', 'type_of_collision'], observed=True).size().reset_index(name='count')
    
    top_collisions = time_collision_agg.groupby('type_of_collision')['count'].sum().nlargest(5).index.tolist()
    time_collision_agg = time_collision_agg[time_collision_agg['type_of_collision'].isin(top_collisions)]

    chart = alt.Chart(time_collision_agg).mark_bar().encode(
        x=alt.X('type_of_collision', title='Collision Type'),
        y=alt.Y('count', title='Accident Count'),
        column=alt.Column('hour', header=alt.Header(titleOrient="bottom"), title='Hour'),
        color=alt.Color('type_of_collision', title='Collision Type', scale=alt.Scale(scheme='category10')),
        tooltip=['hour', 'type_of_collision', 'count']
    ).properties(title="Collision Type Distribution by Hour (Top 5)")
    draw_chart(chart, "Collision Type Distribution by Hour (Grouped Bar Chart)")
    
st.markdown("---")

st.header("4.Factor Analysis: Contributing Factors")
st.info("Objective: Examine the impact of driver personal factors, environmental conditions (weather/road), and driving behavior on accident frequency and severity.")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Driver Personal Features and Severe Accident Count")
    
    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()
    
    st.markdown("##### Severe Accident Count by Age Band")
    age_agg = df_severe.groupby('age_band_of_driver', observed=True).size().reset_index(name='Severe_Count')
    chart_age = alt.Chart(age_agg).mark_bar(color='#E34C31').encode(
        x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
        y=alt.Y('age_band_of_driver', title='Age Band', sort=None),
        tooltip=['age_band_of_driver', 'Severe_Count']
    )
    draw_chart(chart_age, "Severe Accident Count by Age Band")

    st.markdown("##### Severe Accident Count by Driving Experience")
    exp_agg = df_severe.groupby('driving_experience', observed=True).size().reset_index(name='Severe_Count')
    chart_exp = alt.Chart(exp_agg).mark_bar(color='#CC6633').encode(
        x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
        y=alt.Y('driving_experience', title='Driving Experience', sort=None),
        tooltip=['driving_experience', 'Severe_Count']
    )
    draw_chart(chart_exp, "Severe Accident Count by Driving Experience")
    
    st.markdown("##### Severe Accident Count by Sex")
    sex_agg = df_severe.groupby('sex_of_driver', observed=True).size().reset_index(name='Severe_Count')
    chart_sex = alt.Chart(sex_agg).mark_bar(color='#943E2C').encode(
        x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
        y=alt.Y('sex_of_driver', title='Driver Sex', sort=None),
        tooltip=['sex_of_driver', 'Severe_Count']
    )
    draw_chart(chart_sex, "Severe Accident Count by Driver Sex")

with col2:
    st.subheader("Impact of Weather and Road Surface Combination")
    weather_surface_agg = df_filtered.groupby(['weather_conditions', 'road_surface_type'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(weather_surface_agg).mark_rect().encode(
        x=alt.X('road_surface_type', title='Road Surface Type'),
        y=alt.Y('weather_conditions', title='Weather Condition'),
        color=alt.Color('count', scale=alt.Scale(range='heatmap'), title='Accident Count'),
        tooltip=['road_surface_type', 'weather_conditions', 'count']
    ).properties(title="Accident Heatmap: Weather vs. Road Surface")
    draw_chart(chart, "Impact of Weather and Road Surface Combination")

with col3:
    st.subheader("Driver Behavior and Accident Severity Proportion")
    
    behavior_severity_agg = df_filtered.groupby(['cause_of_accident', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    total_by_cause = behavior_severity_agg.groupby('cause_of_accident')['count'].sum()
    top_10_causes = total_by_cause.nlargest(10).index.tolist()
    
    behavior_severity_agg = behavior_severity_agg[behavior_severity_agg['cause_of_accident'].isin(top_10_causes)].copy()

    chart = alt.Chart(behavior_severity_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='Accident Severity Proportion'),
        y=alt.Y('cause_of_accident', title='Driver Behavior (Top 10 Causes)', 
                sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
        tooltip=['cause_of_accident', 'accident_severity', alt.Tooltip('count', format=',')]
    ).properties(title="Accident Severity Proportion by Driver Behavior")
    draw_chart(chart, "Driver Behavior and Accident Severity Proportion")

st.markdown("---")

st.header("5. 💥 Collision Type and Casualty Relationship")
st.info("Objective: Quantify the frequency, severity, and casualty impact of different collision types (`type_of_collision`).")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Collision Type Frequency (Top 5)")
    collision_counts = df_filtered['type_of_collision'].value_counts().head(5).reset_index(name='Count')
    collision_counts.columns = ['type_of_collision', 'Count']
    
    chart = alt.Chart(collision_counts).mark_arc(outerRadius=120).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="type_of_collision", type="nominal", title='Collision Type', scale=alt.Scale(scheme='category10')),
        order=alt.Order("Count", sort="descending"),
        tooltip=['type_of_collision', alt.Tooltip('Count', format=',')]
    ).properties(title="Top 5 Collision Type Proportion")
    draw_chart(chart, "Collision Type Frequency")

with col2:
    st.subheader("Collision Type vs. Accident Severity Proportion")
    collision_severity_agg = df_filtered.groupby(['type_of_collision', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(collision_severity_agg).mark_bar().encode(
        x=alt.X('count', stack="normalize", title='Accident Proportion'),
        y=alt.Y('type_of_collision', title='Collision Type', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
        tooltip=['type_of_collision', 'accident_severity', alt.Tooltip('count', format=',')]
    ).properties(title="Collision Type and Severity Proportion")
    draw_chart(chart, "Collision Type vs. Accident Severity Proportion")

with col3:
    st.subheader("Impact of Collision Type on Average Casualties")
    
    casualty_agg = df_filtered.groupby('type_of_collision', observed=True)['casualty_count'].agg(
        mean='mean',
        std='std'
    ).reset_index()
    
    casualty_agg['lower_bound'] = casualty_agg['mean'] - casualty_agg['std']
    casualty_agg['upper_bound'] = casualty_agg['mean'] + casualty_agg['std']
    casualty_agg['lower_bound'] = casualty_agg['lower_bound'].apply(lambda x: max(0, x))

    bar = alt.Chart(casualty_agg).mark_bar(color='#4C78A8').encode(
        y=alt.Y('type_of_collision', title='Collision Type', sort='-x'),
        x=alt.X('mean', title='Average Casualties'),
        tooltip=['type_of_collision', alt.Tooltip('mean', format='.2f', title='Average Casualties'), alt.Tooltip('std', format='.2f', title='Standard Deviation')]
    ).properties(title="Collision Type vs. Average Casualties")

    error_bars = alt.Chart(casualty_agg).mark_rule().encode(
        y=alt.Y('type_of_collision', title='Collision Type'),
        x=alt.X('lower_bound', title=''),
        x2='upper_bound'
    )
    
    chart = bar + error_bars
    draw_chart(chart, "Collision Type vs. Average Casualties (Mean + Std Dev)")


st.markdown("---")

st.header("6. 👤 Driver Feature and Accident Severity Correlation")
st.info("Objective: Explore the complex relationship between driver characteristics, suchs as age and education, and accident severity.")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Educational Level and Accident Severity Proportion")
    edu_severity_agg = df_filtered.groupby(['educational_level', 'accident_severity'], observed=True).size().reset_index(name='count')
    
    chart = alt.Chart(edu_severity_agg).mark_bar().encode(
        x=alt.X('educational_level', title='Educational Level', sort=None), 
        y=alt.Y('count', stack="normalize", title='Accident Proportion'),
        color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
        tooltip=['educational_level', 'accident_severity', alt.Tooltip('count', format=',')]
    ).properties(title="Educational Level vs. Accident Severity Proportion")
    draw_chart(chart, "Educational Level vs. Accident Severity Proportion")

with col2:
    st.subheader("Driver Age, Experience, and Severe Accident")

    df_severe = df_filtered[df_filtered['accident_severity'].isin(CRITICAL_SEVERITY)].copy()

    age_exp_agg = df_severe.groupby(['driving_experience', 'age_band_of_driver'], observed=True).size().reset_index(name='Severe_Count')

    chart = alt.Chart(age_exp_agg).mark_rect().encode(
        x=alt.X('driving_experience', title='Driving Experience', sort=None),
        y=alt.Y('age_band_of_driver', title='Age Band', sort=None),
        color=alt.Color('Severe_Count', scale=alt.Scale(range='heatmap'), title='Severe Accident Count'),
        tooltip=['age_band_of_driver', 'driving_experience', 'Severe_Count']
    ).properties(title="Driving Experience vs. Age Band Severe Accident")
    draw_chart(chart, "Driver Age, Experience, and Severe Accident")

st.markdown("---")

st.header("7. 💡 Insights & Next Steps")

st.markdown("""
Based on the in-depth analysis across five dimensions, we can identify key risk factors contributing to severe traffic accidents, providing clear direction for traffic safety policy development.
""")

st.subheader("Key Insights")

st.success(
    """
    **1. Risk Concentration by Area:**
    * **High-risk areas** (`Office areas`, `Residential areas`) show not only high total accident volumes but also a significantly higher proportion of **'Vehicle with vehicle collision'**, suggesting inadequate traffic management and flow in these areas during peak hours.

    **2. Elevated Risk During Evenings and Weekends:**
    * **High-risk periods** concentrate between **17:00 and 20:00**. The proportion of severe accident types like **'Rear-end'** and **'Side collision'** increases during these hours, indicating a combined effect of driver fatigue, impatience, and low light conditions.

    **3. Behavioral Factors as Primary Cause for Severe Casualties:**
    * **Driver Behavior** analysis clearly shows that specific actions (e.g., `No distancing`, `Changing lane to the right`) account for the largest proportion of all accidents and also exhibit the highest **Severe/Fatal Accident Proportion**, confirming that subjective behavioral errors are the most direct cause of severe outcomes.
    * **Personal features** analysis indicates the largest volume of risk is concentrated among **18-30 year-old** and **male** drivers, necessitating targeted public awareness and enforcement.

    **4. High-Risk Collision Types:**
    * The **Average Casualties Bar Chart** highlights that **'Overturning'** and **'Collision with fixed objects'** have the highest average casualties and standard deviation, marking them as high fatality/disability risk types.
    * The **Severity Proportion Stacked Bar Chart** confirms these types have the highest proportion of Severe/Fatal outcomes.

    **5. Focus on Less Educated Drivers:**
    * **Educational Level** analysis reveals that drivers with lower education levels (e.g., `Elementary school`, `Junior high school`) contribute to a high volume of accidents, and their severe accident proportion warrants attention, potentially linked to understanding of traffic laws and risk judgment.
    * The **Age-Experience Heatmap** clearly identifies the combination of **18-30 year-old** drivers with **2-5 years of experience** as the **primary hotspot** for severe accidents, designating young and moderately experienced drivers as the priority target for intervention.
    """
)

st.subheader("Next Steps and Recommendations")

st.markdown(
    """
    Based on the data insights above, we recommend implementing the following three targeted actions:
    
    1.  **🎯 Enforcement and Intervention for High-Risk Behaviors:**
        * **Enforcement Focus:** Shift enforcement from solely speed limits to **dangerous driving behaviors**, such as **`No distancing`** and **improper lane changing**. Utilize automated monitoring systems to specifically identify and penalize these high-risk actions.
        * **Road Deployment:** Install electronic surveillance in high-density areas (e.g., `Office areas`) to monitor frequently occurring **rear-end** and **side collisions**.
        
    2.  **🏗️ Infrastructure and Awareness Optimization for Critical Time Windows:**
        * **Night Illumination:** Prioritize the repair and addition of road lighting to mitigate the **environmental amplification of risk** during nighttime accidents.
        * **Awareness Campaigns:** Traffic safety campaigns should focus on the **17:00 - 20:00** window, reminding drivers of the impact of fatigue and emotion on driving performance.
        
    3.  **📚 Driver Training and Education System Improvement:**
        * **Targeted Training:** Design intensive training programs specifically for the high-risk group of **18-30 year-old drivers with 2-5 years of experience** to enhance their practical risk awareness.
        * **Risk Education:** Incorporate mandatory education on the consequences of high-risk collision types (like **overturning** and **hitting fixed objects**) into driving tests and annual reviews.
        * **Basic Education:** Consider offering free or mandatory **traffic rule reinforcement courses** for drivers with lower educational backgrounds or specific experience ranges to improve their risk identification and avoidance skills.
    """
)

st.markdown("---")
st.markdown("Created for #EFREIDataStoriesWUT2025 | Data Visualization Project")