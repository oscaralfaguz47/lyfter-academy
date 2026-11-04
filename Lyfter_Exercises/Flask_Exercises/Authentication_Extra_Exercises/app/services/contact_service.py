
from sqlalchemy.orm import Session

from collections.abc import Sequence

from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactListParams, ContactCreate
from app.security.permissions import Actor, Permission
from app.models.contact import Contact
from app.errors.handlers import NotFoundError

import logging
logger = logging.getLogger(__name__)

class ContactService:
    def __init__(self, session: Session, repository: ContactRepository) -> None:
        self._session = session
        self._repository = repository

    def list_contacts(self, params: ContactListParams, actor: Actor) -> Sequence[Contact]:
        user_id = params.user_id if actor.can(Permission.CONTACTS_READ) else actor.id
        contacts = self._repository.list(params, user_id)
        return contacts, self._repository.count(params, user_id)

    def create_contact(self, data: ContactCreate, actor: Actor) -> Contact:
        contact = Contact(**data.model_dump(exclude_none=True), user_id=actor.id)
        self._repository.add(contact)
        self._session.commit()
        logger.info("Contact %s created", contact.id)
        return contact

    def get_contact(self, contact_id: int, actor: Actor) -> Contact | None:
        contact = self._repository.get_by_id(contact_id)
        if contact is None or (contact.user_id != actor.id and not actor.can(Permission.CONTACTS_READ)):
            raise NotFoundError(f"Contact {contact_id} not found.")
        return contact
