import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import openai
import os

# Set ey from environment variable for security
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY", "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"))

# Persistent database setup
def init_db():
    db_path = os.path.join("db", "userdb.db")
    os.makedirs("db", exist_ok=True)
    is_new = not os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if is_new:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                grade TEXT
            )
        ''')
        cursor.executemany('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', [
            ('Alice', 20, 'A'),
            ('Bob', 21, 'B'),
            ('Charlie', 22, 'C')
        ])
        conn.commit()
    return conn

# Convert natural language to SQL
def nl_to_sql():
    user_input = nl_entry.get().strip()
    if not user_input:
        messagebox.showwarning("Empty Input", "Please enter a plain English query.")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Convert plain English into SQLite-compatible SQL queries."},
                {"role": "user", "content": user_input}
            ]
        )
        sql = response.choices[0].message.content.strip()
        query_input.delete("1.0", tk.END)
        query_input.insert(tk.END, sql)
    except Exception as e:
        messagebox.showerror("OpenAI Error", str(e))

# Execute SQL query
def run_query():
    query = query_input.get("1.0", tk.END).strip()
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)

    if not query:
        messagebox.showwarning("Empty Query", "Please enter a SQL query.")
        return

    try:
        cursor = db_conn.cursor()
        cursor.execute(query)

        if query.lower().startswith("select"):
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            df = pd.DataFrame(rows, columns=columns)
            output_text.insert(tk.END, df.to_string(index=False))
        else:
            db_conn.commit()
            output_text.insert(tk.END, "Query executed successfully.")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}")

    output_text.config(state=tk.DISABLED)

# Create user-defined table
def create_table():
    sql = table_input.get("1.0", tk.END).strip()
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    try:
        cursor = db_conn.cursor()
        cursor.executescript(sql)
        db_conn.commit()
        output_text.insert(tk.END, "Table created and records inserted successfully.")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}")
    output_text.config(state=tk.DISABLED)

# --- GUI Setup with Scrollable Frame ---
root = tk.Tk()
root.title("AI SQL Query Compiler")
root.geometry("900x850")
root.configure(bg="#f4f4f4")

# Canvas + Scrollbar for scrolling
main_canvas = tk.Canvas(root, bg="#f4f4f4")
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)
main_canvas.configure(yscrollcommand=scrollbar.set)

# Scrollable content frame inside canvas
frame = tk.Frame(main_canvas, bg="#f4f4f4")
main_canvas.create_window((0, 0), window=frame, anchor="nw")

# Update scrollregion
def update_scroll_region(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))
frame.bind("<Configure>", update_scroll_region)

# Enable mouse wheel scrolling
def on_mousewheel(event):
    main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
main_canvas.bind_all("<MouseWheel>", on_mousewheel)

# --- Widgets go inside `frame` instead of `root` ---
title_font = ("Helvetica", 14, "bold")
text_font = ("Consolas", 12)
button_font = ("Helvetica", 12, "bold")

# Natural Language Input
tk.Label(frame, text="Ask in Plain English:", font=title_font, bg="#f4f4f4").pack(anchor='w', padx=20, pady=(20, 5))
nl_frame = tk.Frame(frame)
nl_frame.pack(fill=tk.X, padx=20)
nl_entry = tk.Entry(nl_frame, font=text_font)
nl_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
tk.Button(nl_frame, text="Convert to SQL", font=button_font, bg="#2196F3", fg="white", command=nl_to_sql).pack()

# User-defined Table
tk.Label(frame, text="Create Table 1 (Optional):", font=title_font, bg="#f4f4f4").pack(anchor='w', padx=20, pady=(20, 5))
table_frame = tk.Frame(frame)
table_frame.pack(fill=tk.BOTH, expand=True, padx=20)
table_scroll = tk.Scrollbar(table_frame)
table_scroll.pack(side=tk.RIGHT, fill=tk.Y)
table_input = tk.Text(table_frame, height=6, font=text_font, yscrollcommand=table_scroll.set, wrap="word", bd=2, relief="sunken")
table_input.pack(fill=tk.BOTH, expand=True)
table_scroll.config(command=table_input.yview)
tk.Button(frame, text="Create Table 1", font=button_font, bg="#9C27B0", fg="white", command=create_table).pack(pady=10)

# SQL Query Input
tk.Label(frame, text="Enter SQL Query:", font=title_font, bg="#f4f4f4").pack(anchor='w', padx=20, pady=(20, 5))
query_frame = tk.Frame(frame)
query_frame.pack(fill=tk.BOTH, expand=True, padx=20)
query_scroll = tk.Scrollbar(query_frame)
query_scroll.pack(side=tk.RIGHT, fill=tk.Y)
query_input = tk.Text(query_frame, height=8, font=text_font, yscrollcommand=query_scroll.set, wrap="word", bd=2, relief="sunken")
query_input.pack(fill=tk.BOTH, expand=True)
query_scroll.config(command=query_input.yview)

# Run Button
tk.Button(frame, text="Run Query", command=run_query, font=button_font, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

# Output Display
tk.Label(frame, text="Output:", font=title_font, bg="#f4f4f4").pack(anchor='w', padx=20, pady=(10, 5))
output_frame = tk.Frame(frame)
output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
output_scroll = tk.Scrollbar(output_frame)
output_scroll.pack(side=tk.RIGHT, fill=tk.Y)
output_text = tk.Text(output_frame, height=10, font=text_font, yscrollcommand=output_scroll.set, wrap="word", bd=2, relief="sunken", bg="#eeeeee", state=tk.DISABLED)
output_text.pack(fill=tk.BOTH, expand=True)
output_scroll.config(command=output_text.yview)

# Init DB
db_conn = init_db()

# Run App
root.mainloop()
