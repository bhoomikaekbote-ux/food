import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Food Habits Analytics",
    page_icon="🍔",
    layout="wide"
)

# -------------------------
# LOAD DATA
# -------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("food_data.csv")

    df.columns = df.columns.str.strip().str.lower()

    return df

df = load_data()

# -------------------------
# HEADER
# -------------------------

st.title("🍕 Food Habits & Nutrition Analytics")
st.markdown("Deep Analytics Dashboard")

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.header("Filters")

if "gender" in df.columns:
    gender = st.sidebar.multiselect(
        "Gender",
        df["gender"].unique(),
        default=df["gender"].unique()
    )

    df = df[df["gender"].isin(gender)]

if "gpa" in df.columns:

    gpa_range = st.sidebar.slider(
        "GPA Range",
        float(df["gpa"].min()),
        float(df["gpa"].max()),
        (
            float(df["gpa"].min()),
            float(df["gpa"].max())
        )
    )

    df = df[
        (df["gpa"] >= gpa_range[0]) &
        (df["gpa"] <= gpa_range[1])
    ]

# -------------------------
# KPI CARDS
# -------------------------

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Participants",
        len(df)
    )

with c2:
    if "gpa" in df.columns:
        st.metric(
            "Avg GPA",
            round(df["gpa"].mean(),2)
        )

with c3:
    if "cook" in df.columns:
        st.metric(
            "Cooking Categories",
            df["cook"].nunique()
        )

with c4:
    st.metric(
        "Columns",
        len(df.columns)
    )

st.divider()

tabs = st.tabs([
    "Demographics",
    "Food Analytics",
    "Behavior",
    "Insights"
])

# -------------------------
# DEMOGRAPHICS
# -------------------------

with tabs[0]:

    col1,col2 = st.columns(2)

    if "gender" in df.columns:

        with col1:

            fig = px.pie(
                df,
                names="gender",
                title="Gender Split"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    if "gpa" in df.columns:

        with col2:

            fig = px.histogram(
                df,
                x="gpa",
                nbins=20,
                title="GPA Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

# -------------------------
# FOOD ANALYTICS
# -------------------------

with tabs[1]:

    if "calories_day" in df.columns:

        fig = px.histogram(
            df,
            x="calories_day",
            title="Importance of Calories"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    if "cook" in df.columns:

        fig = px.bar(
            df["cook"]
            .value_counts()
            .reset_index(),
            x="cook",
            y="count",
            title="Cooking Frequency"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# -------------------------
# BEHAVIOR
# -------------------------

with tabs[2]:

    numeric = df.select_dtypes(
        include="number"
    )

    if len(numeric.columns) > 1:

        corr = numeric.corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

# -------------------------
# INSIGHTS
# -------------------------

with tabs[3]:

    st.subheader(
        "Automatic Insights"
    )

    insights = []

    insights.append(
        f"Total Participants: {len(df)}"
    )

    if "gpa" in df.columns:

        insights.append(
            f"Average GPA: {round(df['gpa'].mean(),2)}"
        )

    if "gender" in df.columns:

        insights.append(
            f"Most Common Gender: {df['gender'].mode()[0]}"
        )

    for i in insights:
        st.success(i)

    st.dataframe(df.head(20))
