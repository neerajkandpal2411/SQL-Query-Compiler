# 🚀 AI SQL Query Compiler

## ✨ Overview

The **AI SQL Query Compiler** is a powerful and intuitive desktop application that bridges the gap between natural language and SQL. Built with Python's Tkinter, this tool allows users to effortlessly convert plain English queries into executable SQL commands using the power of Artificial Intelligence (OpenAI's GPT-3.5-turbo). It also provides a robust interface to execute these queries against an embedded SQLite database and view the results.

Say goodbye to complex SQL syntax memorization! With this application, you can interact with your database using everyday language.



---

## 🌟 Features

* **Natural Language to SQL Conversion:** Translate your English questions into precise SQL queries with the help of OpenAI's GPT-3.5-turbo.
* **SQL Query Execution:** Run any SQLite-compatible SQL query directly from the GUI.
* **Interactive Results Display:** View query results (especially `SELECT` statements) formatted neatly in a table using Pandas.
* **Persistent SQLite Database:** Comes with a pre-initialized `students` table for immediate testing, and supports creating your own custom tables.
* **User-Friendly GUI:** A clean and scrollable interface built with `tkinter` for a smooth user experience.
* **Error Handling:** Provides clear error messages for invalid inputs or query execution issues.

---

## 🛠️ Technologies Used

* **Python 3.x**
* **Tkinter:** For the Graphical User Interface.
* **SQLite3:** Embedded database for query execution.
* **Pandas:** For elegant display of query results.
* **OpenAI API:** For Natural Language to SQL conversion (specifically `gpt-3.5-turbo`).

---

## 💡 How to Use
<ol>
  <li> Ask in Plain English:</li>
  <ul>
    <li>Type your query in natural language (e.g., "Show me all students older than 20").</li>
    <li>Click "Convert to SQL". The translated SQL will appear in the "Enter SQL Query" box.</li>
  </ul>
  <li>Create Custom Table (Optional):</li>
  <ul>
    <li>In the "Create Table 1 (Optional)" section, enter a CREATE TABLE SQL statement, potentially followed by INSERT statements.</li>
    <li>Click "Create Table 1".</li>
    <li>(A students table is pre-initialized on first run in db/userdb.db.)</li>
  </ul>
  <li>Run SQL Query:</li>
  <ul>
    <li>Either use the AI-generated SQL or type your own SQL query directly into the "Enter SQL Query" box.</li>
    <li>Click "Run Query".</li>
    <li>The results will be displayed in the "Output" section.</li>
  </ul>
</ol>

---

## 📞 Author <br>
Neeraj Kandpal <br>
Linkedin : https://www.linkedin.com/in/neeraj-kandpal/
