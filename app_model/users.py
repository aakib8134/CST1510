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
