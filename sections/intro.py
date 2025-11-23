import streamlit as st

def show():
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
        This **Ethiopian Road Traffic Accident Dataset** was specifically selected because of its rich, interconnected variables that go beyond simple time/location data. It contains crucial **driver characteristics** (Age, Education, Experience), **environmental factors** (Weather, Road Surface), **behavioral causes** (`Cause_of_accident`), and detailed **severity** outcomes. This allows for a shift from simple counting to **causal and predictive analysis**.\n\nThis project utilizes five analytical dimensions to convert raw data into targeted insights (Analysis Phase):\n\n* **Geographic Risk:** Where are the high-risk zones?\n* **Temporal Patterns:** When are the high-risk hours/days?\n* **Causal Factors:** Which driver actions and conditions lead to accidents?\n* **Collision Mechanics:** Which collision types are most lethal?\n* **Driver Demographics:** Which driver profiles are most vulnerable or dangerous?
        """
    )
    st.markdown("---")
