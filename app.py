# Here is some starter code to get the data:
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.datasets import fetch_openml

@st.cache_data
def get_data():
    titanic_sklearn = fetch_openml('titanic', version = 1, as_frame = True)
    titanic_df = titanic_sklearn.frame
    return titanic_df

titanic_df = get_data()

st.title("Titanic Stats and Info")

# Age Distribution
tab_male, tab_female, tab_overall = st.tabs(['Male', "Female", "Overall"])

with tab_overall:
    fig = px.histogram(titanic_df, x="age", title="Overall Age Distribution", labels={"age": "Age"})
    fig.update_layout(yaxis_title="Count")
    st.plotly_chart(fig)

with tab_female:
    female_df = titanic_df[(titanic_df['sex'] == 'female')]
    # female_non_survivors = titanic_df[(titanic_df['sex'] == 'female') & (titanic_df['survived'] == "0")]
    fig = px.histogram(female_df, x="age", title="Age Distribution of Female Passengers", labels={"age": "Age"})
    fig.update_layout(yaxis_title="Count")
    st.plotly_chart(fig)

with tab_male:
    male_df = titanic_df[(titanic_df['sex'] == 'male')]
    # male_non_survivors = titanic_df[(titanic_df['sex'] == 'male') & (titanic_df['survived'] == "0")]
    fig = px.histogram(male_df, x="age", title="Age Distribution of Male Passengers", labels={"age": "Age"})
    fig.update_layout(yaxis_title="Count")
    st.plotly_chart(fig)

# Mean Fare Calculator
st.header("Mean Fare Calculator")

left, right = st.columns(2)

with left:
    gender_filter = st.radio("Select Gender", ["Male", "Female"])
with right:
    survived_filter = st.radio("Select Survival Status", ["Survived", "Died"])

if survived_filter == "Survived":
    filtered_df = titanic_df[(titanic_df['sex'] == gender_filter.lower()) & (titanic_df['survived'] == "1")]
else:
    filtered_df = titanic_df[(titanic_df['sex'] == gender_filter.lower()) & (titanic_df['survived'] == "0")]

mean_fare = filtered_df['fare'].mean()

st.write(f"The mean fare for {gender_filter.lower()} passengers who {survived_filter.lower()} was: ${mean_fare:.2f}")

# Dataframe Filter
st.header("Filter Data by Age")

slider_value = st.slider('Age', min_value = 0,
                            max_value= 80,
                            value = 0)

n_rows = int(st.text_input(f'Display how many rows of people with age {slider_value}?', value = 5))

df_age = titanic_df[(np.floor(titanic_df['age']) == slider_value)].sort_values(by='name').reset_index(drop=True)

st.dataframe(df_age.head(n_rows))