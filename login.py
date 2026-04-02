import re
import bcrypt
import sqlite3
import pandas as pd

from app_model.db import conn
from app_model.users import add_user, get_user


def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    bcrypted_password = bcrypt.hashpw(password_bytes, salt)
    return (bcrypted_password).decode("utf-8")


def check_password(plain_text_password, hash_password):
    password_bytes = plain_text_password.encode("utf-8")
    hash_password_bytes = hash_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_password_bytes)


def register_user(conn):
    name = input("Enter your name: ")
    password = input("Enter your password: ")
    role = input("Enter your role: ")
    h_password = hash_password(password)
    add_user(conn, name, h_password, role)


def login_user(conn):
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    username, password_hash = get_user(conn, username)
    if username == username and check_password(password, password_hash):
        print("\nLogin successful! Welcome, " + username + "!")
        return True
    return False


def username_validation(username):
    if len(username) < 3 or len(username) > 20:
        return (False, "Username must be between 3 and 20 characters")
    if not re.match("^[a-zA-Z0-9_]+$", username):
        return (False, "Username can only contain letters, numbers and underscores")
    return (True, "Username is valid")


def password_validation(password):
    if len(password) < 8:
        return (False, "Password must be at least 8 characters long")
    if not re.search("[a-z]", password):
        return (False, "Password must contain one lowercase letter")
    if not re.search("[A-Z]", password):
        return (False, "Password must contain one uppercase letter")
    if not re.search("[0-9]", password):
        return (False, "Password must contain at least one digit")
    return (True, "Password is valid")


def display_menu():
    """Displays the main menu options."""
    print("\n" + "="*50)
    print(" MULTI-DOMAIN INTELLIGENCE PLATFORM")
    print(" Secure Authentication System")
    print("="*50)
    print("\n[1] Register a new user")
    print("[2] Login")
    print("[3] Exit")
    print("-"*50)


def main():
    """Main program loop."""
    print("\nWelcome to the Week 7 Authentication System!")

    while True:
        display_menu()
        try:
            choice = input("\nPlease select an option (1-3): ").strip()
        except KeyboardInterrupt:
            print("\nProgram interrupted.")
            break

        if choice == '1':
            # Register the user
            register_user(conn)
            print("\nRegistration successful! You can now log in.")
        elif choice == '2':
            # Login flow
            if login_user(conn):
                print("\nYou are now logged in.")
            else:
                print("\nLogin failed. Please check your username and password.")
                # Optional: Ask if they want to logout or exit
            input("\nPress Enter to return to main menu...")
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
