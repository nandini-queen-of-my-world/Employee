import streamlit as st
from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
connection_string = "mongodb+srv://Nandini:nandini9502@cluster0.smgpcp9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client['employee_db']
collection = db['employees']

# Streamlit App
st.title("Employee Management System")

# Sidebar for Navigation
option = st.sidebar.selectbox("Choose Option", ["Add Employee", "Search Employee", "View All Employees", "Update Employee", "Delete Employee"])

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

elif option == "View All Employees":
    st.header("List of All Employees")
    employees = list(collection.find({}, {"_id": 0, "emp_id": 1, "name": 1, "department": 1}))
    if employees:
        df = pd.DataFrame(employees)
        st.dataframe(df)
    else:
        st.write("No employees found.")

elif option == "Update Employee":
    st.header("Update Employee Details")
    update_id = st.text_input("Enter Employee ID to update")
    if st.button("Search Employee to Update"):
        result = collection.find_one({"emp_id": update_id})
        if result:
            name = st.text_input("Name", value=result.get('name', ''))
            dept = st.text_input("Department", value=result.get('department', ''))
            if st.button("Update Employee"):
                result = collection.update_one({"emp_id": update_id}, {"$set": {"name": name, "department": dept}})
                if result.matched_count > 0:
                    st.success(f"Employee {name} updated successfully!")
                else:
                    st.error("Update failed.")
        else:
            st.error("Employee not found.")

elif option == "Delete Employee":
    st.header("Delete Employee")
    delete_id = st.text_input("Enter Employee ID to delete")
    if st.button("Delete Employee"):
        result = collection.find_one({"emp_id": delete_id})
        if result:
            collection.delete_one({"emp_id": delete_id})
            st.success(f"Employee {result['name']} deleted successfully!")
        else:
            st.error("Employee not found.")
