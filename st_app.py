import streamlit as st
import pandas as pd
import numpy as np
import bcrypt
import json
import os
from  main_dummy import *
# Define the path to the users JSON file
JSON_FILE = "users.json"

# Create a users database
if os.path.exists(JSON_FILE) and os.stat(JSON_FILE).st_size > 0:
    with open(JSON_FILE, "r") as f:
        users = json.load(f)
else:
    users = []

def save_users():
    with open(JSON_FILE, "w") as f:
        json.dump(users, f)

def register(username, password):
    # Check if username already exists
    for user in users:
        if user["username"] == username:
            return "Username already exists"
    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    # Add user to database
    users.append({"username": username, "password": hashed_password})
    save_users()
    return "Registration successful"

def login(username, password):
    # Check if username exists
    for user in users:
        if user["username"] == username:
            # Retrieve the hashed password for the user
            hashed_password = user["password"]
            # Check if the password is correct
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return "Login successful", True
            else:
                return "Incorrect password", False
    return "Username not found", False

# Define the Streamlit app
def app():
    st.title("User Registration and Login")
    val = False
    # Display the registration form
    st.subheader("Register")
    reg_username = st.text_input("Username", key="reg_key")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_button = st.button("Register")
    if reg_button:
        reg_result = register(reg_username, reg_password)
        st.write(reg_result)
        st.write(users) # display the users database after each registration

    # Display the login form
    st.subheader("Login")
    login_username = st.text_input("Username")
    login_password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    if login_button:
            with st.spinner("Logging in..."):
                login_result,val = login(login_username, login_password)
            st.write(login_result)
            if val is True:
                with st.spinner("Generating coffee recommendation..."):
                    predict(username=login_username)
                    pCoffee, usn, em = coffee_recommendation()
                st.write("============================================================", style="blink bold red underline on Green")
                st.write(f"Hello {usn}, your coffee recommendation is {pCoffee} based on your current emotion, {em}", style="blink bold red underline on Green")
                st.write("============================================================", style="blink bold red underline on Green")

                console.print("============================================================", style="blink bold red underline on Green")
                console.print(f"Hello {usn}, your coffee recommendation is {pCoffee} based on your current emotion, {em}", style="blink bold red underline on Green")
                console.print("============================================================", style="blink bold red underline on Green")
    

# Run the Streamlit app
if __name__ == "__main__":
    app()

