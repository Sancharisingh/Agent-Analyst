# 📊 Autonomous Data Analyst Agent

🚀 **Live Demo:** https://agentanalyst.streamlit.app/

An AI-powered system that automatically analyzes datasets, generates insights, and creates visualizations — just like a human data analyst.

---

## 🚀 Overview

This project is an **agentic AI system** that:

* Accepts a CSV file
* Cleans and preprocesses data automatically
* Uses an LLM (Google Gemini) to reason about the dataset
* Generates insights
* Creates relevant visualizations

👉 The goal is to simulate a **junior data analyst** that works autonomously.

---

## ✨ Features

* 📂 Upload any CSV dataset
* 🧹 Automatic data cleaning
* 📈 Summary statistics & analysis
* 🤖 AI-generated insights (Gemini API)
* 📊 Auto-generated charts (histogram, bar, scatter, heatmap)
* 🧠 Agent-based decision making (no manual selection required)

---

## 🧠 How It Works

1. **Data Ingestion**

   * User uploads CSV via Streamlit UI

2. **Data Cleaning**

   * Removes duplicates
   * Handles missing values
   * Fixes data types

3. **Analysis**

   * Generates dataset summary using Pandas

4. **Agent Reasoning**

   * LLM analyzes dataset summary
   * Decides:

     * Important columns
     * Relevant visualizations
     * Key insights

5. **Execution**

   * Charts are generated automatically
   * Insights are displayed

---

## 🛠 Tech Stack

* **Language:** Python
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib
* **Frontend:** Streamlit
* **LLM:** Google Gemini API
* **Architecture:** Modular backend + agent layer

---

## 📁 Project Structure

```
project/
│
├── backend.py        # Core logic + agent reasoning
├── frontend.py       # Streamlit UI
├── requirements.txt  # Dependencies
├── .env              # Local API key (not committed)
├── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

---

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add API Key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

---

### 5. Run the app

```bash
streamlit run frontend.py
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub
2. Go to Streamlit Cloud
3. Select repo
4. Set main file:

```
frontend.py
```

5. Add secret:

```toml
GEMINI_API_KEY = "your_api_key"
```

---

## 📸 Demo Flow

1. Upload CSV
2. Click **Run Autonomous Analysis**
3. View:

   * Agent plan
   * Auto-generated charts
   * AI insights

---

## 🧠 Key Concept: Agentic AI

Unlike traditional dashboards, this system:

* **Decides what to analyze**
* **Chooses visualizations**
* **Generates insights autonomously**

👉 This makes it an **AI agent**, not just a tool.

---

## 📌 Limitations

* Depends on LLM output quality
* JSON parsing from LLM can occasionally fail
* Works best with structured tabular data

---

## 🚀 Future Improvements

* Multi-step agent loop
* Vector-based memory
* Natural language query interface
* PDF report generation
* Advanced visualizations

---

## 👩‍💻 Author

Sanchari Singh
Final Year IT Student | Full Stack Developer

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to contribute!
