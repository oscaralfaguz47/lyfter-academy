from abc import ABC, abstractmethod

class User(ABC):
    def __init__(self, user_name, permissions):
        self.user_name = user_name
        self.permissions = permissions

    @abstractmethod
    def get_role(self):
        pass
    @abstractmethod
    def has_permission(self, permission):
        pass


class AdminUser(User):
    def __init__(self, user_name):
        super().__init__(user_name, [])

    def get_role(self):
        return "Admin"

    def has_permission(self, permission):
        return True

class RegularUser(User):
    def __init__(self, user_name):
        super().__init__(user_name,  ["read"])

    def get_role(self):
        return "Regular"

    def has_permission(self, permission):
            return permission in self.permissions


user_admin = AdminUser("Oscar")
user_regular = RegularUser("Emilio")

print(user_admin.has_permission("delete"))
print(user_regular.has_permission("delete"))