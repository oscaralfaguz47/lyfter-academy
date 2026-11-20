import click 
from flask import Flask


from app.database import get_session
from app.repositories.user_repository import UserRepository
from app.security.permissions import UserRole, ROLE_PERMISSIONS, Permission


def register_commands(app: Flask) -> None:
    @app.cli.command("promote-admin")
    @click.argument("email")
    def promote_admin(email: str) -> None:
        session = get_session()
        user = UserRepository(session).get_by_email(email.lower())
        if user is None: 
            raise click.ClickException(f"No user with email {email}")
        user.role = UserRole.ADMIN
        session.commit()
        click.echo(f"{email} is now admin.")

    @app.cli.command("permissions")
    def list_permissions() -> None:
        """ Print which roles have which permissions. """
        roles = list(ROLE_PERMISSIONS)
        click.echo(f"{'permission':<20}" + "".join(f"{role:<8}" for role in roles))
        for permission in Permission:
            marks = "".join(f"{'✓' if permission in ROLE_PERMISSIONS[role] else 'x':<8}" for role in roles)
            click.echo(f"{permission:<20}{marks}")