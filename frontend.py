import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import (
    load_data,
    clean_data,
    basic_analysis,
    generate_insights,
    suggest_visualizations,
    agent_analyze
)


st.set_page_config(page_title="Autonomous Data Analyst", layout="wide")

st.title("📊 Autonomous Data Analyst Agent")


uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Raw Data")
    st.dataframe(df.head())
    cleaned_df = clean_data(df)

    st.subheader("🧹 Cleaned Data")
    st.dataframe(cleaned_df.head())
    analysis = basic_analysis(cleaned_df)

    st.subheader("📈 Basic Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Shape:**", analysis["shape"])
        st.write("**Columns:**", analysis["columns"])

    with col2:
        st.write("**Null Values:**")
        st.json(analysis["null_counts"])
    st.subheader("🤖 Agent Analysis")

    if st.button("Run Autonomous Analysis"):
        with st.spinner("Agent is analyzing..."):
            plan = agent_analyze(cleaned_df)

            st.write("### 🧠 Agent Plan")
            st.json(plan)
            st.subheader("📊 Auto Generated Charts")

            for viz in plan.get("visualizations", []):
                fig, ax = plt.subplots()

                try:
                    if viz["type"] == "histogram":
                        cleaned_df[viz["column"]].hist(ax=ax)

                    elif viz["type"] == "bar":
                        cleaned_df[viz["column"]].value_counts().plot(kind='bar', ax=ax)

                    elif viz["type"] == "scatter":
                        ax.scatter(
                            cleaned_df[viz["x"]],
                            cleaned_df[viz["y"]]
                        )
                        ax.set_xlabel(viz["x"])
                        ax.set_ylabel(viz["y"])

                    st.pyplot(fig)

                except Exception as e:
                    st.write(f"⚠️ Chart error: {e}")
            st.subheader("🧠 AI Insights")
            insights = generate_insights(cleaned_df)
            st.write(insights)