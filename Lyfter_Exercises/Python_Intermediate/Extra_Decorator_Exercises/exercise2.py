user_logged_in = False

def requires_login(func):
    def wrapper(*args, **kwargs):
        if not user_logged_in:
            raise PermissionError("User not authenticated")
        func(*args, **kwargs)
    return wrapper

@requires_login
def view_profile():
    print("Show user's profile")

try:
    view_profile()
except PermissionError as e:
    print(e)

user_logged_in = True
view_profile()