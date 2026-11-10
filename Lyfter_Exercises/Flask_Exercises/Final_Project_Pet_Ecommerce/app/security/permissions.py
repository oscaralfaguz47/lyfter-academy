
from dataclasses import dataclass
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    CLIENT = "client"

class Permission(StrEnum):
    USERS_READ = "users:read"
    USERS_UPDATE = "users:update"
    USERS_DELETE = "users:delete"
    PRODUCTS_READ = "products:read"
    PRODUCTS_CREATE = "products:create"
    PRODUCTS_UPDATE = "products:update"
    PRODUCTS_DELETE = "products:delete"
    PRODUCTS_RESTOCK = "products:restock"
    INVOICES_READ = "invoices:read"
    LOGIN_HISTORY_READ = "login_history:read"

ROLE_PERMISSIONS: dict[UserRole, frozenset[Permission]] = {
    UserRole.ADMIN: frozenset(Permission),
    UserRole.CLIENT: frozenset({Permission.PRODUCTS_READ}),
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