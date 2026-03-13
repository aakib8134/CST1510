import bcrypt

plain_text_password = "Magic123"


def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode("utf-8")
    salt = bcrypt.gensalt()
    bcrypted_password = bcrypt.hashpw(password_bytes, salt)
    return (bcrypted_password).decode("utf-8")


def check_password(plain_text_password, hash_password):
    password_bytes = plain_text_password.encode("utf-8")
    hash_password_bytes = hash_password.encode("utf-8")
    if bcrypt.checkpw(password_bytes, hash_password_bytes):
        print("Password is correct")
    else:
        print("Password is incorrect")


user_name = input("What is your name?")
password = input("What is your password?")


def register_user(user_name, password):
    with open('users.txt', 'r') as f:
        users = f.readlines()

        for user in users:
            line = user.strip().split(',')
            if line[0] == user_name:
                print("User already exists")
                return
    h_password = hash_password(password)
    with open('users.txt', 'a') as f:
        f.write(f"{user_name},{h_password}\n")


register_user(user_name, password)


def login_user(user_name, password):
    with open('users.txt', 'r') as f:
        users = f.readlines()

        for user in users:
            line = user.strip().split(',')
            if line[0] == user_name:
                check_password(password, line[1])
                return
    print("User does not exist")


login_user(user_name, password)
