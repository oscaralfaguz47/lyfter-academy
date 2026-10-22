from flask import Blueprint, request, url_for

from app.services.address_service import AddressService
from app.database import get_session
from app.repositories.address_repository import AddressRepository
from app.repositories.user_repository import UserRepository
from app.schemas.validation import parse
from app.schemas.address import AddressRead, AddressCreate, AddressUpdate, AddressListParams
from app.routes.responses import pagination_meta, serialize_many, serialize
from app.routes.responses import ok, created, no_content


addresses_bp = Blueprint("addresses", __name__, url_prefix="/api/v1/addresses")

def _address_service() -> AddressService:
    session = get_session()
    return AddressService(session, AddressRepository(session), UserRepository(session))


@addresses_bp.get("")
def list_addresses():
    params = parse(AddressListParams, request.args.to_dict(), "Invalid query params.")
    addresses, total = _address_service().list_addresses(params)
    meta = pagination_meta(params.page, params.per_page, total)
    return ok(serialize_many(AddressRead, addresses), meta=meta)

@addresses_bp.get("/<int:address_id>")
def get_address(address_id: int):
    address = _address_service().get_address(address_id)
    return ok(serialize(AddressRead, address))

@addresses_bp.post("")
def create_address():
    data = parse(AddressCreate, request.get_json())
    address = _address_service().create_address(data)
    return created(serialize(AddressRead, address), location=url_for("addresses.get_address", address_id=address.id))

@addresses_bp.patch("/<int:address_id>")
def update_address(address_id: int):
    data = parse(AddressUpdate, request.get_json())
    address = _address_service().update_address(address_id, data)
    return ok(serialize(AddressRead, address))

@addresses_bp.delete("/<int:address_id>")
def delete_address(address_id: int):
    _address_service().delete_address(address_id)
    return no_content()