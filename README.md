# The Empathetic Analyzer 🟣

> **"Building the Bank of 2035: Where AI meets Empathy"**

This project demonstrates an **AI-powered Debt Collection Agent** designed for the Riverline.ai ecosystem. It analyzes borrower conversations in real-time to distinguish between **"Ability to Pay"** (Distress) and **"Willingness to Pay"** (Strategic Default), enabling empathetic and economically optimal recovery strategies.

## ✨ Features

*   **Real-time Sentiment Analysis**: Uses Hugging Face Transformers (`distilbert`) to gauge borrower stress levels.
*   **Economic Intent Classifier**: Distinguishes technical defaults from willful defaults using linguistic pattern matching.
*   **Nudge Theory Integration**: Recommends behavioral nudges (e.g., restructuring vs. credit score reminders) based on the borrower's persona.
*   **Premium Dashboard**: A dark-themed, data-rich interface for collections agents.

## 🛠️ Tech Stack

*   **Frontend**: Streamlit (Python-based interactive dashboard)
*   **ML Engine**: Hugging Face `transformers`, `torch`
*   **Logic**: Custom rule-based intent classification
*   **Styling**: Custom CSS for the "Riverline" aesthetic

## 🚀 How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App**:
    ```bash
    streamlit run app.py
    ```

3.  **Explore Scenarios**: use the sidebar to switch between "Job Loss", "Strategic Default", etc.

## 📂 Project Structure

```
empathetic-analyzer/
├── app.py                 # Main Dashboard Application
├── requirements.txt       # Dependencies
├── src/
│   ├── analyzer_engine.py # ML Logic (Hugging Face + Classifier)
│   ├── data_generator.py  # Realistic Conversation Simulator
│   └── styles.css         # Premium UI Styling
```
