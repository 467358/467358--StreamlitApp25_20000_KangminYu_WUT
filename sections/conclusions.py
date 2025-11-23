import streamlit as st

def show():
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
