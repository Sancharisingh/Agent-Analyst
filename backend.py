"""
Backend module for Autonomous Data Analyst Agent

- Modular functions
- No notebook-style execution
- Each function is independently testable
"""

import pandas as pd
import numpy as np
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=API_KEY)

# -----------------------------------------
# 1. load_data
# -----------------------------------------
def load_data(file_path: str) -> pd.DataFrame:
    """
    Load CSV file into a Pandas DataFrame.

    Args:
        file_path (str): Path to CSV file

    Returns:
        pd.DataFrame
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise Exception(f"[load_data] Error: {e}")


# -----------------------------------------
# 2. clean_data
# -----------------------------------------
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataset by:
    - Removing duplicates
    - Handling missing values
    - Fixing numeric and datetime types

    Args:
        df (pd.DataFrame)

    Returns:
        pd.DataFrame
    """
    df = df.copy()

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    for col in df.columns:
        if df[col].dtype in ["float64", "int64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(
                df[col].mode()[0] if not df[col].mode().empty else "Unknown"
            )

    # Convert numeric-like columns safely
    for col in df.columns:
        try:
            converted = pd.to_numeric(df[col], errors='coerce')
            if converted.notna().sum() > 0:
                df[col] = converted
        except:
            pass

    # Convert datetime-like columns safely
    for col in df.select_dtypes(include=["object", "string"]).columns:
        try:
            converted = pd.to_datetime(df[col], format="%Y-%m-%d", errors='coerce')
            if converted.notna().sum() > 0:
                df[col] = converted
        except:
            pass

    return df


# -----------------------------------------
# 3. basic_analysis
# -----------------------------------------
def basic_analysis(df: pd.DataFrame) -> dict:
    """
    Perform basic analysis:
    - Shape
    - Columns
    - Data types
    - Null counts
    - Summary statistics

    Args:
        df (pd.DataFrame)

    Returns:
        dict
    """
    analysis = {
        "shape": df.shape,
        "columns": df.columns.tolist(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isnull().sum().to_dict(),
        "summary": df.describe(include="all").to_dict()
    }

    return analysis


# -----------------------------------------
# 4. generate_insights
# -----------------------------------------
def generate_insights(df: pd.DataFrame) -> str:
    """
    Generate insights using Gemini API based on dataframe summary.

    Args:
        df (pd.DataFrame)

    Returns:
        str
    """
    try:
        summary = basic_analysis(df)

        prompt = f"""
        You are a senior data analyst.

        Analyze the dataset summary below and generate clear insights.

        {summary}

        Provide:
        - Key trends
        - Important patterns
        - Any anomalies
        - Business insights (if applicable)
        """

        # NOTE: Replace with a valid model from your list_models() output
        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        return f"[generate_insights] Error: {e}"


# -----------------------------------------
# 5. suggest_visualizations
# -----------------------------------------
def suggest_visualizations(df: pd.DataFrame) -> list:
    """
    Suggest visualizations based on column types.

    Args:
        df (pd.DataFrame)

    Returns:
        list
    """
    suggestions = []

    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns

    if len(numeric_cols) > 0:
        suggestions.append("Histogram for numeric distributions")
        suggestions.append("Boxplot for outlier detection")

    if len(categorical_cols) > 0:
        suggestions.append("Bar chart for category counts")

    if len(numeric_cols) >= 2:
        suggestions.append("Correlation heatmap")
        suggestions.append("Scatter plot between numeric variables")

    return suggestions

def agent_analyze(df: pd.DataFrame) -> dict:
    """
    Agent decides:
    - What analysis to run
    - What charts to generate

    Returns structured plan
    """

    summary = basic_analysis(df)

    prompt = f"""
    You are an autonomous data analyst agent.

    Based on this dataset summary:

    {summary}

    Decide:
    1. Key analysis steps
    2. Important columns
    3. Best visualizations

    Output STRICT JSON:
    {{
        "analysis_steps": [],
        "important_columns": [],
        "visualizations": [
            {{"type": "histogram", "column": "col_name"}},
            {{"type": "bar", "column": "col_name"}},
            {{"type": "scatter", "x": "col1", "y": "col2"}}
        ]
    }}
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        import json

        match = re.search(r"\{.*\}", response.text, re.DOTALL)

        if match:
            json_str = match.group()
            plan = json.loads(json_str)
            return plan
        else:
            return {"error": "Invalid JSON from model"}

    except Exception as e:
        return {"error": str(e)}