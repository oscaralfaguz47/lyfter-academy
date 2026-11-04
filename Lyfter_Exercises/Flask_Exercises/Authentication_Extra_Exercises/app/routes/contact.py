
from flask import Blueprint, request, url_for
from app.database import get_session
from app.services.contact_service import ContactService
from app.repositories.contact_repository import ContactRepository
from app.auth import current_actor, login_required
from app.schemas.contact import ContactListParams, ContactRead, ContactCreate
from app.schemas.validation import parse
from app.routes.responses import pagination_meta, ok, serialize_many, created, serialize

contact_bp = Blueprint("contacts", __name__, url_prefix="/api/v1/contacts")

def _contact_service() -> ContactService:
    session = get_session()
    return ContactService(session, ContactRepository(session))


@contact_bp.get("")
@login_required
def list_contacts():
    params = parse(ContactListParams, request.args.to_dict(), "Invalid query parameters.")
    contacts, total = _contact_service().list_contacts(params, current_actor())
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(ContactRead, contacts), meta=meta)

@contact_bp.post("")
@login_required
def create_contact():
    data = parse(ContactCreate, request.get_json())
    contact = _contact_service().create_contact(data, current_actor())
    return created(serialize(ContactRead, contact), location=url_for("contacts.get_contact", contact_id=contact.id))

@contact_bp.get("/<int:contact_id>")
@login_required
def get_contact(contact_id: int):
    contact = _contact_service().get_contact(contact_id, current_actor())
    return ok(serialize(ContactRead, contact))
