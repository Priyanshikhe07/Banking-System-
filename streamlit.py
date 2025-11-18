import streamlit as st
from pathlib import Path
import json
import random
import string

# ------------------------------
# Bank Class
# ------------------------------
class Bank:
    database = 'database.json'
    data = []

    # Load existing DB
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            with open(database, "w") as f:
                json.dump([], f)
    except Exception as err:
        st.error(f"Error loading database: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_uppercase, k=5)
        digits = random.choices(string.digits, k=4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id)

    # Create account
    @staticmethod
    def create_account():
        st.subheader("Create New Account")
        name = st.text_input("Enter your name")
        email = st.text_input("Enter your email")
        phone = st.text_input("Enter phone number (10 digits)")
        pin = st.text_input("Enter 4-digit PIN", type="password")

        if st.button("Create Account"):
            if len(pin) != 4 or not pin.isdigit():
                st.warning("PIN must be exactly 4 digits!")
                return

            if len(phone) != 10 or not phone.isdigit():
                st.warning("Phone number must be 10 digits!")
                return

            acc_no = Bank.__accountno()
            data = {
                "name": name,
                "email": email,
                "phone no.": phone,
                "pin": int(pin),
                "Account no.": acc_no,
                "Balance": 0
            }

            Bank.data.append(data)
            Bank.__update()

            st.success(f"Account created! Your Account Number: **{acc_no}**")

    # Deposit money
    @staticmethod
    def deposit_money():
        st.subheader("Deposit Money")
        acc = st.text_input("Enter your Account Number")
        pin = st.text_input("Enter PIN", type="password")

        amount = st.number_input("Enter amount to deposit", min_value=1)

        if st.button("Deposit"):
            user = [i for i in Bank.data if i["Account no."] == acc and str(i["pin"]) == pin]

            if not user:
                st.error("Invalid account or PIN!")
                return

            if amount > 10000:
                st.warning("Max deposit limit is ₹10,000")
                return

            user[0]["Balance"] += amount
            Bank.__update()
            st.success("Amount deposited successfully!")

    # Withdraw money
    @staticmethod
    def withdraw_money():
        st.subheader("Withdraw Money")
        acc = st.text_input("Enter Account Number")
        pin = st.text_input("Enter PIN", type="password")
        amount = st.number_input("Enter amount to withdraw", min_value=1)

        if st.button("Withdraw"):
            user = [i for i in Bank.data if i["Account no."] == acc and str(i["pin"]) == pin]

            if not user:
                st.error("Invalid account or PIN!")
                return

            if amount > user[0]["Balance"]:
                st.error("Insufficient balance!")
                return

            user[0]["Balance"] -= amount
            Bank.__update()
            st.success("Amount withdrawn!")

    # Show details
    @staticmethod
    def details():
        st.subheader("Check Account Details")
        acc = st.text_input("Enter Account Number")
        pin = st.text_input("Enter PIN", type="password")

        if st.button("Show Details"):
            user = [i for i in Bank.data if i["Account no."] == acc and str(i["pin"]) == pin]

            if not user:
                st.error("Invalid account or PIN!")
                return

            st.json(user[0])

    # Update details
    @staticmethod
    def update_details():
        st.subheader("Update Account Details")
        acc = st.text_input("Enter Account Number")
        pin = st.text_input("Enter PIN", type="password")

        if st.button("Verify"):
            st.session_state["verified"] = [i for i in Bank.data if i["Account no."] == acc and str(i["pin"]) == pin]

        if "verified" in st.session_state and st.session_state["verified"]:
            user = st.session_state["verified"][0]

            st.write("Leave any field blank to skip updating.")

            new_name = st.text_input("New name", value=user["name"])
            new_email = st.text_input("New email", value=user["email"])
            new_phone = st.text_input("New phone", value=user["phone no."])
            new_pin = st.text_input("New PIN", value=str(user["pin"]), type="password")

            if st.button("Update"):
                user["name"] = new_name
                user["email"] = new_email
                user["phone no."] = new_phone
                user["pin"] = int(new_pin)

                Bank.__update()
                st.success("Details updated!")

    # Delete account
    @staticmethod
    def delete_account():
        st.subheader("Delete Account")
        acc = st.text_input("Enter Account Number")
        pin = st.text_input("Enter PIN", type="password")

        if st.button("Delete"):
            user = [i for i in Bank.data if i["Account no."] == acc and str(i["pin"]) == pin]

            if not user:
                st.error("Invalid account or PIN!")
                return

            Bank.data.remove(user[0])
            Bank.__update()
            st.success("Account deleted!")


# ------------------------------------
# Streamlit UI Navigation
# ------------------------------------
st.title("🏦 BANK MANAGEMENT SYSTEM")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Account Details",
        "Update Details", "Delete Account"]

choice = st.sidebar.selectbox("Navigation Menu", menu)

if choice == "Create Account":
    Bank.create_account()

elif choice == "Deposit Money":
    Bank.deposit_money()

elif choice == "Withdraw Money":
    Bank.withdraw_money()

elif choice == "Account Details":
    Bank.details()

elif choice == "Update Details":
    Bank.update_details()

elif choice == "Delete Account":
    Bank.delete_account()