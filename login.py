import re
import bcrypt
import sqlite3
import pandas as pd


def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    bcrypted_password = bcrypt.hashpw(password_bytes, salt)
    return (bcrypted_password).decode("utf-8")


def check_password(plain_text_password, hash_password):
    password_bytes = plain_text_password.encode("utf-8")
    hash_password_bytes = hash_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hash_password_bytes)


def register_user(user_name, password):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()

        for user in users:
            line = user.strip().split(',')
            if line[0] == user_name:
                print("User already exists")
                return
    h_password = hash_password(password)
    with open('DATA/users.txt', 'a') as f:
        f.write(f"{user_name},{h_password}\n")


def login_user(user_name, password):
    with open('DATA/users.txt', 'r') as f:
        users = f.readlines()

        for user in users:
            line = user.strip().split(',')
            if line[0] == user_name:
                if check_password(password, line[1]):
                    return True
                else:
                    return False
    print("User does not exist")
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
            # Registration flow
            print("\n--- USER REGISTRATION ---")
            username = input("Enter a username: ").strip()

            # Validate username
            is_valid, error_msg = username_validation(username)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue

            password = input("Enter a password: ").strip()

            # Validate password
            is_valid, error_msg = password_validation(password)
            if not is_valid:
                print(f"Error: {error_msg}")
                continue
            # Confirm password
            # Confirm password
            password_confirm = input("Confirm password: ").strip()
            if password != password_confirm:
                print("Error: Passwords do not match.")
                continue
            role = input("Enter your role: ").strip().lower()

            # Register the user
            register_user(username, password)
        elif choice == '2':
            # Login flow
            print("\n--- USER LOGIN ---")
            username = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()

            # Attempt login
            if login_user(username, password):
                print("\nYou are now logged in.")
                print(
                    "(In a real application, you would now access the dashboard or protected resources.)")

                # Optional: Ask if they want to logout or exit
                input("\nPress Enter to return to main menu...")
        elif choice == '3':
            # Exit
            print("\nThank you for using the authentication system.")
            print("Exiting...")
            break

        else:
            print("\nError: Invalid option. Please select 1, 2, or 3.")


# if __name__ == "__main__":
#    main()


def user_table(conn):
    conn = sqlite3.connect("DATA/intelligent_platform.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()


def add_user(conn, username, password, role):
    cursor = conn.cursor()
    cursor.execute('''
            INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)
        ''', (username, password, role))
    conn.commit()


def migrate_users_to_db(conn):
    with open("DATA/users.txt", "r") as f:
        users = f.readlines()
        for user in users:
            name, password_hash = user.strip().split(',')
            add_user(conn, name, password_hash)

    conn.close()


# read data from the users.


def get_all_users(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def get_user(conn, name):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, password_hash FROM users WHERE username = ?", (name,))
    user = cursor.fetchone()
    conn.close()
    return user


def update_user(conn, name, new_name):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET username = ? WHERE username = ?", (new_name, name))
    conn.commit()
    conn.close()
    return name + " has been updated." + " New username: " + new_name


def delete_user(conn, name):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (name,))
    conn.commit()
    conn.close()
    return name + " has been deleted from the database."


def migrate_cyber_incidents_to_db(conn):
    data = pd.read_csv("DATA/cyber_incidents.csv")
    data.to_sql("cyber_incidents", conn)


def migrate_datasets_metadata_to_db(conn):
    data = pd.read_csv("DATA/datasets_metadata.csv")
    data.to_sql("datasets_metadata", conn)


def migrate_it_tickets_to_db(conn):
    data = pd.read_csv("DATA/it_tickets.csv")
    data.to_sql("it_tickets", conn)


def get_all_cyber_incidents(conn):
    sql = '''
        SELECT * FROM cyber_incidents
    '''
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)


def get_all_datasets_metadata(conn):
    sql = '''
        SELECT * FROM datasets_metadata
    '''
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)


def get_all_it_tickets(conn):
    sql = '''
        SELECT * FROM it_tickets
    '''
    data = pd.read_sql(sql, conn)
    conn.close()
    return (data)


conn = sqlite3.connect("DATA/intelligent_platform.db")
