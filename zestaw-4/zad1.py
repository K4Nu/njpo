import functools
import hashlib, binascii
from dotenv import load_dotenv
import os
import shelve
from os import urandom
load_dotenv()

def hash_password(password):
    #salt stored in .env file
    get_salt=os.getenv("SALT",None)
    salt=str.encode(os.getenv("salt")) if get_salt else hashlib.sha256(urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


def store_user_data():
    """Store initial user data in shelve with unique salts."""
    with shelve.open("UserDB") as db:
        # Create users and hash their passwords with unique salts
        data = {
            "Tomek": hash_password("azOr"),
            "Janek": hash_password("w12@az"),
            "Rozalia": hash_password("Youn12!@#"),
        }
        for username, pwd_hash in data.items():
            db[username] = pwd_hash

def authenticate(func):
    """Decorator to authenticate a user based on login and password."""
    def wrapper(login,password):
        with shelve.open("UserDB") as file:
            if login in file:
                if file.get(login)==hash_password(password):
                    print("You are succefully logged in!")
                    return True
                else:
                    print("Your data is incorrect")
            return False
    return wrapper

@authenticate
def login_user(login, password):
    """Authenticate user and provide feedback."""


# Test login with detailed responses

#store_user_data()
print(login_user("Tomek","azO"))