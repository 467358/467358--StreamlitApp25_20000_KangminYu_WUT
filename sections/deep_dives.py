import streamlit as st
import altair as alt
import numpy as np

ACCIDENT_SEVERITY_ORDER = ['Slight Injury', 'Serious Injury', 'Fatal Injury']
CRITICAL_SEVERITY = ['Serious Injury', 'Fatal Injury']

def show(df):
    st.header("2. 🗺️ Geographic Accident Comparison ")
    st.info("Objective: Identify high-risk geographical areas and analyze their primary collision characteristics.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Geographic Distribution of Accidents by Severity")
        area_agg_severity = df.groupby(['area_accident_occured', 'accident_severity'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(area_agg_severity).mark_circle(opacity=0.8).encode(
            x=alt.X('accident_severity', title='Accident Severity', sort=ACCIDENT_SEVERITY_ORDER),
            y=alt.Y('area_accident_occured', title='Accident Area Occurred', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
            size=alt.Size('count', title='Accident Count', scale=alt.Scale(range=[50, 600])),
            color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
            tooltip=['area_accident_occured', 'accident_severity', 'count']
        ).properties(title="Area Accident Severity Distribution")
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.subheader("Major Collision Type Distribution by Area")
        area_collision_agg = df.groupby(['area_accident_occured', 'type_of_collision'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(area_collision_agg).mark_bar().encode(
            x=alt.X('count', stack="normalize", title='Collision Type Proportion'),
            y=alt.Y('area_accident_occured', title='Accident Area Occurred', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
            color=alt.Color('type_of_collision', title='Collision Type', scale=alt.Scale(scheme='category10')),
            tooltip=['area_accident_occured', 'type_of_collision', alt.Tooltip('count', format=',')]
        ).properties(title="Area Collision Type Proportion")
        st.altair_chart(chart, use_container_width=True)
    st.markdown("---")
    st.header("3. ⏱️ Temporal Accident Analysis")
    st.info("Objective: Determine high-risk time windows within a day and observe the temporal changes in collision types.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Hourly Accident Count and Severity Trend")
        time_severity_agg = df.groupby(['hour', 'accident_severity'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(time_severity_agg).mark_line(point=True).encode(
            x=alt.X('hour', title='Hour of Day'),
            y=alt.Y('count', title='Accident Count'),
            color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
            tooltip=['hour', 'accident_severity', 'count']
        ).properties(title="Accident Trends Grouped by Hour and Severity")
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.subheader("Collision Type Distribution Across Different Hours")
        time_collision_agg = df.groupby(['hour', 'type_of_collision'], observed=True).size().reset_index(name='count')
        top_collisions = time_collision_agg.groupby('type_of_collision')['count'].sum().nlargest(5).index.tolist()
        time_collision_agg = time_collision_agg[time_collision_agg['type_of_collision'].isin(top_collisions)]
        chart = alt.Chart(time_collision_agg).mark_bar().encode(
            x=alt.X('type_of_collision', title='Collision Type'),
            y=alt.Y('count', title='Accident Count'),
            column=alt.Column('hour', header=alt.Header(titleOrient="bottom"), title='Hour'),
            color=alt.Color('type_of_collision', title='Collision Type', scale=alt.Scale(scheme='category10')),
            tooltip=['hour', 'type_of_collision', 'count']
        ).properties(title="Collision Type Distribution by Hour (Top 5)")
        st.altair_chart(chart, use_container_width=True)
    st.markdown("---")
    st.header("4.Factor Analysis: Contributing Factors")
    st.info("Objective: Examine the impact of driver personal factors, environmental conditions (weather/road), and driving behavior on accident frequency and severity.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Driver Personal Features and Severe Accident Count")
        df_severe = df[df['accident_severity'].isin(CRITICAL_SEVERITY)].copy()
        st.markdown("##### Severe Accident Count by Age Band")
        age_agg = df_severe.groupby('age_band_of_driver', observed=True).size().reset_index(name='Severe_Count')
        chart_age = alt.Chart(age_agg).mark_bar(color='#E34C31').encode(
            x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
            y=alt.Y('age_band_of_driver', title='Age Band', sort=None),
            tooltip=['age_band_of_driver', 'Severe_Count']
        )
        st.altair_chart(chart_age, use_container_width=True)
        st.markdown("##### Severe Accident Count by Driving Experience")
        exp_agg = df_severe.groupby('driving_experience', observed=True).size().reset_index(name='Severe_Count')
        chart_exp = alt.Chart(exp_agg).mark_bar(color='#CC6633').encode(
            x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
            y=alt.Y('driving_experience', title='Driving Experience', sort=None),
            tooltip=['driving_experience', 'Severe_Count']
        )
        st.altair_chart(chart_exp, use_container_width=True)
        st.markdown("##### Severe Accident Count by Sex")
        sex_agg = df_severe.groupby('sex_of_driver', observed=True).size().reset_index(name='Severe_Count')
        chart_sex = alt.Chart(sex_agg).mark_bar(color='#943E2C').encode(
            x=alt.X('Severe_Count', title='Severe/Fatal Accident Count'),
            y=alt.Y('sex_of_driver', title='Driver Sex', sort=None),
            tooltip=['sex_of_driver', 'Severe_Count']
        )
        st.altair_chart(chart_sex, use_container_width=True)
    with col2:
        st.subheader("Impact of Weather and Road Surface Combination")
        weather_surface_agg = df.groupby(['weather_conditions', 'road_surface_type'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(weather_surface_agg).mark_rect().encode(
            x=alt.X('road_surface_type', title='Road Surface Type'),
            y=alt.Y('weather_conditions', title='Weather Condition'),
            color=alt.Color('count', scale=alt.Scale(range='heatmap'), title='Accident Count'),
            tooltip=['road_surface_type', 'weather_conditions', 'count']
        ).properties(title="Accident Heatmap: Weather vs. Road Surface")
        st.altair_chart(chart, use_container_width=True)
    with col3:
        st.subheader("Driver Behavior and Accident Severity Proportion")
        behavior_severity_agg = df.groupby(['cause_of_accident', 'accident_severity'], observed=True).size().reset_index(name='count')
        total_by_cause = behavior_severity_agg.groupby('cause_of_accident')['count'].sum()
        top_10_causes = total_by_cause.nlargest(10).index.tolist()
        behavior_severity_agg = behavior_severity_agg[behavior_severity_agg['cause_of_accident'].isin(top_10_causes)].copy()
        chart = alt.Chart(behavior_severity_agg).mark_bar().encode(
            x=alt.X('count', stack="normalize", title='Accident Severity Proportion'),
            y=alt.Y('cause_of_accident', title='Driver Behavior (Top 10 Causes)', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
            color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
            tooltip=['cause_of_accident', 'accident_severity', alt.Tooltip('count', format=',')]
        ).properties(title="Accident Severity Proportion by Driver Behavior")
        st.altair_chart(chart, use_container_width=True)
    st.markdown("---")
    st.header("5. 💥 Collision Type and Casualty Relationship")
    st.info("Objective: Quantify the frequency, severity, and casualty impact of different collision types (`type_of_collision`).")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Collision Type Frequency (Top 5)")
        collision_counts = df['type_of_collision'].value_counts().head(5).reset_index(name='Count')
        collision_counts.columns = ['type_of_collision', 'Count']
        chart = alt.Chart(collision_counts).mark_arc(outerRadius=120).encode(
            theta=alt.Theta(field="Count", type="quantitative"),
            color=alt.Color(field="type_of_collision", type="nominal", title='Collision Type', scale=alt.Scale(scheme='category10')),
            order=alt.Order("Count", sort="descending"),
            tooltip=['type_of_collision', alt.Tooltip('Count', format=',')]
        ).properties(title="Top 5 Collision Type Proportion")
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.subheader("Collision Type vs. Accident Severity Proportion")
        collision_severity_agg = df.groupby(['type_of_collision', 'accident_severity'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(collision_severity_agg).mark_bar().encode(
            x=alt.X('count', stack="normalize", title='Accident Proportion'),
            y=alt.Y('type_of_collision', title='Collision Type', sort=alt.EncodingSortField(field='count', op='sum', order='descending')),
            color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
            tooltip=['type_of_collision', 'accident_severity', alt.Tooltip('count', format=',')]
        ).properties(title="Collision Type and Severity Proportion")
        st.altair_chart(chart, use_container_width=True)
    with col3:
        st.subheader("Impact of Collision Type on Average Casualties")
        casualty_agg = df.groupby('type_of_collision', observed=True)['casualty_count'].agg(
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
        st.altair_chart(chart, use_container_width=True)
    st.markdown("---")
    st.header("6. 👤 Driver Feature and Accident Severity Correlation")
    st.info("Objective: Explore the complex relationship between driver characteristics, suchs as age and education, and accident severity.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Educational Level and Accident Severity Proportion")
        edu_severity_agg = df.groupby(['educational_level', 'accident_severity'], observed=True).size().reset_index(name='count')
        chart = alt.Chart(edu_severity_agg).mark_bar().encode(
            x=alt.X('educational_level', title='Educational Level', sort=None),
            y=alt.Y('count', stack="normalize", title='Accident Proportion'),
            color=alt.Color('accident_severity', scale=alt.Scale(domain=ACCIDENT_SEVERITY_ORDER, range=['#4C78A8', '#E34C31', '#943E2C']), title='Severity'),
            tooltip=['educational_level', 'accident_severity', alt.Tooltip('count', format=',')]
        ).properties(title="Educational Level vs. Accident Severity Proportion")
        st.altair_chart(chart, use_container_width=True)
    with col2:
        st.subheader("Driver Age, Experience, and Severe Accident")
        df_severe = df[df['accident_severity'].isin(CRITICAL_SEVERITY)].copy()
        age_exp_agg = df_severe.groupby(['driving_experience', 'age_band_of_driver'], observed=True).size().reset_index(name='Severe_Count')
        chart = alt.Chart(age_exp_agg).mark_rect().encode(
            x=alt.X('driving_experience', title='Driving Experience', sort=None),
            y=alt.Y('age_band_of_driver', title='Age Band', sort=None),
            color=alt.Color('Severe_Count', scale=alt.Scale(range='heatmap'), title='Severe Accident Count'),
            tooltip=['age_band_of_driver', 'driving_experience', 'Severe_Count']
        ).properties(title="Driving Experience vs. Age Band Severe Accident")
        st.altair_chart(chart, use_container_width=True)
    st.markdown("---")
