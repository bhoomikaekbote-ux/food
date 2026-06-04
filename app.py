import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Food Habits Analytics",
    page_icon="🍔",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("food_data.csv")
    df.columns = df.columns.str.strip().str.lower()
    return df

df = load_data()

st.title("Food Habits Analytics Dashboard")
st.write(df.head())
