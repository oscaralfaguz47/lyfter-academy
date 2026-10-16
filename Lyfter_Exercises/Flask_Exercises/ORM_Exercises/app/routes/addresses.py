from flask import Blueprint, request

from app.services.address_service import AddressService
from app.database import get_session
from app.repositories.address_repository import AddressRepository
from app.schemas.validation import parse
from app.schemas.pagination import PaginationParams
from app.schemas.address import AddressRead
from app.routes.responses import pagination_meta, serialize_many
from app.routes.responses import ok


addresses_bp = Blueprint("addresses", __name__, url_prefix="/api/v1/addresses")

def _address_service() -> AddressService:
    session = get_session()
    return AddressService(session, AddressRepository(session))


@addresses_bp.get("")
def list_addresses():
    pagination = parse(PaginationParams, request.args.to_dict(), "Invalid query params.")
    addresses, total = _address_service().list_addresses(pagination)
    meta = pagination_meta(pagination.page, pagination.per_page, total)
    return ok(serialize_many(AddressRead, addresses), meta=meta)