from flask import session, redirect, url_for

def login_required(func):
    def wrapper():
        if "user_id" not in session:
            print("Login necessário!")
            return url_for("auth.login")
        return func()
    return wrapper