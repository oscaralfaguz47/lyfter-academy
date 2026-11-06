
from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    USER = "user"

class Permission(StrEnum):
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    CONTACTS_READ = "contacts:read"
    CONTACTS_DELETE = "contacts:delete"
    LOGIN_HISTORY_READ = "login_history:read"

ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.ADMIN: frozenset(Permission),
    UserRole.USER: frozenset(),
}

@dataclass(frozen=True)
class Actor: 
    """ The authenticated user performing the current action. """

    id: int
    role: UserRole

    def can(self, permission: Permission) -> bool:
        return permission in ROLE_PERMISSIONS[self.role]

    def can_access_user(self, user_id: int, permission: Permission) -> bool:
        """ Own account, or the permission to act on anyone's. """
        return self.id == user_id or self.can(permission)