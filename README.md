
# AI-Powered SQL Query Compiler

A Python-based SQL compiler with GUI that:
- Accepts SQL queries and shows output
- Supports Natural Language to SQL conversion using OpenAI API
- Allows users to create and insert their own tables
- Stores tables and data persistently using SQLite

## How to Run
```bash
pip install -r requirements.txt
python ui.py
```

## Features
- SQLite backend (persistent)
- OpenAI GPT-3.5 API integration
- Full GUI with Tkinter

## Directory
- `app.py` – Main GUI and logic
- `db/userdb.db` – Your saved tables/data
- `assets/` – Optional for images or styling

## Note
Replace `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` in `ui.py` with your actual OpenAI API key.