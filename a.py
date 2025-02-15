import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS fitness (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT NOT NULL,
                      age INTEGER,
                      weight REAL,
                      date TEXT,
                      exercise TEXT,
                      duration INTEGER,
                      calories INTEGER)''')
    conn.commit()
    conn.close()

# Function to add record
def add_record(name, age, weight, date, exercise, duration, calories):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fitness (name, age, weight, date, exercise, duration, calories) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (name, age, weight, date, exercise, duration, calories))
    conn.commit()
    conn.close()

# Function to load records
def load_records():
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fitness")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows, columns=["ID", "Name", "Age", "Weight (kg)", "Date", "Exercise", "Duration (mins)", "Calories Burned"])

# Function to delete record
def delete_record(record_id):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fitness WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()

# Function to update record
def update_record(record_id, name, age, weight, date, exercise, duration, calories):
    conn = sqlite3.connect("fitness_tracker.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE fitness SET name=?, age=?, weight=?, date=?, exercise=?, duration=?, calories=? WHERE id=?",
                   (name, age, weight, date, exercise, duration, calories, record_id))
    conn.commit()
    conn.close()

# Streamlit UI
st.title("Personal Fitness Tracker")

# Initialize database
init_db()

# Sidebar menu
menu = st.sidebar.radio("Select a section", ["Add Record", "View Records", "Update Record", "Delete Record"])

# Add New Record
if menu == "Add Record":
    with st.form("add_form"):
        st.header("Add New Record")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        weight = st.number_input("Weight (kg)", min_value=1.0)
        date = st.date_input("Date", min_value=datetime(2000, 1, 1))
        exercise = st.text_input("Exercise")
        duration = st.number_input("Duration (mins)", min_value=1)
        calories = st.number_input("Calories Burned", min_value=1)

        submit_button = st.form_submit_button("Add Record")

        if submit_button:
            if name and exercise and duration and calories:
                add_record(name, age, weight, date.strftime('%Y-%m-%d'), exercise, duration, calories)
                st.success("Record added successfully!")
            else:
                st.error("Please fill all fields!")

# View Records
elif menu == "View Records":
    st.header("Fitness Records")
    df = load_records()

    if df.empty:
        st.write("No records available.")
    else:
        st.write(df)

# Update Record
elif menu == "Update Record":
    st.header("Update Record")
    df = load_records()

    selected_id = st.selectbox("Select Record ID to Update", df["ID"].tolist())

    if selected_id:
        selected_record = df[df["ID"] == selected_id].iloc[0]
        st.write("Selected Record:", selected_record)

        with st.form("update_form"):
            new_name = st.text_input("Name", selected_record["Name"])
            new_age = st.number_input("Age", min_value=1, max_value=100, value=selected_record["Age"])
            new_weight = st.number_input("Weight (kg)", min_value=1.0, value=selected_record["Weight (kg)"])
            new_date = st.date_input("Date", value=datetime.strptime(selected_record["Date"], '%Y-%m-%d'))
            new_exercise = st.text_input("Exercise", selected_record["Exercise"])
            new_duration = st.number_input("Duration (mins)", min_value=1, value=selected_record["Duration (mins)"])
            new_calories = st.number_input("Calories Burned", min_value=1, value=selected_record["Calories Burned"])

            update_button = st.form_submit_button("Update Record")

            if update_button:
                update_record(selected_id, new_name, new_age, new_weight, new_date.strftime('%Y-%m-%d'), new_exercise, new_duration, new_calories)
                st.success("Record updated successfully!")

# Delete Record
elif menu == "Delete Record":
    st.header("Delete Record")
    df = load_records()

    selected_id = st.selectbox("Select Record ID to Delete", df["ID"].tolist())

    if selected_id:
        selected_record = df[df["ID"] == selected_id].iloc[0]
        st.write("Selected Record:", selected_record)

        delete_button = st.button("Delete Record")
        if delete_button:
            delete_record(selected_id)
            st.success("Record deleted successfully!")

