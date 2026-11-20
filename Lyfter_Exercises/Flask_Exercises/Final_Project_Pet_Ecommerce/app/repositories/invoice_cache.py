from app.cache import Cache
from app.repositories.resource_cache import ResourceCache
from app.schemas.invoice import InvoicePage, InvoiceRead



class InvoiceCache(ResourceCache[InvoiceRead, InvoicePage]):
    """ Items are keyed by invoice_number, the number the API uses. """
    def __init__(self, cache: Cache) -> None:
        super().__init__(
            cache,
            prefix="invoices:v1",
            item_schema=InvoiceRead,
            page_schema=InvoicePage,
            item_ttl_seconds=300,
            list_ttl_seconds=60,
        )