from app.security.permissions import ROLE_PERMISSIONS, Permission, UserRole

EXPECTED_PERMISSIONS = {
    UserRole.ADMIN: set(Permission),
    UserRole.CLIENT: {Permission.PRODUCTS_READ},
}

# Changing the policy must require updating this test
def test_role_permissions_match_expected_policy() -> None:
    assert ROLE_PERMISSIONS == EXPECTED_PERMISSIONS