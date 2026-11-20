import pytest

from app.security.permissions import ROLE_PERMISSIONS, Permission, UserRole, Actor

EXPECTED_PERMISSIONS = {
    UserRole.ADMIN: set(Permission),
    UserRole.CLIENT: {Permission.PRODUCTS_READ},
}

OWN_ID = 1
OTHER_ID = 2

# Changing the policy must require updating this test
def test_role_permissions_match_expected_policy() -> None:
    assert ROLE_PERMISSIONS == EXPECTED_PERMISSIONS

@pytest.mark.parametrize(
    ("role", "target_id", "expected"),
    [
        (UserRole.CLIENT, OWN_ID, True),
        (UserRole.CLIENT, OTHER_ID, False),
        (UserRole.ADMIN, OTHER_ID, True),
    ],
    ids=["client_own_account", "client_other_account", "admin_other_account"],
)
def test_can_access_user_with_users_read_returns_expected(role: UserRole, target_id: int, expected: bool) -> None:
    actor = Actor(id=OWN_ID, role=role)
    assert actor.can_access_user(target_id, Permission.USERS_READ) is expected