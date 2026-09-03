from datetime import date

class User:
    def __init__(self, name, date_of_birth):
        self.name = name
        self.date_of_birth = date_of_birth

    @property
    def age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year
        if(today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        return age

def validate_user_is_and_adult(func):
    def wrapper(user):
        if user.age < 18:
            raise ValueError(f"The user {user.name} is not an adult, the user's age is: {user.age}")
        return func(user)
    return wrapper

@validate_user_is_and_adult
def get_in_users_in_bar(user):
    print(f"The user {user.name} was accepted in the bar, the user's age is: {user.age}")

 
user_adult = User("Oscar", date(1993, 1, 11))
user_minor = User("Pamela", date(2020, 5, 20))

for user in [user_adult, user_minor]:
    try:
        get_in_users_in_bar(user)
    except ValueError as e:
        print(e)