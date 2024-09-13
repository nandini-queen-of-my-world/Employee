import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['employee_db']
collection = db['employees']

# Streamlit App
st.title("Employee Management System")

# Sidebar for Navigation
option = st.sidebar.selectbox("Choose Option", ["Add Employee", "Search Employee"])

if option == "Add Employee":
    st.header("Add Employee Details")
    emp_id = st.text_input("Employee ID")
    name = st.text_input("Name")
    dept = st.text_input("Department")
    if st.button("Add Employee"):
        if emp_id and name and dept:
            collection.insert_one({"emp_id": emp_id, "name": name, "department": dept})
            st.success(f"Employee {name} added successfully!")
        else:
            st.error("Please fill all fields.")

elif option == "Search Employee":
    st.header("Search Employee")
    search_id = st.text_input("Enter Employee ID to search")
    if st.button("Search"):
        result = collection.find_one({"emp_id": search_id})
        if result:
            st.write(f"Employee ID: {result['emp_id']}")
            st.write(f"Name: {result['name']}")
            st.write(f"Department: {result['department']}")
        else:
            st.error("Employee not found.")
