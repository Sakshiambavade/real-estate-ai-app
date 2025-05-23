# Real Estate AI Assistant 🏡

This is a Streamlit web app powered by LangChain and Groq to query real estate data stored in a local SQLite database (`real_estate.db`).

## Features

- Natural language querying over structured data
- Uses Groq's Gemma and Mixtral models
- No need for MySQL — powered by SQLite
- Built with Streamlit for a simple UI

## Usage

1. Clone this repo
2. Add your `.env` file with `GROQ_API_KEY`
3. Run locally:

```bash
pip install -r requirements.txt
streamlit run main.py
